from src.validator import validate_payload


# Rules for the task data
task_schema = {
    "type": "object",
    "properties": {
        "task_name": {"type": "string"},
        "priority": {
            "type": "string",
            "enum": ["low", "medium", "high"]
        },
        "due_date": {"type": "string"}
    },
    "required": ["task_name", "priority", "due_date"]
}


def test_valid_task():
    task = {
        "task_name": "Finish assignment",
        "priority": "high",
        "due_date": "2026-10-20"
    }

    errors = validate_payload(task, task_schema)

    assert errors == []


def test_missing_field():
    task = {
        "task_name": "Finish assignment",
        "priority": "high"
    }

    errors = validate_payload(task, task_schema)

    assert len(errors) > 0


def test_invalid_priority():
    task = {
        "task_name": "Finish assignment",
        "priority": "urgent",
        "due_date": "2026-10-20"
    }

    errors = validate_payload(task, task_schema)

    assert len(errors) > 0

def test_invalid_priority_type():
    task = {
        "task_name": "Finish assignment",
        "priority": 123,
        "due_date": "2026-10-20"
    }

    errors = validate_payload(task, task_schema)

    assert len(errors) > 0

def test_valid_email():
    email_schema = {
        "type": "object",
        "properties": {
            "recipient": {"type": "string"},
            "subject": {"type": "string"},
            "body": {"type": "string"},
            "tone": {"type": "string"}
        },
        "required": ["recipient", "subject", "body", "tone"]
    }

    email = {
        "recipient": "rahul@awd.example.com",
        "subject": "Meeting Tomorrow",
        "body": "Confirming our meeting tomorrow.",
        "tone": "professional"
    }

    assert validate_payload(email, email_schema) == []


def test_valid_database_operation():
    database_schema = {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["insert", "update", "delete"]
            },
            "table": {"type": "string"},
            "data": {"type": "object"},
            "conditions": {"type": "object"}
        },
        "required": ["operation", "table", "data", "conditions"]
    }

    operation = {
        "operation": "insert",
        "table": "users",
        "data": {},
        "conditions": {}
    }

    assert validate_payload(operation, database_schema) == []
