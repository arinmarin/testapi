import pytest
import requests
import sys

from faker import Faker


def find_user(json_obj, text):
    for t in text:
        if t["id"] == json_obj["id"] and \
                t["name"] == json_obj["name"] and \
                t["taken_books_ids"] == json_obj["taken_books_ids"]:
            return True
    return False


def get_json():
    return {"user_name": Faker().name()}


@pytest.mark.parametrize("http_method", ["GET", "POST"])
@pytest.mark.parametrize("data_method", ["query", "json"])
def test_add_user(http_method, data_method, get_url):
    """
    Checks user adding

    :param http_method: HTTP method
    :param data_method: parameters json or query
    :param get_url: fixture that gets base url of API

    """
    url = get_url + "user/add"
    data_list = get_json()
    sys.stdout.write("Method = {}, Url = {}, Data Method = {}, Parameters = {}\n"
                     .format(http_method, url, data_method, data_list))

    if data_method == "query":
        response = requests.request(http_method, url, params=data_list)
    else:
        response = requests.request(http_method, url, json=data_list)

    sys.stdout.write(response.text + '\n')
    assert response.status_code == 200, "Status differs from the expected one"

    json_obj = response.json()
    assert json_obj["body"]["name"] == data_list["user_name"], "A user with incorrect data was added"

    assert requests.request("get", get_url + "user", params={"user_id": json_obj["body"]["id"]}).json() == json_obj, \
        "User on this identifier was not found"

    assert find_user(json_obj["body"], requests.get(get_url + "users").json()["body"]["users"]), \
        "There is no new user in all users list"
