from app.schemas import ExperienceCreate
from fastapi.encoders import jsonable_encoder

experience = ExperienceCreate(role='Web developer intern',start_date="2024-01-20",tasks=['task1','task2'],end_date="2024-10-20",organization="Andela")


def  test_experiences_200(client, apply_migrations):
      response= client.get('/api/v1/experiences')
      assert response.status_code == 200
      assert type(response.json()) == list

def test_experiences_404(client,apply_migrations):
      response= client.get('/api/v1/experiences/1000000')
      assert response.status_code == 404

def test_experiences_create_401(client,apply_migrations):
      experience = ExperienceCreate(role='Web developer intern',start_date="2024-01-20",tasks=['task1','task2'],end_date="2024-10-20",organization="Andela")
      response= client.post('/api/v1/experiences',json=jsonable_encoder(experience))
      assert response.status_code == 401

def test_experiences_create_200(client,apply_migrations,auth_header):
      experience = ExperienceCreate(role='Web developer intern',start_date="2024-01-20",tasks=['task1','task2'],end_date="2024-10-20",organization="Andela")
      response= client.post('/api/v1/experiences',json=jsonable_encoder(experience),headers={"Authorization":auth_header})
      assert response.status_code == 200


def test_experiences_create_422(client,apply_migrations,base_url,auth_header):
      experience={}
      response=client.post (f'{base_url}/experiences',headers={"Authorization":auth_header},json=experience)
      assert response.status_code == 422

def test_experience_create_409(client,apply_migrations,base_url,auth_header):
      experience = ExperienceCreate(role='Web developer intern', start_date="2024-01-20", tasks=['task1', 'task2'],
                                    end_date="2024-10-20", organization="Andela")
      first_response=client.post(f'{base_url}/experiences',json=jsonable_encoder(experience),headers={"Authorization":auth_header})
      second_response=client.post(f'{base_url}/experiences',json=jsonable_encoder(experience),headers={"Authorization":auth_header})
      assert second_response.status_code == 409

def test_experience_update_404(client,apply_migrations,base_url,auth_header):
      experience_id=3
      experience_exists=client.get(f'{base_url}/experiences/{experience_id}')
      assert experience_exists.status_code == 404

def test_experience_update_401(client,apply_migrations,auth_header,base_url):
      first_response=client.post(f'{base_url}/experiences',json=jsonable_encoder(experience),headers={"Authorization":auth_header})
      experience_id=first_response.json()['id']
      response=client.put(f'{base_url}/experiences/{experience_id}',json=jsonable_encoder(experience))
      assert response.status_code == 401

def test_experience_update_200(client,apply_migrations,auth_header,base_url):
      first_response=client.post(f'{base_url}/experiences',json=jsonable_encoder(experience),headers={"Authorization":auth_header})
      experience_id=first_response.json()['id']
      second_response=client.put(f'{base_url}/experiences/{experience_id}',json={**jsonable_encoder(experience),'role':'Full stack engineer'},headers={"Authorization":auth_header})
      assert second_response.status_code == 200

def test_experience_delete_201(client,apply_migrations,auth_header,base_url):
      first_response=client.post(f'{base_url}/experiences',json=jsonable_encoder(experience),headers={"Authorization":auth_header})
      experience_id=first_response.json()['id']
      second_response=client.delete(f'{base_url}/experiences/{experience_id}',headers={"Authorization":auth_header})
      assert second_response.status_code == 200