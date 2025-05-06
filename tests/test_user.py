def test_signup_user_success(client, db_session):
    # given
    payload = {
        "username": "test1",
        "email": "test1@test.com",
        "password": "test1"
    }

    # when
    response = client.post("/api/v1/users/register", json=payload)

    # then
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "test1"
    assert data["email"] == "test1@test.com"
    assert "password" not in data

def test_signup_user_duplicate_username(client, db_session):
    # given
    client.post("/api/v1/users/register", json={
        "username": "test1",
        "email": "test1@test.com",
        "password": "test1"
    })

    # when
    response = client.post("/api/v1/users/register", json={
        "username": "test1",
        "email": "another@test.com",
        "password": "another"
    })

    # then
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already taken"


def test_signup_user_duplicate_email(client, db_session):
    # given
    client.post("/api/v1/users/register", json={
        "username": "test1",
        "email": "test1@test.com",
        "password": "test1"
    })

    # when
    response = client.post("/api/v1/users/register", json={
        "username": "another",
        "email": "test1@test.com",
        "password": "test1"
    })

    # then
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already taken"


