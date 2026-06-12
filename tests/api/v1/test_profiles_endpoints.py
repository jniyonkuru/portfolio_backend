from app.schemas import ProfileCreate
from app.schemas.schemas import Address
from fastapi.encoders import jsonable_encoder


def _profile():
    return ProfileCreate(
        image_url="https://example.com/avatar.png",
        address=Address(country="Rwanda", city="Kigali", phone="+250788000000"),
    )


def test_profiles_list_200(client, apply_migrations, base_url):
    response = client.get(f"{base_url}/profiles/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_profile_get_404(client, apply_migrations, base_url):
    response = client.get(f"{base_url}/profiles/1000000")
    assert response.status_code == 404


def test_profile_create_401(client, apply_migrations, base_url):
    response = client.post(f"{base_url}/profiles/", json=jsonable_encoder(_profile()))
    assert response.status_code == 401


def test_profile_create_200(client, apply_migrations, base_url, auth_header):
    response = client.post(
        f"{base_url}/profiles/",
        json=jsonable_encoder(_profile()),
        headers={"Authorization": auth_header},
    )
    assert response.status_code == 200
    assert response.json()["address"]["city"] == "Kigali"


def test_profile_create_422(client, apply_migrations, base_url, auth_header):
    response = client.post(
        f"{base_url}/profiles/", json={}, headers={"Authorization": auth_header}
    )
    assert response.status_code == 422


def test_profile_create_409(client, apply_migrations, base_url, auth_header):
    headers = {"Authorization": auth_header}
    client.post(f"{base_url}/profiles/", json=jsonable_encoder(_profile()), headers=headers)
    second = client.post(
        f"{base_url}/profiles/", json=jsonable_encoder(_profile()), headers=headers
    )
    assert second.status_code == 409


def test_profile_get_by_id_200(client, apply_migrations, base_url, auth_header):
    created = client.post(
        f"{base_url}/profiles/",
        json=jsonable_encoder(_profile()),
        headers={"Authorization": auth_header},
    )
    profile_id = created.json()["id"]
    response = client.get(f"{base_url}/profiles/{profile_id}")
    assert response.status_code == 200
    assert response.json()["id"] == profile_id


def test_profile_update_401(client, apply_migrations, base_url, auth_header):
    created = client.post(
        f"{base_url}/profiles/",
        json=jsonable_encoder(_profile()),
        headers={"Authorization": auth_header},
    )
    profile_id = created.json()["id"]
    response = client.put(
        f"{base_url}/profiles/{profile_id}", json=jsonable_encoder(_profile())
    )
    assert response.status_code == 401


def test_profile_update_200(client, apply_migrations, base_url, auth_header):
    headers = {"Authorization": auth_header}
    created = client.post(
        f"{base_url}/profiles/", json=jsonable_encoder(_profile()), headers=headers
    )
    profile_id = created.json()["id"]
    response = client.put(
        f"{base_url}/profiles/{profile_id}",
        json={"address": {"country": "Kenya", "city": "Nairobi", "phone": "+254700000000"}},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["address"]["city"] == "Nairobi"


def test_profile_update_image_url(client, apply_migrations, base_url, auth_header):
    headers = {"Authorization": auth_header}
    created = client.post(
        f"{base_url}/profiles/", json=jsonable_encoder(_profile()), headers=headers
    )
    profile_id = created.json()["id"]
    response = client.put(
        f"{base_url}/profiles/{profile_id}",
        json={"image_url": "https://example.com/new.png"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["image_url"] == "https://example.com/new.png"


def test_profile_delete_200(client, apply_migrations, base_url, auth_header):
    headers = {"Authorization": auth_header}
    created = client.post(
        f"{base_url}/profiles/", json=jsonable_encoder(_profile()), headers=headers
    )
    profile_id = created.json()["id"]
    response = client.delete(f"{base_url}/profiles/{profile_id}", headers=headers)
    assert response.status_code == 200
