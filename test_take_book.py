import requests
import json
import sys
import pytest
import random
from tests_data import baseUrl, take_book_param


@pytest.fixture(scope="module")
def books():
    diction = json.loads(requests.request("get", baseUrl + "books").text)["body"]["books"]
    ids = []
    for idd in diction:
        ids.append(idd["id"])
    return ids


@pytest.fixture(scope="module")
def users():
    diction = json.loads(requests.request("get", baseUrl + "users").text)["body"]["users"]
    ids = []
    for idd in diction:
        ids.append(idd["id"])
    return ids


def test_zero_amount_book_take(users):
    user_id = random.choice(users)

    par_dict = {"book_name": "Besi", "book_author": "Dostoevskiy Fedor", "amount": 0}
    request = requests.request("get", baseUrl + "book/add", params=par_dict)
    assert request.status_code == 200, "Book with 0 amount was not added"

    bk_id = json.loads(request.text)["body"]["id"]
    request = requests.request("get", baseUrl + "user/take_book", params={"user_id": user_id, "book_id": bk_id})
    if request.status_code != 406:
        sys.stderr.write("Status is incorrect\n")

    request = requests.request("get", baseUrl + "user", params={"user_id": user_id})
    user_books = json.loads(request.text)["body"]["taken_books_ids"]
    for b in user_books:
        if b == bk_id:
            assert False, "User took a book that is forbidden to take"


def test_more_than_max(users):
    max_count = 3
    user_id = random.choice(users)

    book_list = json.loads(requests.request("get", baseUrl + "user", params={"user_id": user_id}).text)["body"][
        "taken_books_ids"]
    for i in range(max_count):
        requests.request("get", baseUrl + "user/take_book", params={"user_id": user_id, "book_id": i})
        i += 1
        book_list = json.loads(requests.request("get", baseUrl + "user", params={"user_id": user_id}).text)["body"][
            "taken_books_ids"]

    if len(book_list) > max_count:
        assert False, "User took more than {} books".format(max_count)


def test_idential_books(users, books):
    user_id = random.choice(users)
    book_id = random.choice(books)

    requests.request("get", baseUrl + "user/take_book", params={"user_id": user_id, "book_id": book_id})
    requests.request("get", baseUrl + "user/take_book", params={"user_id": user_id, "book_id": book_id})

    book_list = json.loads(requests.request("get", baseUrl + "user", params={"user_id": user_id}).text)["body"][
        "taken_books_ids"]
    if book_list.count(book_id) > 1:
        assert False, "User took idential books"


def test_take_zero_books(users):

    par_dict = {"book_name": "Goi", "book_author": "Noize MC", "amount": 0}
    request = requests.request("get", baseUrl + "book/add", params=par_dict)
    assert request.status_code == 200, "Book with 0 amount was not added"

    user_id = random.choice(users)
    book_id = json.loads(request.text)["body"]["id"]
    request = requests.request("get", baseUrl + "user/take_book", params={"user_id": user_id, "book_id": book_id})
    assert request.status_code != 200, "Success by take book with amount is 0"

    book_list = json.loads(requests.request("get", baseUrl + "user", params={"user_id": user_id}).text)["body"][
        "taken_books_ids"]
    if book_id in book_list:
        assert False, "Amount 0 book took"

def amount_of_book(id):
    return json.loads(requests.request("get", baseUrl + "book", params={"book_id": id}).text)["body"]["amount"]


@pytest.mark.parametrize("method, is_need_param, is_need_json", take_book_param)
def test_take_book(method, is_need_param, is_need_json, books, users):
    map_of_argument = None
    my_json = None
    header = None

    map_user = random.choice(users)
    map_book = random.choice(books)

    json_user = random.choice(users)
    json_book = random.choice(books)

    if is_need_param:
        map_of_argument = {"user_id": map_user, "book_id": map_book}
        map_am = amount_of_book(map_book)
    if is_need_json:
        header = {"content-type": "application/json"}
        my_json = {"user_id": json_user, "book_id": json_book}
        json_am = amount_of_book(json_book)

    request = requests.request(method, baseUrl + "user/take_book", params=map_of_argument, headers=header, json=my_json)
    assert request.status_code == 200, "Return status is incorrect"

    if is_need_json:
        assert amount_of_book(json_book) + 1 == json_am, "Amount of book does not change"
        user_id = json_user
        book_id = json_book
    else:
        assert amount_of_book(map_book) + 1 == map_am, "Amount of book does not change"
        user_id = map_user
        book_id = map_book

    book_list = json.loads(requests.request("get", baseUrl + "user", params={"user_id": user_id}).text)["body"][
        "taken_books_ids"]
    if book_id not in book_list:
        assert False, "There is no book by user"
