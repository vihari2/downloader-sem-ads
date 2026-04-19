# InstaDownloader

Um web app simples e funcional para baixar vídeos e Reels do Instagram diretamente no celular ou computador.

---

## Objetivo 
Permitir que o usuário cole o link de um vídeo do Instagram, clique em um botão e o download comece automaticamente na sua máquina.

## Tecnologias e Estrutura
O projeto utiliza uma arquitetura **Frontend + Backend (API)** para contornar as restrições de segurança do Instagram.

### Frontend
- **HTML5 / CSS3 / JavaScript**
- Interface responsiva (funciona em qualquer tela).
- Captura a URL do vídeo e faz a chamada para o servidor.

### Backend
- **Python (Flask)** 
- **Biblioteca:** `yt-dlp`

---

## 📁 Organização de Pastas
```text
meu-downloader/
├── frontend/             # Interface do usuário
│   ├── index.html        # Campo de input e botão
│   ├── style.css         # Estilização (CSS)
│   └── script.js         # Lógica de envio para a API
├── backend/              # Servidor (API própria)
│   ├── main.py           # Código do servidor e extração
│   └── requirements.txt  # Bibliotecas necessárias (yt-dlp, etc.)
└── README.md             # Documentação do projeto
