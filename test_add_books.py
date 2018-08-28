import pytest
import json
import requests
import sys
from tests_data import *


def transfer(input_args, id_get):
    return {"body": {"amount": input_args["amount"],
                     "author": input_args["book_author"],
                     "name": input_args["book_name"],
                     "id": id_get}, "status": 200}


def find_book(json_obj, text):
    for t in text:
        if t["id"] == json_obj["id"] and \
                t["amount"] == json_obj["amount"] and \
                t["author"] == json_obj["author"] and \
                t["name"] == json_obj["name"]:
            return True
    return False


@pytest.mark.parametrize("method, map_of_argument, header, my_json", add_book_param)
def test_add_book(method, map_of_argument, header, my_json):
    url = baseUrl + "book/add"
    sys.stdout.write("Method = {}, Url = {}, Parameters = {}, Headers = {}, Json = {}\n"
                     .format(method, url, map_of_argument, header, my_json))
    request = requests.request(method, url, params=map_of_argument, headers=header, json=my_json)
    text = request.text
    sys.stdout.write(text + '\n')
    assert request.status_code == 200, "Status differs from the expected one"

    json_obj = json.loads(text)
    bk_id = json_obj["body"]["id"]
    assert json_obj == transfer(map_of_argument if (my_json is None) else my_json, bk_id), \
        "A book with incorrect data was added"

    url = baseUrl + "book"
    assert json.loads(requests.request("get", url, params={"book_id": bk_id}).text) == json_obj, \
        "Book on this identifier was not found"

    url = baseUrl + "books"
    assert find_book(json_obj["body"], json.loads(requests.request("get", url).text)["body"]["books"]), \
        "There is no new book in all books list"
