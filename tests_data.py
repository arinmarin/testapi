"""Base url of API"""
baseUrl = 'http://yoshilyosha.pythonanywhere.com/api/v1/'


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

"""
Tuple of tests for adding books into db

(method, map_of_parameters, headers, json)

"""
add_book_param = (
    ("get", {"book_name": "The Little Prince", "book_author": "Antoine de Saint-Exupery", "amount": 1}, None, None),
    ("get", {"book_name": "The Holy Bible", "book_author": "", "amount": 2}, None, None),
    ("post", {"book_name": "The Little Prince", "book_author": "Antoine de Saint-Exupery", "amount": 3}, None, None),
    ("get", None, {"content-type": "application/json"}, {"book_name": "The Little Prince", "book_author": "Antoine de Saint-Exupery", "amount": 2}),
    ("post", None, {"content-type": "application/json"}, {"book_name": "The Little Prince", "book_author": "Antoine de Saint-Exupery", "amount": 6}),
    ("post", {"book_name": "The Hunger Games", "book_author": "Suzanne Collins", "amount": 2}, {"content-type": "application/json"}, {"book_name": "The Little Prince", "book_author": "Antoine de Saint-Exupery", "amount": 2}),
    ("get", {"book_name": "The Hunger Games", "book_author": "Suzanne Collins", "amount": 2}, {"content-type": "application/json"}, {"book_name": "The Little Prince", "book_author": "Antoine de Saint-Exupery", "amount": 2}),
    ("get", {"book_name": "", "book_author": "Suzanne Collins", "amount": 0}, None, None),
)

"""
Tuple of tests for adding users into db

(method, map_of_parameters, headers, json)

"""
add_user_param = (
    ("get", {"user_name": "Hillary Clinton"}, None, None),
    ("post", {"user_name": "Mary Rubets"}, None, None),
    ("get", {"user_name": "Monica Fush"}, {"content-type": "application/json"}, {"user_name": "Monica Tush"}),
    ("post", {"user_name": "Lucy Fush"}, {"content-type": "application/json"}, {"user_name": "Lucy Tush"}),
    ("get", None, {"content-type": "application/json"}, {"user_name": "Mandy Timures"}),
    ("post", None, {"content-type": "application/json"}, {"user_name": "Hidy Timures"}),
    ("get", {"user_name": ""}, None, None),
    ("get", None, {"content-type": "application/json"}, {"user_name": ""}),
)

"""
Tuple of tests for taking book

(method, is_need_param, is_need_json)

"""
take_book_param = (
    ("get", True, False),
    ("post", True, False),
    ("get", False, True),
    ("post", False, True),
    ("get", True, True),
    ("post", True, True),
)
