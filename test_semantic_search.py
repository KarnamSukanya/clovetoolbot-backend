from services.semantic_search_service import search_tools


query = """
Need AutoCAD drafting automation tool
for level alignment and annotation management
"""

results = search_tools(query)

for result in results:

    print("\n")
    print(result)