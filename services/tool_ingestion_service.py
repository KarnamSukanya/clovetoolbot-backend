import os
import chromadb

from sentence_transformers import SentenceTransformer

from services.google_sheet_service import load_tools_sheet


# ----------------------------------------
# ChromaDB Persistent Storage
# ----------------------------------------

client = chromadb.PersistentClient(
    path="database"
)

collection = client.get_or_create_collection(
    name="engineering_tools"
)


# ----------------------------------------
# Embedding Model
# ----------------------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ----------------------------------------
# Tool Ingestion
# ----------------------------------------

def ingest_tools():

    df = load_tools_sheet()

    for index, row in df.iterrows():

        try:

            tool_id = str(row.get("Tool ID", ""))
            tool_name = str(row.get("Tool Name", ""))
            description = str(row.get("Detailed Description", ""))
            keywords = str(row.get("Keywords", ""))
            workflows = str(row.get("Related Workflows", ""))
            automation_logic = str(row.get("Automation Logic", ""))
            dependencies = str(row.get("Dependencies", ""))
            reusable_components = str(row.get("Reusable Components", ""))
            code_path = str(row.get("Code File Path", ""))

            code_content = ""

            # ----------------------------------------
            # Read Actual Tool Code
            # ----------------------------------------

            if os.path.exists(code_path):

                with open(
                    code_path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as file:

                    code_content = file.read()

            else:

                print(f"Code file not found: {code_path}")

            # ----------------------------------------
            # Combined Engineering Intelligence Context
            # ----------------------------------------

            combined_text = f"""
Tool ID:
{tool_id}

Tool Name:
{tool_name}

Description:
{description}

Keywords:
{keywords}

Workflows:
{workflows}

Automation Logic:
{automation_logic}

Dependencies:
{dependencies}

Reusable Components:
{reusable_components}

Code:
{code_content}
"""

            # ----------------------------------------
            # Generate Embeddings
            # ----------------------------------------

            embedding = embedding_model.encode(
                combined_text
            ).tolist()

            # ----------------------------------------
            # Store in ChromaDB
            # ----------------------------------------

            collection.add(
                documents=[combined_text],
                embeddings=[embedding],
                ids=[tool_id]
            )

            print(f"Ingested: {tool_name}")

        except Exception as e:

            print(f"Error on row {index}: {e}")

    print("All tools ingested successfully.")