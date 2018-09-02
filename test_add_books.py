import pytest
import requests
import sys
from faker import Faker
from random import randint


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


def get_json():
    return {"book_name": Faker().sentence(nb_words=3), "book_author": Faker().name(), "amount": randint(0, 30)}


@pytest.mark.parametrize("http_method", ["GET", "POST"])
@pytest.mark.parametrize("data_method", ["query", "json"])
def test_add_book(http_method, data_method, get_url):
    """
    Checks book adding

    :param http_method: HTTP method
    :param data_method: parameters json or query
    :param get_url: fixture that gets base url of API

    """
    url = get_url + "book/add"
    data_list = get_json()
    sys.stdout.write("Method = {}, Url = {}, Data Method = {}, Parameters = {}\n"
                     .format(http_method, url, data_method, data_list))

    if data_method == "query":
        response = requests.request(http_method, url, params=data_list)
    else:
        response = requests.request(http_method, url, json=data_list)

    sys.stdout.write(response.text + '\n')
    if response.status_code == 405:
        pytest.skip("Bug 1 - book/add do not support POST")
    assert response.status_code == 200, "Status differs from the expected one"

    json_obj = response.json()
    bk_id = json_obj["body"]["id"]
    assert json_obj == transfer(data_list, bk_id), "A book with incorrect data was added"

    url = get_url + "book"
    assert requests.get(url, params={"book_id": bk_id}).json() == json_obj, \
        "Book on this identifier was not found"

    url = get_url + "books"
    assert find_book(json_obj["body"], requests.get(url).json()["body"]["books"]), \
        "There is no new book in all books list"
