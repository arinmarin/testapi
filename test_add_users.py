import pytest
import json
import requests
import sys
from tests_data import *


def find_user(json_obj, text):
    for t in text:
        if t["id"] == json_obj["id"] and \
                t["name"] == json_obj["name"] and \
                t["taken_books_ids"] == json_obj["taken_books_ids"]:
            return True
    return False


@pytest.mark.parametrize("method, map_of_argument, header, my_json", add_user_param)
def test_add_user(method, map_of_argument, header, my_json):
    url = baseUrl + "user/add"
    sys.stdout.write("Method = {}, Url = {}, Parameters = {}, Headers = {}, Json = {}\n"
                     .format(method, url, map_of_argument, header, my_json))
    request = requests.request(method, url, params=map_of_argument, headers=header, json=my_json)
    text = request.text
    sys.stdout.write(text + '\n')
    assert request.status_code == 200, "Status differs from the expected one"

    json_obj = json.loads(text)
    assert json_obj["body"]["name"] == map_of_argument["user_name"] if (my_json is None) else my_json["user_name"], \
        "A user with incorrect data was added"

    url = baseUrl + "user"
    assert json.loads(requests.request("get", url, params={"user_id": json_obj["body"]["id"]}).text) == json_obj, \
        "User on this identifier was not found"

    url = baseUrl + "users"
    assert find_user(json_obj["body"], json.loads(requests.request("get", url).text)["body"]["users"]), \
        "There is no new user in all users list"
