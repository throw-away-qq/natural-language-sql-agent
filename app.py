
import streamlit as st
import sqlite3
import re
import os
from openai import OpenAI

# ======================
# CONFIG
# ======================
DB_PATH = "Chinook_Sqlite.sqlite"
API_KEY = os.environ.get("OPENROUTER_API_KEY", "your-openrouter-api-key")

# Use real, available models
GUARD_MODEL = 'google/gemma-3n-e4b-it:free'
META_MODEL = "google/gemini-2.5-flash-lite-preview-09-2025"
SQL_MODEL = "google/gemini-2.5-flash-lite-preview-09-2025"
ANSWER_MODEL = 'google/gemma-3n-e4b-it:free'

# Load schema (MUST be UTF-8)
try:
    with open("schema.sql", "r", encoding="utf-16") as f:
        SCHEMA_DDL = f.read()
except Exception as e:
    st.error(f"schema.sql missing or not UTF-16: {e}")
    st.stop()

# ======================
# PROMPTS
# ======================
GUARD_PROMPT = """You are a validator. Is the question:
- About the Chinook music store database?
- Safe and non-malicious?
Answer ONLY "VALID" or "INVALID".

Question: {question}
"""

META_PROMPT = """You are a database expert. Is this question asking about the database structure (e.g., tables, columns, relationships) rather than data?

Examples of YES: 
- "What tables are in the database?"
- "What columns does the Customer table have?"
- "Describe the schema."

Examples of NO:
- "How many customers are there?"
- "List artists from the 80s"

Answer ONLY "META" or "DATA".

Question: {question}
"""

SQL_PROMPT = """Generate a SQLite SELECT query. Rules:
- Use ONLY the provided schema
- NO explanations, markdown, or comments
- Output ONLY the SQL ending with ;

Schema:
{schema}

Question: {question}
"""

ANSWER_FROM_META_PROMPT = """Answer the user's question using ONLY the database schema below.

Question: {question}
Schema:
{schema}

Answer concisely in natural language.
"""

ANSWER_FROM_DATA_PROMPT = """Answer using the SQL result.

Question: {question}
Result (tab-separated):
{result}

Answer concisely. Do not mention SQL.
"""

# ======================
# HELPERS
# ======================
def call_openrouter(model: str, prompt: str) -> str:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=API_KEY)
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=500,
    )
    return resp.choices[0].message.content.strip()

def safe_execute_sql(sql: str):
    if not re.match(r"^\s*SELECT\s", sql, re.IGNORECASE):
        raise ValueError("Only SELECT allowed")
    for kw in ["DROP", "DELETE", "INSERT", "UPDATE", "ATTACH", "PRAGMA"]:
        if kw in sql.upper():
            raise ValueError("Unsafe SQL")
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

def format_tsv(rows):
    if not rows:
        return "(no results)"
    header = "\t".join(rows[0].keys())
    body = "\n".join("\t".join(str(v) for v in r) for r in rows)
    return f"{header}\n{body}"

# ======================
# STREAMLIT APP
# ======================
st.set_page_config(page_title="Chinook NL-to-SQL + Meta", layout="wide")
st.title("🎵 Chinook NL-to-SQL + Schema Q&A")
st.caption("Ask about data OR database structure (tables, columns, etc.)")

st.info("""
**Try these:**
- *Data*: "Top 3 customers by total spending"
- *Meta*: "What columns are in the Invoice table?"
- *Meta*: "List all tables in the database"
""")

question = st.text_input("Ask anything about the Chinook database:", 
                        placeholder="e.g., How many tracks are there? OR What is the schema?")

if st.button("Get Answer") and question:
    if not API_KEY or API_KEY == "your-openrouter-api-key":
        st.error("🔑 Set OpenRouter API key in environment variable OPENROUTER_API_KEY")
        st.stop()

    try:
        # === STEP 1: GUARDRAIL ===
        with st.spinner("Validating..."):
            guard_out = call_openrouter(GUARD_MODEL, GUARD_PROMPT.format(question=question))
            if "VALID" not in guard_out.upper():
                st.error("Rejected: off-topic or unsafe.")
                st.stop()

        # === STEP 2: META vs DATA ===
        with st.spinner("Classifying..."):
            meta_out = call_openrouter(META_MODEL, META_PROMPT.format(question=question))
            is_meta = "META" in meta_out.upper()

        if is_meta:
            # === META PATH ===
            with st.spinner("Answering from schema..."):
                natural_answer = call_openrouter(
                    ANSWER_MODEL,
                    ANSWER_FROM_META_PROMPT.format(question=question, schema=SCHEMA_DDL)
                )
                sql_query = None
                results = None
        else:
            # === SQL PATH ===
            with st.spinner("Generating SQL..."):
                sql_raw = call_openrouter(SQL_MODEL, SQL_PROMPT.format(schema=SCHEMA_DDL, question=question))
                sql_match = re.search(r"(SELECT.*?;)", sql_raw, re.DOTALL | re.IGNORECASE)
                sql_query = sql_match.group(1) if sql_match else sql_raw.split("\n")[0]

            with st.spinner("Executing..."):
                results = safe_execute_sql(sql_query)
                tsv_result = format_tsv(results)

            with st.spinner("Generating answer..."):
                natural_answer = call_openrouter(
                    ANSWER_MODEL,
                    ANSWER_FROM_DATA_PROMPT.format(question=question, result=tsv_result)
                )

        # === OUTPUT ===
        st.subheader("Answer")
        st.write(natural_answer)

        if is_meta:
            st.subheader("Answer Source")
            st.write("Schema introspection (no SQL executed)")
        else:
            st.subheader("Generated SQL")
            st.code(sql_query, language="sql")
            st.subheader("Results")
            if results:
                st.dataframe([dict(r) for r in results], use_container_width=True)
            else:
                st.write("(no results)")

    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")
st.caption("Supports both data queries and schema/meta questions • Read-only • Chinook DB")
