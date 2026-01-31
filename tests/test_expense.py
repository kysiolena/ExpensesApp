def test_no_expenses_list(client, init_db, second_user_token):
    response = client.get(
        "/expense/",
        headers={"Authorization": f"Bearer {second_user_token}"},
    )

    assert response.status_code == 200
    assert response.json == []


def test_expenses_list(client, init_db, default_user_token):
    response = client.get(
        "/expense/",
        headers={"Authorization": f"Bearer {default_user_token}"},
    )

    assert response.status_code == 200
    assert len(response.json) > 0


def test_full_expense_flow(client, init_db, default_user_token):
    # Create
    create_expense_res = client.post(
        "/expense/",
        json={
            "title": "Test Expense",
            "description": "Test Expense Description",
            "amount": 100,
        },
        headers={"Authorization": f"Bearer {default_user_token}"},
    )

    assert create_expense_res.status_code == 201
    assert "id" in create_expense_res.json
    assert create_expense_res.json["title"] == "Test Expense"
    assert create_expense_res.json["description"] == "Test Expense Description"
    assert create_expense_res.json["amount"] == 100

    # Read
    create_expense_res_id = create_expense_res.json["id"]

    read_expense_res = client.get(
        f"/expense/{create_expense_res_id}",
        headers={"Authorization": f"Bearer {default_user_token}"},
    )

    assert read_expense_res.status_code == 200
    assert read_expense_res.json["id"] == create_expense_res_id
    assert read_expense_res.json["title"] == "Test Expense"
    assert read_expense_res.json["description"] == "Test Expense Description"
    assert read_expense_res.json["amount"] == 100

    # Update
    update_expense_res = client.patch(
        f"/expense/{create_expense_res_id}",
        json={
            "title": "Test Expense Updated",
        },
        headers={"Authorization": f"Bearer {default_user_token}"},
    )

    assert update_expense_res.status_code == 200
    assert update_expense_res.json["title"] == "Test Expense Updated"

    # Delete
    delete_expense_res = client.delete(
        f"/expense/{create_expense_res_id}",
        headers={"Authorization": f"Bearer {default_user_token}"},
    )

    assert delete_expense_res.status_code == 204
    assert delete_expense_res.json is None
