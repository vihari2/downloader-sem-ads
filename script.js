const form = document.querySelector(".search-form");
const input = document.querySelector("#input");
const submitBtn = document.querySelector(".form__submit");
const pasteBtn = document.querySelector(".btn-paste");

// Lógica para baixar
form.onsubmit = async (e) => {
  e.preventDefault();
  const url = input.value;
  if (!url) return alert("Por favor, cole um link!");

  submitBtn.innerText = " Processando...";
  submitBtn.disabled = true;

  try {
    const response = await fetch("https://downloader-sem-ads-production.up.railway.app/download", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: url }), 
    });

    if (response.ok) {
      const blob = await response.blob();

      const downloadUrl = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = downloadUrl;
      link.download = "video_instagram.mp4";
      document.body.appendChild(link);
      link.click();

      window.URL.revokeObjectURL(downloadUrl);
      link.remove();
      input.value = "";
    } else {
      const errorData = await response.json();
      alert("Erro no servidor: " + errorData.error);
    }
  } catch (err) {
    console.error("Erro detalhado:", err);
    alert("Erro de conexão ou processamento.");
  } finally {
    console.log("O finally rodou! Resetando botão...");
    submitBtn.innerText = "Baixar Video";
    submitBtn.disabled = false;
  }
};

pasteBtn.addEventListener("click", async () => {
  try{
    const text = await navigator.clipboard.readText();
    input.value = text;
  } catch (err) {
    alert("Não foi possível acessar a área de transferência.");
  }
});
