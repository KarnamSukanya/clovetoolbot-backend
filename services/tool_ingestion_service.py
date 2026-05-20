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
# Add Chunk To ChromaDB
# ----------------------------------------

def add_chunk(
    chunk_id,
    chunk_text,
    metadata
):

    embedding = embedding_model.encode(
        chunk_text
    ).tolist()

    collection.add(
        documents=[chunk_text],
        embeddings=[embedding],
        ids=[chunk_id],
        metadatas=[metadata]
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

            description = str(
                row.get("Detailed Description", "")
            )

            keywords = str(
                row.get("Keywords", "")
            )

            workflows = str(
                row.get("Related Workflows", "")
            )

            automation_logic = str(
                row.get("Automation Logic", "")
            )

            dependencies = str(
                row.get("Dependencies", "")
            )

            reusable_components = str(
                row.get("Reusable Components", "")
            )

            code_path = str(
                row.get("Code File Path", "")
            )

            code_content = ""

            # ----------------------------------------
            # Read Code File
            # ----------------------------------------

            if os.path.exists(code_path):

                with open(
                    code_path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as file:

                    code_content = file.read()

            # ----------------------------------------
            # Create Engineering Chunks
            # ----------------------------------------

            chunks = [

                {
                    "id": f"{tool_id}_description",
                    "text": f"""
Tool ID:
{tool_id}

Tool Name:
{tool_name}

Description:
{description}

Keywords:
{keywords}
""",
                    "metadata": {
                        "tool_id": tool_id,
                        "tool_name": tool_name,
                        "chunk_type": "description"
                    }
                },

                {
                    "id": f"{tool_id}_workflow",
                    "text": f"""
Tool ID:
{tool_id}

Tool Name:
{tool_name}

Workflows:
{workflows}

Automation Logic:
{automation_logic}
""",
                    "metadata": {
                        "tool_id": tool_id,
                        "tool_name": tool_name,
                        "chunk_type": "workflow"
                    }
                },

                {
                    "id": f"{tool_id}_dependencies",
                    "text": f"""
Tool ID:
{tool_id}

Tool Name:
{tool_name}

Dependencies:
{dependencies}

Reusable Components:
{reusable_components}
""",
                    "metadata": {
                        "tool_id": tool_id,
                        "tool_name": tool_name,
                        "chunk_type": "dependencies"
                    }
                },

                {
                    "id": f"{tool_id}_code",
                    "text": f"""
Tool ID:
{tool_id}

Tool Name:
{tool_name}

Code:
{code_content}
""",
                    "metadata": {
                        "tool_id": tool_id,
                        "tool_name": tool_name,
                        "chunk_type": "code"
                    }
                }
            ]

            # ----------------------------------------
            # Store Chunks
            # ----------------------------------------

            for chunk in chunks:

                add_chunk(
                    chunk["id"],
                    chunk["text"],
                    chunk["metadata"]
                )

            print(f"Ingested: {tool_name}")

        except Exception as e:

            print(f"Error on row {index}: {e}")

    print("All tools ingested successfully.")