import ollama

from services.semantic_search_service import (
    search_tools
)

from services.context_compressor import (
    compress_engineering_context
)


# ----------------------------------------
# Generate Engineering AI Response
# ----------------------------------------

def generate_rag_response(user_query):

    # ----------------------------------------
    # Retrieve Relevant Engineering Chunks
    # ----------------------------------------

    retrieved_results = search_tools(
        user_query,
        top_k=2
    )

    # ----------------------------------------
    # Compress Engineering Context
    # ----------------------------------------

    engineering_context = compress_engineering_context(
        retrieved_results
    )

    # ----------------------------------------
    # Engineering System Prompt
    # ----------------------------------------

    system_prompt = f"""
You are CloveToolBot.

You are an engineering retrieval assistant.

Your task is to:

1. Analyze retrieved engineering functions.

2. Identify reusable AutoLISP logic.

3. Suggest ONLY relevant engineering APIs,
functions, and reusable implementation patterns.

STRICT RULES:

- DO NOT generate full AutoLISP applications.
- DO NOT invent APIs.
- DO NOT invent AutoCAD functions.
- DO NOT generate pseudo-code.
- ONLY summarize reusable engineering logic.
- Keep responses concise.
- Focus on APIs, reusable functions,
and engineering implementation approaches.

Retrieved Engineering Context:
{engineering_context}
"""

    # ----------------------------------------
    # Generate AI Engineering Response
    # ----------------------------------------

    response = ollama.chat(

        model="qwen2.5-coder:1.5b",

        options={

            "temperature": 0.1,
            "num_predict": 120

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