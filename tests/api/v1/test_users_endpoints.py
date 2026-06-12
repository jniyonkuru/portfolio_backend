PASSWORD = "Str0ngP@ssword"


def _new_user(**overrides):
    user = {
        "user_name": "alice",
        "password": PASSWORD,
        "role": "admin",
        "email": "alice@gmail.com",
        "first_name": "alice",
        "last_name": "doe",
    }
    user.update(overrides)
    return user


def test_create_user_200(client, apply_migrations, base_url):
    response = client.post(f"{base_url}/users/create", json=_new_user())
    assert response.status_code == 200
    body = response.json()
    assert body["user_name"] == "alice"
    assert body["email"] == "alice@gmail.com"
    assert "password" not in body


def test_create_user_422(client, apply_migrations, base_url):
    response = client.post(f"{base_url}/users/create", json={})
    assert response.status_code == 422


def test_create_user_409(client, apply_migrations, base_url):
    client.post(f"{base_url}/users/create", json=_new_user())
    response = client.post(f"{base_url}/users/create", json=_new_user())
    assert response.status_code == 409


def test_token_200(client, apply_migrations, base_url):
    client.post(f"{base_url}/users/create", json=_new_user())
    response = client.post(
        f"{base_url}/users/token",
        data={"username": "alice", "password": PASSWORD},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_token_wrong_password_400(client, apply_migrations, base_url):
    client.post(f"{base_url}/users/create", json=_new_user())
    response = client.post(
        f"{base_url}/users/token",
        data={"username": "alice", "password": "wrong-password"},
    )
    assert response.status_code == 400


def test_token_unknown_user_400(client, apply_migrations, base_url):
    response = client.post(
        f"{base_url}/users/token",
        data={"username": "ghost", "password": PASSWORD},
    )
    assert response.status_code == 400


def test_me_401_without_token(client, apply_migrations, base_url):
    response = client.get(f"{base_url}/users/me")
    assert response.status_code == 401


def test_me_200(client, apply_migrations, base_url, auth_header):
    response = client.get(f"{base_url}/users/me", headers={"Authorization": auth_header})
    assert response.status_code == 200
    assert response.json()["user_name"] == "jniyonkuru"


def test_me_invalid_token_401(client, apply_migrations, base_url):
    response = client.get(
        f"{base_url}/users/me", headers={"Authorization": "Bearer not-a-real-token"}
    )
    assert response.status_code == 401
