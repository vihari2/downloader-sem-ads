from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import yt_dlp
import requests
import os

# Streaming: envia em chunks, sem carregar tudo na memória -correção

app = Flask(__name__)

ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "*")
CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGIN}})


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "InstaDownloader backend rodando!"})


@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url") if data else None

    if not url:
        return jsonify({"error": "Link vazio!"}), 400

    if "instagram.com" not in url:
        return jsonify({"error": "Por favor, cole um link do Instagram."}), 400

    try:
        ydl_opts = {
            "format": "best[ext=mp4]/best",
            "quiet": True,
            "no_warnings": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get("url")
            title = info.get("title", "video_instagram")

            if not video_url:
                return jsonify({"error": "Não foi possível obter o link do vídeo."}), 500

        
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.instagram.com/",
        }
        video_stream = requests.get(video_url, stream=True, headers=headers, timeout=30)

        safe_title = "".join(c for c in title if c.isalnum() or c in " _-")[:50].strip()
        filename = f"{safe_title or 'video_instagram'}.mp4"

        def generate():
            for chunk in video_stream.iter_content(chunk_size=1024 * 256):
                if chunk:
                    yield chunk

        return Response(
            generate(),
            mimetype="video/mp4",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Type": "video/mp4",
            },
        )

    except yt_dlp.utils.DownloadError as e:
        msg = str(e)
        if "Private" in msg or "login" in msg.lower():
            return jsonify({"error": "Este perfil é privado ou requer login."}), 403
        return jsonify({"error": "Não foi possível processar esse link."}), 500

    except Exception as e:
        return jsonify({"error": "Erro interno: " + str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
