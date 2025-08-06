# Job Skills Trend Tracker

This project analyzes job descriptions to extract and track trending technical skills over time using automation and AI.

## 🚀 Project Goals

- Automate ingestion of job description files from Google Drive
- Extract relevant technical skills from each job description
- Index the extracted data using ChromaDB (vector store)
- Maintain a Google Sheet for skill frequency and trends
- Visualize top skills per job type or time period

## 🧰 Tech Stack

- **n8n**: No-code/low-code automation platform (Docker)
- **Python**: For skill extraction, processing, and Chroma integration
- **ChromaDB**: Lightweight vector database for skill indexing
- **Google Drive & Sheets APIs**: Input and output data
- **OpenAI API**: Skill extraction using LLMs

## 🗂️ Project Structure

```text
jobSkillsMap/
├── docker-compose.yml         # n8n container setup
├── .env                       # Secrets and API keys (excluded from Git)
├── requirements.txt           # Python dependencies
├── chroma/                    # Chroma vectorDB stuff
├── n8n_credentials/           # n8n workflows and saved credentials
├── gdrive/                    # Google API auth and helpers for I/O
├── pipelines/                 # Python scripts for skill extraction, DB updates
│   ├── extract_skills.py
│   └── update_chroma.py
├── webapp/                    # Optional Flask for job description input
├── docs/                      # Architecture, notes, screenshots
└── README.md

```




## 🧪 Setup Instructions

1. Clone the repo and run `docker-compose up`
2. Create n8n owner account at `http://localhost:5678`
3. Set up Google and OpenAI credentials via `.env` and n8n UI
4. Run `pip install -r requirements.txt` inside virtualenv
5. Drop `.docx` files into `inputs/` and trigger pipeline

## 📈 Coming Soon

- Google Sheet skill trend heatmap
- Dashboards or Streamlit visualizations
- Webhook-based ingestion pipeline

---

Let me know if you'd like to customize this with your blog, LinkedIn, or repo badges.

Once you're happy with this, you can:

```sh
git add README.md
git commit -m "Add initial README with project goals and setup"
git push
