# Natural Language to SQL Agent

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OpenRouter API](https://img.shields.io/badge/API-OpenRouter-green.svg)](https://openrouter.ai/)

This project is a Natural Language to SQL agent that converts user questions into safe, read-only SQL queries and returns answers in plain English. It's a complete, educational repository demonstrating how to build a secure, multi-LLM agent using OpenRouter.

This repository is perfect for learning:
- **AI Agent Architecture**: Build a multi-step pipeline with validation, classification, generation, and response agents.
- **Secure LLM Integration**: Implement robust security against SQL injection and malicious queries.
- **OpenRouter API**: Use OpenAI's SDK to interact with dozens of different LLM providers.
- **Prompt Engineering**: Design effective prompts for database-related tasks.

---

## Quick Start (5 Minutes)

### 1. Prerequisites
- Python 3.8+
- An [OpenRouter API Key](https://openrouter.ai/keys) (free tier available)

### 2. Clone and Install
```bash
git clone https://github.com/YOUR-USERNAME/natural-language-sql-agent.git
cd natural-language-sql-agent
pip install -r requirements.txt
```

### 3. Set API Key
Set your OpenRouter API key as an environment variable.

**Windows (PowerShell):**
```powershell
$env:OPENROUTER_API_KEY='your-openrouter-api-key'
```

**Linux/Mac:**
```bash
export OPENROUTER_API_KEY='your-openrouter-api-key'
```
*(Alternatively, you can create a `.env` file from the `.env.example` and paste your key there.)*

### 4. Run the Application
You have two options to run the agent:

**Option A: Streamlit Web App (Recommended)**
```bash
streamlit run app.py
```
Navigate to `http://localhost:8501` in your browser.

**Option B: Jupyter Notebook**
```bash
jupyter notebook SQL_Agent_Final.ipynb
```
Run the cells sequentially to see the step-by-step process.

---

## How It Works: The Agent Pipeline

The agent processes a question in a secure, multi-step pipeline:

1.  **Guardrail Validation**: A small, fast LLM (`google/gemma-3n-e4b-it`) first checks if the question is safe and relevant to the database.
2.  **Query Classification**: A second LLM (`google/gemini-2.5-flash-lite`) determines if the question is about data (e.g., "who are the top customers?") or metadata (e.g., "what tables exist?").
3.  **SQL Generation / Schema Response**:
    *   For **data** questions, a powerful code model (`google/gemini-2.5-flash-lite`) generates a SQL query based on the database schema.
    *   For **metadata** questions, the agent answers directly from the schema definition without querying the database.
4.  **Safe Execution**: The generated SQL is validated against a strict security layer (read-only, no dangerous keywords) before being executed on the `Chinook_Sqlite.sqlite` database.
5.  **Natural Language Response**: The final LLM (`google/gemma-3n-e4b-it`) converts the raw SQL results into a clear, human-readable answer.

This modular architecture makes the agent robust, secure, and easy to modify.

## Project Components

- `SQL_Agent_Final.ipynb`: A Jupyter Notebook providing a step-by-step walkthrough of the agent's logic.
- `app.py`: A user-friendly Streamlit web application for easy interaction.
- `Chinook_Sqlite.sqlite`: The sample music store database.
- `schema.sql` & `sample_rows.txt`: Context files used to help the LLM generate accurate queries.
- `requirements.txt`: A list of all necessary Python packages.

## Configuration

You can easily change the LLMs used for each step by editing the configuration variables in `app.py` or `SQL_Agent_Final.ipynb`.

```python
# AGENT MODELS
SQL_GENERATOR_MODEL = "google/gemini-2.5-flash-lite-preview-09-2025"
GUARDRAIL_MODEL = 'google/gemma-3n-e4b-it:free'
ANSWER_MODEL = 'google/gemma-3n-e4b-it:free'
```
The default models are chosen for their balance of performance and low cost (or free).

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to submit pull requests, report issues, and suggest enhancements.

## License

This project is licensed under the [MIT License](LICENSE).
