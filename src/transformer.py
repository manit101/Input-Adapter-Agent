import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from the .env file")

client = genai.Client(api_key=api_key)

def transform(input_text, target_schema):
    # Gemini returns either a successful payload or a structured error.
    response_schema = {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": ["success", "error"]
            },
            "data": {
                "anyOf": [
                    target_schema,
                    {"type": "null"}
                ]
            },
            "missing_fields": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "message": {
                "type": ["string", "null"]
            }
        },
        "required": [
            "status",
            "data",
            "missing_fields",
            "message"
        ]
    }

    prompt = f"""
    You are an input transformation agent.

    Read the user's message and the target JSON schema.

    Target schema:
    {json.dumps(target_schema, indent=2)}

    User's message:
    {input_text}

    Rules:
    1. Extract information and intent from the user's message.
    2. Map and normalize it to the target schema.
    3. You may generate reasonable content for fields that are meant
    to be composed, such as an email body or subject, using the
    information and intent provided by the user.
    4. Do not invent critical facts, identities, dates, amounts,
    decisions, or other required values that the user did not provide.
    5. Distinguish between content you can reasonably compose and
    factual information that must come from the user.
    4. Treat required fields in the target schema as mandatory.
    5. If any required field cannot be determined from the user's message,
    return status "error", data null, list the missing field names in
    missing_fields, and explain the problem in message.
    6. Do not treat the string "null" as a real value.
    7. If required information is ambiguous, return status "error".
    8. If all required information is available, return status "success",
    put the transformed payload in data, use an empty missing_fields array,
    and set message to null.
    9. The data object must match the target schema exactly.
    10. Return only JSON in the required response format.
    11. Preserve all relevant information explicitly provided by the user.
    12. For object-valued fields such as "data" and "conditions",
        populate the object with relevant extracted information whenever
        the user's message provides it.
    13. Do not return an empty object for a field when the user has
        explicitly supplied relevant values for that field.
    14. Before returning success, check that no relevant user-provided
        information has been accidentally omitted.
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": response_schema
        }
    )

    return json.loads(response.text)
