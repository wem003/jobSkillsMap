# jobSkillsMap

This project analyzes job descriptions to extract and track trending technical skills over time using automation and AI.

## 🚀 Project Goals

- Automate ingestion of job description files from Google Drive
- Extract relevant technical skills from each job description
- Index the extracted data using ChromaDB (vector store)
- Maintain a Google Sheet for skill frequency and trends
- Visualize top skills per job type or time period

## 🧰 Tech Stack

- **Flask**: Simple local UI for job description submission and status tracking
- **n8n**: No-code/low-code automation platform (Docker)
- **Python**: For skill extraction, processing, and Chroma integration
- **ChromaDB**: Lightweight vector database for skill indexing
- **Google Drive & Sheets APIs**: Input and output data
- **OpenAI API**: Skill extraction using LLMs

## 🗂️ Project Structure

> **Note:** This structure includes planned folders for the full implementation.  
> Some directories may not exist or be populated until the corresponding features are complete.

```text
jobSkillsMap/
├── docker-compose.yml         # n8n container setup
├── .env                       # Secrets and API keys (excluded from Git)
├── requirements.txt           # Python dependencies
├── chroma/                    # Chroma vectorDB files
├── n8n_credentials/           # n8n workflows and saved credentials
├── gdrive/                    # Google API auth and I/O helpers
├── pipelines/                 # Python scripts for skill extraction, DB updates
│   ├── extract_skills.py
│   └── update_chroma.py
├── webapp/                    # Flask app for submission & status tabs
│   ├── templates/
│   └── static/
├── data/
│   ├── pending/               # Google Drive "Pending" folder mirror
│   └── processed/             # Google Drive "Processed" folder mirror
├── docs/                      # Architecture diagrams, notes, screenshots
└── README.md
```




## 🧪 Setup Instructions

**COMING SOON** – Will be updated once the Flask app and n8n workflows are complete.


---

## Functional Requirements

### UI Layer (Flask App)
- **Simple input form with two tabs**
  - **Tab 1 – Submission**
    - Input fields for:
      - Job Title
      - Company
      - Job Description
    - Header shows the count of pending and processed files
    - On submission, a new text file named with a title/timestamp is saved to a `Pending` folder in Google Drive
  - **Tab 2 – Status**
    - Show a table of uploaded job files with:
      - File name
      - Timestamp
      - Status – pending or processed
    - Files do not need to be viewable in the first iteration

---

### Automation Layer (n8n)
- Poll Google Drive `Pending` folder on a schedule
- For each file:
  1. Get job title and description
  2. Use OpenAI API to determine skills from the description text
  3. Save skills as structured data
  4. Index these skills in **ChromaDB** (vector store)
  5. Move the file to the Google Drive `Processed` folder


### Retrieval and Analysis Phase
- Enable retrieval of the **top 15 skills** for a given job title using similarity search or tag aggregation (TBD)
- **Process:**
  1. Python script running on cron or n8n scheduled task
  2. Use ChromaDB API to run similarity search on stored data
  3. Filter by job titles or embedding similarity
  4. Aggregate skills
  5. Return the top 15 with counts:
     - Number of occurrences
     - Number of jobs (weighted)
- **Output formats:** JSON, CSV, or similar for stretch goals

### Stretch Goals
1. **Visualization:** Display top skills (bar chart, heatmap, etc.)
2. **Trends Over Time:** Compare skill demands for a given title now vs. 6 months later to track evolution

### Constraints / Notes
- **No job scraping** – respect TOS of job boards
- No authentication in the initial version beyond required API keys (single-user app, running locally)
- Visualization is optional – raw CSV/text output is fine for now
- No AI code assist tools were used for coding; learning resources included ChatGPT, YouTube, and Udemy


---

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
