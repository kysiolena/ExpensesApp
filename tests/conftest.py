import os

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.db import db
from app.expense.models import Expense
from app.user.models import User


@pytest.fixture(scope="module")
def client():
    os.environ["CONFIG_TYPE"] = "app.config.TestingConfig"

    app = create_app()

    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture(scope="module")
def user():
    return User(
        username="HelloWorld",
        email="hello@world.com",
        phone="012345678910",
        first_name="Hello",
        last_name="World",
        password="strong_password",
    )


@pytest.fixture(scope="module")
def init_db(client):
    db.create_all()

    # Create Users
    default_user = User(
        username="MaRy",
        email="mary@world.com",
        phone="111111111111",
        first_name="Ma",
        last_name="Ry",
        password=generate_password_hash("strong_password"),
    )

    second_user = User(
        username="PatrIck",
        email="patrick@world.com",
        phone="222222222222",
        first_name="Patr",
        last_name="Ick",
        password=generate_password_hash("strong_password"),
    )

    db.session.add(default_user)
    db.session.add(second_user)

    db.session.commit()

    # Create Expenses
    expense_1 = Expense(
        title="Expense 1",
        amount=7,
        description="Expense 1 description",
        user_id=default_user.id,
    )
    expense_2 = Expense(
        title="Expense 2",
        amount=17,
        description="Expense 2 description",
        user_id=default_user.id,
    )
    expense_3 = Expense(
        title="Expense 3",
        amount=77,
        description="Expense 3 description",
        user_id=default_user.id,
    )

    db.session.add_all([expense_1, expense_2, expense_3])
    db.session.commit()

    yield

    db.drop_all()


@pytest.fixture(scope="module")
def default_user_token(client):
    response = client.post(
        "/user/login",
        json={
            "email": "mary@world.com",
            "password": "strong_password",
        },
    )

    yield response.json["token"]


@pytest.fixture(scope="module")
def second_user_token(client):
    response = client.post(
        "/user/login",
        json={
            "email": "patrick@world.com",
            "password": "strong_password",
        },
    )

    yield response.json["token"]
