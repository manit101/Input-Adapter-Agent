import json

from src.transformer import transform
from src.validator import validate_payload


def main():
    print("=== Adaptive Input Transformation Agent ===")

    input_text = input("\nEnter your message:\n> ")

    print("\nPaste the target JSON Schema.")
    print("Enter a blank line when finished:")

    schema_lines = []

    while True:
        line = input()

        if line == "":
            break

        schema_lines.append(line)

    try:
        schema = json.loads("\n".join(schema_lines))
    except json.JSONDecodeError:
        print("Error: The schema is not valid JSON.")
        return

    try:
        print("\nTransforming input with Gemini...")
        result = transform(input_text, schema)
        print("Transformation complete!")
    except Exception as error:
        print("Transformation failed:", error)
        return

    # Handle missing or ambiguous information first.
    if result.get("status") == "error":
        print("\nTransformation error:")
        print(result.get("message") or "Required information is missing.")

        missing_fields = result.get("missing_fields", [])

        if missing_fields:
            print("Missing fields:", ", ".join(missing_fields))

        return

    if result.get("status") != "success":
        print("\nError: Unexpected transformation status.")
        return

    data = result.get("data")

    if not isinstance(data, dict):
        print("\nError: The transformation did not return a valid data object.")
        return

    # Validate the actual payload against the original schema.
    try:
        errors = validate_payload(data, schema)
    except Exception as error:
        print("Validation failed:", error)
        return

    if errors:
        print("\nThe generated data does not match the schema:")
        for error in errors:
            print("-", error)
        return

    print("\nValid output:")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
