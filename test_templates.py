import json
import sys
import jsonschema
import pytest
import requests


def is_validate(json_obj, schema):
    try:
        jsonschema.validate(json_obj, schema)
        return True
    except jsonschema.exceptions.ValidationError as ve:
        sys.stderr.write(str(ve) + "\n")
        return False


@pytest.mark.parametrize("url,template", [
    ("http://yoshilyosha.pythonanywhere.com/api/v1/books", "templates/books_template.json"),
    ("http://yoshilyosha.pythonanywhere.com/api/v1/users", "templates/users_template.json"),
])
def test_template_valid(url, template):
    with open(template, 'r') as f:
        schema_data = f.read()
    schema = json.loads(schema_data)

    json_obj = json.loads(requests.get(url).text)

    assert is_validate(json_obj, schema), "Schema {} is not valid".format(template)
