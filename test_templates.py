import re
import sys
import jsonschema
import pytest
import json
import requests

from tests_data import param


def is_need_to_skip(http_method, data_method, url, params):
    msg = ''
    if http_method == "POST" and url == "users":
        msg = 'Bug 8 - users do not support POST'
    if data_method == "json" and url == "user" and not re.fullmatch(r"[0-9]+", str(params.get("user_id"))):
        msg = 'Bug 9 - user and json and "user_id" and not positive number'
    if url == "book" and not re.fullmatch(r"[0-9]+", str(params.get("book_id"))):
        msg = 'Bug 10 - book and not positive number'
    if url == "book/add" and http_method == "POST":
        msg = 'Bug 1 - book/add do not support POST'
    if url == "user/add" and not re.fullmatch(r"[A-Z][a-z]+\s[A-Z][a-z]+", str(params.get("user_name"))):
        msg = "Bug 11 - user/add may add not only named words"
    if url == "user/take_book" and data_method == "json":
        msg = "Bug 6 - user/take_book. Json is not works"
    return msg


def is_validate(json_obj, schema):
    try:
        jsonschema.validate(json_obj, schema)
        return True
    except jsonschema.exceptions.ValidationError as ve:
        sys.stderr.write(str(ve) + "\n")
        return False


@pytest.mark.parametrize("http_method", ["GET", "POST"])
@pytest.mark.parametrize("data_method", ["query", "json"])
@pytest.mark.parametrize("url, template, map_of_argument", param)
def test_template_valid(http_method, data_method, url, template, map_of_argument, get_url, clear_base):
    """
    Check if output json answer is correct
    :param http_method: HTTP method
    :param data_method: parameters json or query
    :param url:
    :param template: json schema template for validation
    :param map_of_argument: list of parameters for request
    :param get_url: fixture that gets base url of API

    """
    sys.stdout.write("Method = {}, Data Type = {}, Url = {}, Template = {}, Parameters = {}\n"
                     .format(http_method, data_method, get_url + url, template, map_of_argument))

    with open("templates/" + template, 'r') as f:
        schema_data = f.read()
    schema = json.loads(schema_data)

    msg = is_need_to_skip(http_method, data_method, url, map_of_argument)
    if msg:
        pytest.skip(msg)

    if data_method == "query":
        response = requests.request(http_method, get_url + url, params=map_of_argument)
    else:
        response = requests.request(http_method, get_url + url, json=map_of_argument)

    sys.stdout.write(response.text + '\n')
    assert response.status_code == (200 if template != "400_template.json" else 400)

    assert is_validate(response.json(), schema), "Schema {} is not valid\n".format(template)
