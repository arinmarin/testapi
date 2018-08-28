import requests
import json
import sys
from tests_data import baseUrl


def test_zero_amount_book_take():
    user_id = 0

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


def test_more_than_three():
    max_count = 3
    user_id = 0

    book_list = json.loads(requests.request("get", baseUrl + "user", params={"user_id": user_id}).text)["body"][
        "taken_books_ids"]
    for i in range(max_count):
        requests.request("get", baseUrl + "user/take_book", params={"user_id": user_id, "book_id": i})
        i += 1
        book_list = json.loads(requests.request("get", baseUrl + "user", params={"user_id": user_id}).text)["body"][
            "taken_books_ids"]

    if len(book_list) > max_count:
        assert False, "User took more than {} books".format(max_count)


def test_idential_books():
    user_id = 0
    book_id = 1

    requests.request("get", baseUrl + "user/take_book", params={"user_id": user_id, "book_id": book_id})
    requests.request("get", baseUrl + "user/take_book", params={"user_id": user_id, "book_id": book_id})

    book_list = json.loads(requests.request("get", baseUrl + "user", params={"user_id": user_id}).text)["body"][
        "taken_books_ids"]
    if book_list.count(book_id) > 1:
        assert False, "User took idential books"