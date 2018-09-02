import pytest
import requests
from faker import Faker


@pytest.fixture(scope="module")
def books(get_url):
    """Fixture returned a list of all books ids
    """
    requests.get(get_url + "book/add", params=Faker().sentence(nb_words=3))
    diction = requests.get(get_url + "books").json()["body"]["books"]
    ids = []
    for idd in diction:
        ids.append(idd["id"])
    return ids


@pytest.fixture(scope="module")
def users(get_url):
    """Fixture returned a list of all users ids
    """
    requests.get(get_url + "user/add", params=Faker().name())
    diction = requests.get(get_url + "users").json()["body"]["users"]
    ids = []
    for idd in diction:
        ids.append(idd["id"])
    return ids


@pytest.fixture(scope="session")
def get_url():
    return 'http://yoshilyosha.pythonanywhere.com/api/v1/'
