def test_signup_requires_email_query_param(client):
    # Act
    response = client.post("/activities/Chess Club/signup")

    # Assert
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert isinstance(detail, list)
    assert detail[0]["loc"][-1] == "email"


def test_signup_rejects_get_method(client):
    # Act
    response = client.get("/activities/Chess Club/signup")

    # Assert
    assert response.status_code == 405
