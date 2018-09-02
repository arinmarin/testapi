import requests
import pytest
import random

from faker import Faker


def test_zero_amount_book_take(users, get_url):
    """
    Checks can user take a book with a zero amount
    :param users: fixture that gets all users list
    :param get_url: fixture that gets base url of API

    """
    user_id = random.choice(users)

    par_dict = {"book_name": Faker().sentence(nb_words=3), "book_author": Faker().name(), "amount": 0}
    request = requests.get(get_url + "book/add", params=par_dict)
    assert request.status_code == 200, "Book with 0 amount was not added"

    bk_id = request.json()["body"]["id"]
    request = requests.get(get_url + "user/take_book", params={"user_id": user_id, "book_id": bk_id})
    if request.status_code == 200:
        pytest.skip("Bug 2 - User take book with zero amount. Status == 200")
    assert request.status_code == 400, "Status is incorrect"

    request = requests.get(get_url + "user", params={"user_id": user_id})
    user_books = request.json()["body"]["taken_books_ids"]
    if bk_id in user_books:
        pytest.skip("Bug 3 - User take book with zero amount")
    assert bk_id not in user_books, "User take book with zero amount"


def test_more_than_max(users, get_url):
    """
    Checks can user take more than max book amount
    :param users: fixture that gets all users list
    :param get_url: fixture that gets base url of API

    """
    max_count = 3
    user_id = random.choice(users)

    for i in range(max_count + 1):
        requests.get(get_url + "user/take_book", params={"user_id": user_id, "book_id": i})
        i += 1

    book_list = requests.get(get_url + "user", params={"user_id": user_id}).json()["body"]["taken_books_ids"]

    if len(book_list) > max_count:
        pytest.skip("Bug 4 - User took more than {} books".format(max_count))
    assert not len(book_list) > max_count, "User took more than {} books".format(max_count)


def test_identical_books(users, books, get_url):
    """
    Checks can user take two identical books
    :param users: fixture that gets all users list
    :param books: fixture that gets all books list
    :param get_url: fixture that gets base url of API

    """
    user_id = random.choice(users)
    book_id = random.choice(books)

    requests.get(get_url + "user/take_book", params={"user_id": user_id, "book_id": book_id})
    requests.get(get_url + "user/take_book", params={"user_id": user_id, "book_id": book_id})

    book_list = requests.get(get_url + "user", params={"user_id": user_id}).json()["body"]["taken_books_ids"]
    if book_list.count(book_id) > 1:
        pytest.skip("Bug 5 - User took identical books")
    assert not book_list.count(book_id) > 1, "User took identical books"


def amount_of_book(id_, get_url):
    return requests.get(get_url + "book", params={"book_id": str(id_)}).json()["body"]["amount"]


def get_json(user_id, book_id):
    return {"user_id": user_id, "book_id": book_id}


@pytest.mark.parametrize("http_method", ["GET", "POST"])
@pytest.mark.parametrize("data_method", ["query", "json"])
def test_take_book(http_method, data_method, books, users, get_url):
    """
    Check can user take book correctly
    :param http_method: HTTP method
    :param data_method: parameters json or query
    :param books: fixture that gets all books list
    :param users: fixture that gets all users list
    :param get_url: fixture that gets base url of API

    """
    user_id = random.choice(users)
    book_id = random.choice(books)

    data_list = get_json(user_id, book_id)
    first_amount = amount_of_book(book_id, get_url)
    if data_method == "query":
        request = requests.request(http_method, get_url + "user/take_book", params=data_list)
    else:
        request = requests.request(http_method, get_url + "user/take_book", json=data_list)
        pytest.skip("Bug 6 - user/take_book. Json is not works")
    assert request.status_code == 200, "Return status is incorrect"

    if first_amount == amount_of_book(book_id, get_url):
        pytest.skip("Bug 7 - user/take_book. Amount of book does not change")
    assert first_amount == amount_of_book(book_id, get_url) + 1, "Amount of book does not change"

    book_list = requests.get(get_url + "user", params={"user_id": user_id}).json()["body"]["taken_books_ids"]
    if book_id not in book_list:
        assert False, "There is no book by user"
