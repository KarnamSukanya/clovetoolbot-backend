import ollama

from services.semantic_search_service import search_tools


# ----------------------------------------
# RAG Response Generator
# ----------------------------------------

def generate_rag_response(user_query):

    # ----------------------------------------
    # Retrieve Related Engineering Tools
    # ----------------------------------------

    retrieved_documents = search_tools(
        user_query,
        top_k=3
    )

    # ----------------------------------------
    # Debug Retrieved Documents
    # ----------------------------------------

    print("\n========== RETRIEVED DOCUMENTS ==========\n")

    for doc in retrieved_documents:

        print(doc[:1500])
        print("\n-----------------------------------\n")

    # ----------------------------------------
    # Structured Engineering Context
    # ----------------------------------------

    engineering_context = ""

    for index, document in enumerate(retrieved_documents):

        engineering_context += f"""

==============================
ENGINEERING TOOL {index + 1}
==============================

{document}

"""

    # ----------------------------------------
    # System Prompt
    # ----------------------------------------

    system_prompt = f"""
You are CloveToolBot.

You are a STRICT engineering retrieval assistant.

You MUST ONLY answer using the exact information
provided inside Retrieved Engineering Context.

STRICT RULES:

- DO NOT invent anything.
- DO NOT generate fake tool IDs.
- DO NOT generate fake URLs.
- DO NOT generate external products.
- DO NOT generate assumptions.
- DO NOT explain beyond retrieved data.
- DO NOT mention Autodesk tools unless explicitly retrieved.
- DO NOT create examples.

If exact information is unavailable,
respond ONLY with:

"Relevant engineering data not found in memory."

ONLY summarize and organize retrieved engineering data.

ONLY use:
- tool names
- tool IDs
- workflows
- APIs
- dependencies
- automation logic
that explicitly exist in Retrieved Engineering Context.

Retrieved Engineering Context:
{engineering_context}
"""

    # ----------------------------------------
    # Generate Response from Ollama
    # ----------------------------------------

    response = ollama.chat(
        model="deepseek-coder",
        options={
            "temperature": 0.1
        },
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    )

    return response["message"]["content"]