def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.json
    assert response.json["message"] == "Hello, I'm your Expense tracking App!"


def test_not_found(client):
    response = client.get("/abc")

    assert response.status_code == 404
    assert "error" in response.json
    assert response.json["error"] == "We couldn't find that"
