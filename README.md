# Adaptive Input Transformation Agent

## Overview

The Adaptive Input Transformation Agent converts structured or unstructured user input into JSON that matches a receiving agent's input schema.

It uses Gemini to extract relevant information, map fields, normalize values, and identify missing information. Python's `jsonschema` library validates the generated payload before it is displayed.

## Features

- Accepts natural-language input and a target JSON Schema at runtime.
- Dynamically adapts to different receiving-agent schemas.
- Extracts, renames, and reshapes relevant information.
- Supports nested JSON objects and different field types.
- Identifies missing or ambiguous required information and returns a structured error.
- Validates required fields, data types, and allowed enum values.
- Does not execute consequential actions such as sending emails or modifying a database.

## Architecture

1. **Input collection (`main.py`)** — receives the user's message and target JSON Schema.
2. **Transformation (`transformer.py`)** — sends the input and schema to Gemini and parses the JSON response.
3. **Error handling (`main.py`)** — displays a transformation error if required information is missing or ambiguous.
4. **Validation (`validator.py`)** — validates successful payloads against the original schema.
5. **Output** — displays either a validation error or the resulting JSON.

## Technology Stack

- Python
- Google Gemini API (`google-genai`)
- `jsonschema`
- `python-dotenv`
- `pytest`

## Project Structure

```text
Input-Adapter-Agent/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── transformer.py
│   └── validator.py
├── tests/
│   └── test_validator.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Gemini API key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key
```

Never commit your actual API key to version control.

### 4. Run the application

```bash
python -m src.main
```

Enter a message, then paste the target JSON Schema. Submit a blank line to finish entering the schema.

## Testing

Run the tests with:

```bash
python -m pytest -v
```

The current test suite covers:

- Valid Task payloads
- Missing required Task fields
- Invalid Task priority values
- Invalid Task priority types
- Valid Email payloads
- Valid Database operation payloads

A Calendar schema was also tested manually without adding Calendar-specific transformation logic.

## Example Agent Contracts

### Task

Fields include `task_name`, `assigned_to`, `priority`, and `due_date`.

### Email

Fields include `recipient`, `subject`, `body`, and `tone`.

### Database

Fields include `operation`, `table`, `data`, and `conditions`.

### Calendar

A runtime-supplied schema can define `event_name`, `date`, `start_time`, and `end_time`.

## Validation and Error Handling

The application checks that the supplied schema is valid and that successful transformation output satisfies its requirements.

Missing required information can produce a structured error with missing field names. Invalid payloads are rejected before the application displays them as valid.

## Assumptions and Limitations

- The quality and consistency of extraction depend partly on the Gemini model's response.
- The JSON Schema validator checks structural validity, not whether every extracted value is factually correct.
- Generic object fields, such as the Database schema's `data` field, may accept empty objects if the supplied schema does not define their internal fields.
- Date formats and other semantic constraints require appropriate schema rules and format validation.
- The application does not send emails, execute database operations, or perform other consequential actions.
- The API key and a working network connection are required to use Gemini.

## Future Improvements

- Add deterministic checks for omitted or fabricated information.
- Expand tests for missing information across different agent types.
- Add date-format validation and stronger semantic checks.
- Improve error reporting and support follow-up clarification.
