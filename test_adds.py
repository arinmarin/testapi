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


@pytest.mark.parametrize("method, map_of_argument, header, my_json, status", add_book_param)
def test_add_book(method, map_of_argument, header, my_json, status):
    url = baseUrl + "book/add"
    sys.stdout.write("Method = {}, Url = {}, Parameters = {}, Headers = {}, Json = {}, Status = {}\n"
                     .format(method, url, map_of_argument, header, my_json, status))
    request = requests.request(method, url, params=map_of_argument, headers=header, json=my_json)
    text = request.text
    sys.stdout.write(text + '\n')
    assert request.status_code == status

    json_obj = json.loads(text)
    id = json_obj["body"]["id"]
    assert json_obj == transfer(map_of_argument if (my_json is None) else my_json, id)

    url = baseUrl + "book"
    assert json.loads(requests.request("get", url, params={"book_id": id}).text) == json_obj
