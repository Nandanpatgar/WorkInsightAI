import json
import requests


# ============================================================
# CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/chat"

MODEL_NAME = "llama3.2"

REQUEST_TIMEOUT = 120


# ============================================================
# EVIDENCE EXTRACTION
# ============================================================

def extract_evidence(
    competency,
    scenario,
    response,
    evidence_dimensions,
):
    """
    Extract evidence from an employee's response.

    Parameters:
        competency: The competency being assessed.
        scenario: The workplace scenario.
        response: The employee's written response.
        evidence_dimensions: Expected competency dimensions.

    Returns:
        A dictionary containing extracted evidence,
        covered dimensions, missing dimensions,
        and an overall evidence summary.
    """

    if not response or not response.strip():
        raise ValueError(
            "The employee response cannot be empty."
        )

    dimensions_text = "\n".join(
        f"- {dimension}"
        for dimension in evidence_dimensions
    )

    # --------------------------------------------------------
    # 1. Construct the AI instructions
    # --------------------------------------------------------

    system_prompt = """
You are an evidence extraction component in a workplace
assessment application.

Your task is to identify evidence explicitly present in
an employee's response.

Rules:

1. Use only information provided in the employee response.
2. Never invent actions, intentions, experiences, or outcomes.
3. Do not treat a proposed action as an action already completed.
4. Separate distinct pieces of evidence.
5. Map evidence to the supplied competency dimensions.
6. If a dimension has no supporting evidence, mark it missing.
7. Do not make hiring, firing, promotion, or personality decisions.
8. Do not infer protected or sensitive personal attributes.
9. Return valid JSON only.
10. If evidence is ambiguous, identify the ambiguity.
"""

    user_prompt = f"""
Analyze the following workplace assessment response.

COMPETENCY:
{competency}

WORKPLACE SCENARIO:
{scenario}

EMPLOYEE RESPONSE:
<employee_response>
{response}
</employee_response>

EXPECTED EVIDENCE DIMENSIONS:
{dimensions_text}

Return a JSON object using this structure:

{{
    "competency": "{competency}",
    "evidence_items": [
        {{
            "evidence": "A concise description of the evidence",
            "supporting_text": "Exact text copied from the response",
            "dimension": "One supplied competency dimension",
            "evidence_type": "action, reasoning, or expected_outcome",
            "status": "explicit or ambiguous"
        }}
    ],
    "covered_dimensions": [
        "A dimension supported by evidence"
    ],
    "missing_dimensions": [
        "A dimension without supporting evidence"
    ],
    "ambiguities": [
        "An ambiguity that needs clarification"
    ],
    "summary": "A concise summary of the evidence found"
}}

Important:
- Every supporting_text value must be copied from the employee response.
- Do not invent quotations.
- Use only the supplied competency dimensions.
- Include a dimension in covered_dimensions only when
  supporting evidence exists.
- Include a dimension in missing_dimensions when the response
  does not provide evidence for it.
- If no evidence exists, return an empty evidence_items array.
"""

    # --------------------------------------------------------
    # 2. Send the request to Ollama
    # --------------------------------------------------------

    payload = {
        "model": MODEL_NAME,
        "stream": False,
        "format": "json",
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        "options": {
            "temperature": 0,
        },
    }

    try:
        api_response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

        api_response.raise_for_status()

    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Cannot connect to Ollama. "
            "Make sure Ollama is running on your computer."
        ) from exc

    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "Ollama took too long to respond. "
            "Please try again."
        ) from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Ollama request failed: {exc}"
        ) from exc

    # --------------------------------------------------------
    # 3. Parse the Ollama response
    # --------------------------------------------------------

    try:
        api_data = api_response.json()

        model_output = api_data["message"]["content"]

        result = json.loads(model_output)

    except (ValueError, KeyError, TypeError) as exc:
        raise RuntimeError(
            "The AI returned an invalid JSON response. "
            "Please try again."
        ) from exc

    # --------------------------------------------------------
    # 4. Validate the result structure
    # --------------------------------------------------------

    required_fields = [
        "evidence_items",
        "covered_dimensions",
        "missing_dimensions",
        "ambiguities",
        "summary",
    ]

    for field in required_fields:
        if field not in result:
            raise RuntimeError(
                f"The AI response is missing the '{field}' field."
            )

    if not isinstance(result["evidence_items"], list):
        raise RuntimeError(
            "The AI returned an invalid evidence_items value."
        )

    if not isinstance(result["covered_dimensions"], list):
        raise RuntimeError(
            "The AI returned an invalid covered_dimensions value."
        )

    if not isinstance(result["missing_dimensions"], list):
        raise RuntimeError(
            "The AI returned an invalid missing_dimensions value."
        )

    if not isinstance(result["ambiguities"], list):
        raise RuntimeError(
            "The AI returned an invalid ambiguities value."
        )

    # --------------------------------------------------------
    # 5. Normalize competency dimensions
    # --------------------------------------------------------

    valid_dimensions = set(evidence_dimensions)

    result["covered_dimensions"] = [
        dimension
        for dimension in result["covered_dimensions"]
        if dimension in valid_dimensions
    ]

    result["missing_dimensions"] = [
        dimension
        for dimension in evidence_dimensions
        if dimension not in result["covered_dimensions"]
    ]

    # Ensure the competency is consistent with the request.
    result["competency"] = competency

    return result