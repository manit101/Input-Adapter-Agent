from jsonschema import Draft202012Validator


def validate_payload(data, schema):
    Draft202012Validator.check_schema(schema)

    validator = Draft202012Validator(schema)
    errors = []

    for error in validator.iter_errors(data):
        errors.append(error.message)

    return errors
