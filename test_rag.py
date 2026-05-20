from services.rag_service import generate_rag_response


query = """
Need AutoLISP function using
vla-InsertBlock and
vlax-curve-getPointAtDist
"""

response = generate_rag_response(
    query
)

print(response)