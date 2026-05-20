import re


IMPORTANT_PATTERNS = [

    r'vlax-[\w-]+',
    r'vla-[\w-]+',
    r'entmake',
    r'entget',
    r'entmod',
    r'entupd',
    r'command',
    r'vl-cmdf',
    r'ssget',
    r'polar',
    r'angle',
    r'distance',
    r'inters',
    r'trans',
    r'vlax-curve-[\w-]+'

]


def extract_important_apis(text):

    detected_apis = set()

    for pattern in IMPORTANT_PATTERNS:

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        for match in matches:

            detected_apis.add(match)

    return list(detected_apis)


def extract_function_names(text):

    pattern = r'\(defun\s+([^\s\(]+)'

    matches = re.findall(
        pattern,
        text
    )

    return matches


def extract_relevant_code_lines(text):

    important_lines = []

    lines = text.splitlines()

    keywords = [

    'vlax',
    'vla',
    'vla-insertblock',
    'insertblock',
    'entmake',
    'command',
    'vl-cmdf',
    'ssget',
    'offset',
    'polyline',
    'distance',
    'spacing',
    'point',
    'curve',
    'vlax-curve-getpointatdist',
    'vlax-curve-getdistatparam',
    'vlax-curve-getendpoint',
    'vlax-curve-getstartpoint',
    'foreach',
    'repeat',
    'while',
    'polar',
    'angle',
    'block',
    'insert',
    'coordinates'

]

    for line in lines:

        lower_line = line.lower()

        if any(
            keyword.lower() in lower_line
            for keyword in keywords
        ):

            cleaned_line = line.strip()

            if cleaned_line:

                important_lines.append(
                    cleaned_line
                )

    return important_lines[:15]


def compress_engineering_context(
    retrieved_results
):

    compressed_context = ""

    for result in retrieved_results:

        metadata = result["metadata"]

        document = result["document"]

        function_names = extract_function_names(
            document
        )

        apis = extract_important_apis(
            document
        )

        code_lines = extract_relevant_code_lines(
            document
        )

        compressed_context += f"""

==================================================
Tool ID:
{metadata.get('tool_id')}

Tool Name:
{metadata.get('tool_name')}

Chunk Type:
{metadata.get('chunk_type')}
"""

        if metadata.get("function_name"):

            compressed_context += f"""

Function Name:
{metadata.get('function_name')}
"""

        compressed_context += f"""

Important APIs:
{', '.join(apis)}

Detected Functions:
{', '.join(function_names)}

Relevant Engineering Logic:
"""

        for line in code_lines:

            compressed_context += f"""
- {line}
"""

        compressed_context += """

==================================================
"""

    return compressed_context