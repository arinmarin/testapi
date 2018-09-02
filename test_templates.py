import json
import sys
import jsonschema
import pytest
import requests
from tests_data import *


def is_validate(json_obj, schema):
    try:
        jsonschema.validate(json_obj, schema)
        return True
    except jsonschema.exceptions.ValidationError as ve:
        sys.stderr.write(str(ve) + "\n")
        return False


@pytest.mark.parametrize("method, url, template, map_of_argument, header, my_json, status", param)
def test_template_valid(method, url, template, map_of_argument, header, my_json, status, get_url):
    url = get_url + url
    sys.stdout.write("Method = {}, Url = {}, Template = {}, Parameters = {}, Headers = {}, Json = {}, Status = {}\n"\
                     .format(method, url, template, map_of_argument, header, my_json, status))
    template = "templates/" + template
    with open(template, 'r') as f:
        schema_data = f.read()
    schema = json.loads(schema_data)

    request = requests.request(method, url, params=map_of_argument, headers=header, json=my_json)
    text = request.text
    request.json()
    sys.stdout.write(text + '\n')
    assert request.status_code == status

    json_obj = json.loads(text)
    assert is_validate(json_obj, schema), "Schema {} is not valid\n".format(template)
