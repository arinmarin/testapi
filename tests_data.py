"""
Tuple of test`s parameters
(endpoint, template, map_of_parameters)
"""
import random

param = (
        ("books", "books_template.json", {}),
        ("books", "books_template.json", {"book_id": 0}),
        ("users", "users_template.json", {}),
        ("users", "users_template.json", {"user_id": 0}),
        ("users", "users_template.json", {"user_id": 3}),
        ("user", "user_template.json", {"user_id": 3}),
        ("user", "400_template.json", {"user_id": -1}),
        ("user", "400_template.json", {"user_id": "BB"}),
        ("user", "400_template.json", {}),
        ("book", "book_template.json", {"book_id": 0}),
        ("book", "400_template.json", {"book_id": -1}),
        ("book", "400_template.json", {"book_id": "AA"}),
        ("book", "400_template.json", {}),
        ("book/add", "book_add_template.json", {"book_name": "The Facebook",
                                                "book_author": "Suzi Collins",
                                                "amount": random.randint(0, 30)}),
        ("book/add", "400_template.json", {"book_name": "The Holy Bible", "amount": random.randint(0, 30)}),
        ("book/add", "400_template.json", {"book_author": "Suzanne Collins", "amount": random.randint(0, 30)}),
        ("book/add", "400_template.json", {"book_author": "Bobbie Collins", "amount": "fail"}),
        ("user/add", "user_add_template.json", {"user_name": "Bobby Brown"}),
        ("user/add", "400_template.json", {"user_name": ""}),
        ("user/add", "400_template.json", {"user_name": 55}),
        ("user/take_book", "200_template.json", {"user_id": 1, "book_id": 2}),
        ("user/take_book", "400_template.json", {"user_id": -1, "book_id": 2}),
        ("user/take_book", "400_template.json", {"user_id": 3, "book_id": -2}),
        ("user/take_book", "400_template.json", {"user_id": 3, "book_id": -2}),
        ("user/take_book", "400_template.json", {"user_id": "amamam", "book_id": 2}),
)
