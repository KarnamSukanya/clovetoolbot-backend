from services.rag_service import generate_rag_response


query = """
Need AutoLISP automation for UCS level alignment,
annotation spacing,
and CAD drafting standardization
"""

response = generate_rag_response(
    query
)

print(response)