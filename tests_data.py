"""
Tuple of test`s parameters

(method, endpoint, template, map_of_parameters, headers, json, status)

"""
param = (
    ("get", "books", "books_template.json", {}, None, None, 200),
    ("post", "books", "books_template.json", {}, None, None, 200),
    ("get", "users", "users_template.json", {}, None, None, 200),
    ("post", "users", "users_template.json", {}, None, None, 200),
    ("get", "user", "400_template.json", {}, None, None, 400),
    ("post", "user", "400_template.json", {}, None, None, 400),
    ("get", "user", "user_template.json", {"user_id": 2}, None, None, 200),
    ("post", "user", "user_template.json", {"user_id": 0}, None, None, 200),
    ("post", "user", "400_template.json", {"user_id": -1}, None, None, 400),
    ("get", "user", "400_template.json", {"user_id": -1}, None, None, 400),
    ("get", "user", "user_template.json", {"user_id": 0}, {"content-type": "application/json"}, {"user_id": 2}, 200),
    ("get", "book", "book_template.json", {"book_id": 0}, {"content-type": "application/json"}, {"book_id": 2}, 200),
    ("get", "user", "user_template.json", {}, {"content-type": "application/json"}, {"user_id": 2}, 200),
    ("post", "user", "user_template.json", {}, {"content-type": "application/json"}, {"user_id": 5}, 200),
    ("get", "book", "book_template.json", {}, {"content-type": "application/json"}, {"book_id": 0}, 200),
    ("post", "book", "book_template.json", {}, {"content-type": "application/json"}, {"book_id": 0}, 200),
    ("get", "book", "book_template.json", {"book_id": 0}, None, None, 200),
    ("get", "book", "400_template.json", {"book_id": -1}, None, None, 400),
    ("post", "book", "400_template.json", {"book_id": -1}, None, None, 400),
    ("get", "book/add", "400_template.json", {"book_name": "The Holy Bible", "amount": 1}, None, None, 400),
    ("get", "book/add", "400_template.json", {"book_author": "Suzanne Collins", "amount": 0}, None, None, 400),
)
