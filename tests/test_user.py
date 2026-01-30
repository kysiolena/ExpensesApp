def test_valid_registration(client, init_db):
    response = client.post(
        "/user/",
        json={
            "username": "test",
            "first_name": "testF",
            "last_name": "testL",
            "email": "test@email.com",
            "phone": "5555555555555",
            "password": "test_password",
        },
    )

    assert response.status_code == 201
    assert "id" in response.json
    assert "username" in response.json
    assert "first_name" in response.json
    assert "last_name" in response.json
    assert "email" in response.json
    assert "phone" in response.json
    assert "password" not in response.json


def test_invalid_password_registration(client, init_db):
    response = client.post(
        "/user/",
        json={
            "username": "test",
            "first_name": "testF",
            "last_name": "testL",
            "email": "test@email.com",
            "phone": "5555555555555",
            "password": "123",
        },
    )

    assert response.status_code == 422
    assert "password" in response.json
    assert response.json["password"] == ["Shorter than minimum length 8."]


def test_duplicate_registration(client, init_db):
    client.post(
        "/user/",
        json={
            "username": "test",
            "first_name": "testF",
            "last_name": "testL",
            "email": "test@email.com",
            "phone": "5555555555555",
            "password": "123123123123",
        },
    )

    response = client.post(
        "/user/",
        json={
            "username": "test",
            "first_name": "testF",
            "last_name": "testL",
            "email": "test@email.com",
            "phone": "5555555555555",
            "password": "123123123123",
        },
    )

    assert response.status_code == 400
    assert "error" in response.json
    assert response.json["error"] == "Duplicate data insertion."


def test_valid_login(client, init_db):
    response = client.post(
        "/user/login",
        json={
            "email": "mary@world.com",
            "password": "strong_password",
        },
    )

    assert response.status_code == 200
    assert "token" in response.json


def test_invalid_login(client, init_db):
    response = client.post(
        "/user/login",
        json={
            "email": "mary@world.com",
            "password": "wrong_password",
        },
    )

    assert response.status_code == 401
    assert "error" in response.json
    assert response.json["error"] == "Incorrect email or password"
