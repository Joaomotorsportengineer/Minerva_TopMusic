# Minerva Top Music

Aplicação web em **Streamlit** para explorar as músicas mais tocadas do **Billboard Hot 100** por ano, com links para o YouTube e um **Chatbot com agente SQL** que responde perguntas sobre o banco de dados de músicas.

---

## Índice

- [Funcionalidades](#funcionalidades)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Como executar](#como-executar)
- [Banco de dados](#banco-de-dados)
- [Páginas do app](#páginas-do-app)
- [Tecnologias](#tecnologias)
- [Observações](#observações)

---

## Funcionalidades

- **Top músicas por ano** – Ranking Billboard Hot 100 year-end (anos 2006–2025).
- **Quantidade configurável** – Escolha de 5 a 100 músicas por ano (slider).
- **Links para o YouTube** – Cada música com link para busca no YouTube (via API ou URL de busca).
- **Imagens** – Capa da música (YouTube quando há API key).
- **Chatbot com agente SQL** – Perguntas em linguagem natural sobre o banco; o agente gera e executa SQL e responde com base na tabela `top_musicas`.
- **Tema** – Configuração de tema (claro/escuro) em `.streamlit/config.toml`.
- **Script de base de dados** – Script para popular o SQLite com top 10 por ano (2006–2025) a partir do Billboard.

---

## Estrutura do projeto

```
Minerva_TopMusic/
├── .env                    # Chaves de API (não commitar)
├── .gitignore
├── .streamlit/
│   └── config.toml         # Tema e configurações do Streamlit
├── BaseDados/
│   ├── top_musicas.db      # Banco SQLite (tabela top_musicas)
│   └── TopMusicData.py     # Script para popular o banco
├── pages/
│   └── 1_Chatbot.py        # Página do Chatbot (agente SQL)
├── requirements.txt
├── README.md
├── Top_Musics.py           # Página principal (top músicas por ano)
```

---

## Pré-requisitos

- **Python 3.10+**
- Conta na [OpenAI](https://platform.openai.com/) (API key) para o Chatbot
- (Opcional) [YouTube Data API v3](https://console.cloud.google.com/) para links e miniaturas; sem API key, o app usa URL de busca no YouTube

---

## Instalação

1. **Clone o repositório**

   ```bash
   git clone https://github.com/Joaomotorsportengineer/Minerva_TopMusic.git
   cd Minerva_TopMusic
   ```

2. **Crie e ative um ambiente virtual**

   ```bash
   python -m venv venv
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuração

1. **Crie o arquivo `.env` na raiz do projeto** (o `.env` não deve ser commitado):

   ```env
   OPENAI_API_KEY=sua_chave_openai_aqui
   YOUTUBE_API_KEY=sua_chave_youtube_aqui
   ```

   - **OPENAI_API_KEY** – Obrigatória para o Chatbot (agente SQL). Obtenha em [OpenAI API Keys](https://platform.openai.com/account/api-keys).
   - **YOUTUBE_API_KEY** – Opcional. Se não definir, os links das músicas usam a URL de busca do YouTube (sem consumo de cota). Obtenha em [Google Cloud Console](https://console.cloud.google.com/) (YouTube Data API v3).

2. **Tema do Streamlit** (opcional)

   Edite `.streamlit/config.toml` e altere `base = "dark"` para `base = "light"` se quiser tema claro.

---

## Como executar

1. **(Opcional) Popular o banco de dados**  
   Se ainda não tiver o arquivo `BaseDados/top_musicas.db` ou quiser atualizar os dados:

   ```bash
   cd BaseDados
   python TopMusicData.py
   cd ..
   ```

   Isso gera/atualiza o SQLite com as top 10 músicas por ano (2006–2025) a partir do Billboard.

2. **Inicie o app Streamlit**

   ```bash
   streamlit run Top_Musics.py
   ```

   O app abre no navegador em `http://localhost:8501` (ou na porta definida em `config.toml`).

---

## Banco de dados

- **Arquivo:** `BaseDados/top_musicas.db` (SQLite)
- **Tabela:** `top_musicas`

| Coluna      | Tipo    | Descrição                    |
|-------------|---------|------------------------------|
| id          | INTEGER | Chave primária               |
| nome_musica | TEXT    | Nome da música               |
| ano         | INTEGER | Ano do ranking (2006–2025)   |
| autor       | TEXT    | Nome do(s) artista(s)        |
| colocacao   | INTEGER | Posição no ranking (1–10)    |

O **Chatbot** usa essa tabela para responder perguntas em linguagem natural (ex.: "Quantas músicas temos?", "Quais músicas do artista X?").

---

## Páginas do app

| Página       | Arquivo             | Descrição                                                                 |
|--------------|---------------------|---------------------------------------------------------------------------|
| **Top músicas** | `Top_Musics.py`     | Página inicial: seleção de ano, quantidade (5–100), lista com link YouTube e ano ao lado de cada música. |
| **Chatbot**  | `pages/1_Chatbot.py` | Chat com agente SQL: perguntas sobre o banco (top_musicas); respostas geradas por consultas SQL. |

---

## Tecnologias

- **Streamlit** – Interface web
- **billboard.py** – Dados do Billboard Hot 100 year-end
- **LangChain / LangGraph** – Orquestração do agente
- **LangChain OpenAI** – Modelo de linguagem (ChatGPT) para o agente SQL
- **SQLDatabase (LangChain Community)** – Conexão com SQLite para o agente
- **python-dotenv** – Variáveis de ambiente (`.env`)
- **requests** – Chamadas à API do YouTube (quando configurada)

---

## Observações

- **Anos do Billboard:** O chart year-end `hot-100-songs` suporta anos **2006–2025**. Anos fora desse intervalo podem gerar avisos ou dados vazios.
- **Cota da YouTube API:** O uso da API consome cota diária. Sem API key, o app usa apenas a URL de busca do YouTube.
- **Segurança:** Nunca commite o arquivo `.env`. Mantenha-o no `.gitignore` e use variáveis de ambiente em produção.
- **OpenAI:** O Chatbot consome créditos da sua conta OpenAI; use um modelo compatível com a sua API key (ex.: `gpt-4o`, `gpt-3.5-turbo`).

---

## Licença

Este projeto é de uso educacional e pessoal. Os dados do Billboard são de terceiros; consulte os termos de uso do [Billboard](https://www.billboard.com/terms-of-use).
