import pytest

from app import app
from app.services.images_service import ImagesService


class _FakeImageService:
    """Stands in for ImagesService so tests never hit Cloudinary."""

    def upload_image(self, image):
        return {
            "url": "https://res.cloudinary.com/demo/image/upload/test.png",
            "public_id": "test-public-id",
        }


@pytest.fixture(scope="function")
def mock_image_service():
    app.dependency_overrides[ImagesService] = lambda: _FakeImageService()
    yield
    app.dependency_overrides.pop(ImagesService, None)


def _project_form(**overrides):
    data = {
        "github_url": "https://github.com/jacques/portfolio",
        "description": "A portfolio API",
        "title": "Portfolio API",
        "tags": ["python", "fastapi"],
    }
    data.update(overrides)
    return data


def _image_file():
    return {"image": ("img.png", b"\x89PNG\r\n\x1a\nfakebytes", "image/png")}


def test_projects_list_200(client, apply_migrations, base_url):
    response = client.get(f"{base_url}/projects/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_project_get_404(client, apply_migrations, base_url):
    response = client.get(f"{base_url}/projects/1000000")
    assert response.status_code == 404


def test_project_create_401(client, apply_migrations, base_url, mock_image_service):
    response = client.post(
        f"{base_url}/projects/", data=_project_form(), files=_image_file()
    )
    assert response.status_code == 401


def test_project_create_200(
    client, apply_migrations, base_url, auth_header, mock_image_service
):
    response = client.post(
        f"{base_url}/projects/",
        data=_project_form(),
        files=_image_file(),
        headers={"Authorization": auth_header},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Portfolio API"
    assert body["image"] == "https://res.cloudinary.com/demo/image/upload/test.png"


def test_project_create_422(
    client, apply_migrations, base_url, auth_header, mock_image_service
):
    response = client.post(
        f"{base_url}/projects/", data={}, headers={"Authorization": auth_header}
    )
    assert response.status_code == 422


def test_project_create_409(
    client, apply_migrations, base_url, auth_header, mock_image_service
):
    headers = {"Authorization": auth_header}
    client.post(
        f"{base_url}/projects/", data=_project_form(), files=_image_file(), headers=headers
    )
    second = client.post(
        f"{base_url}/projects/", data=_project_form(), files=_image_file(), headers=headers
    )
    assert second.status_code == 409


def test_project_get_by_id_200(
    client, apply_migrations, base_url, auth_header, mock_image_service
):
    created = client.post(
        f"{base_url}/projects/",
        data=_project_form(),
        files=_image_file(),
        headers={"Authorization": auth_header},
    )
    project_id = created.json()["id"]
    response = client.get(f"{base_url}/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["id"] == project_id


def test_project_update_200(
    client, apply_migrations, base_url, auth_header, mock_image_service
):
    headers = {"Authorization": auth_header}
    created = client.post(
        f"{base_url}/projects/", data=_project_form(), files=_image_file(), headers=headers
    )
    project_id = created.json()["id"]
    response = client.put(
        f"{base_url}/projects/{project_id}",
        data={"title": "Updated Title"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"


def test_project_update_404(
    client, apply_migrations, base_url, auth_header, mock_image_service
):
    response = client.put(
        f"{base_url}/projects/1000000",
        data={"title": "Updated Title"},
        headers={"Authorization": auth_header},
    )
    assert response.status_code == 404


def test_project_delete_200(
    client, apply_migrations, base_url, auth_header, mock_image_service
):
    headers = {"Authorization": auth_header}
    created = client.post(
        f"{base_url}/projects/", data=_project_form(), files=_image_file(), headers=headers
    )
    project_id = created.json()["id"]
    response = client.delete(f"{base_url}/projects/{project_id}", headers=headers)
    assert response.status_code == 200
