import json
import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2"


def generate_followup_questions(
    competency,
    missing_dimensions,
    ambiguities=None,
    max_questions=3,
):
    """
    Generate targeted follow-up questions based on missing
    competency evidence and ambiguities in the user's response.
    """

    ambiguities = ambiguities or []

    # No follow-up questions are required when there are no gaps.
    if not missing_dimensions and not ambiguities:
        return []

    prompt = f"""
You are an evidence-focused workplace assessment assistant.

Selected competency:
{competency}

Missing evidence dimensions:
{json.dumps(missing_dimensions, ensure_ascii=False)}

Ambiguities:
{json.dumps(ambiguities, ensure_ascii=False)}

Generate up to {max_questions} concise follow-up questions.

Rules:
1. Ask only about missing or unclear evidence.
2. Do not repeat information already provided.
3. Ask neutral, specific, non-leading questions.
4. Do not assign scores or make hiring decisions.
5. Return ONLY a valid JSON array of strings.

Example:
[
    "What specific action would you take to coordinate the remaining tasks?",
    "How would you check whether your approach was successful?"
]
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Generate relevant workplace assessment "
                            "follow-up questions. Return valid JSON only."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0.3,
                },
            },
            timeout=90,
        )

        response.raise_for_status()

        result = response.json()
        content = result.get("message", {}).get("content", "")

        parsed = json.loads(content)

        # Accept either a JSON list or a JSON object containing questions.
        if isinstance(parsed, dict):
            questions = parsed.get("questions", [])
        elif isinstance(parsed, list):
            questions = parsed
        else:
            questions = []

        # Keep only non-empty strings.
        questions = [
            question.strip()
            for question in questions
            if isinstance(question, str) and question.strip()
        ]

        return questions[:max_questions]

    except (
        requests.RequestException,
        ValueError,
        TypeError,
    ):
        # Simple fallback if Ollama is unavailable or returns invalid JSON.
        fallback_questions = []

        for dimension in missing_dimensions:
            fallback_questions.append(
                f"What specific actions would you take to demonstrate "
                f"{dimension.lower()} in this situation?"
            )

            if len(fallback_questions) >= max_questions:
                break

        if not fallback_questions and ambiguities:
            fallback_questions.append(
                "Could you clarify the specific actions you would take "
                "and explain why?"
            )

        return fallback_questions[:max_questions]