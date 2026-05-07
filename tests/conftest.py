from fastapi.testclient import TestClient
from app import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pytest
import os
from pydantic_settings import BaseSettings,SettingsConfigDict
from pathlib import Path
from app.models import Base
from  alembic import command
from alembic.config import Config


#local packages
from app.dependencies import  create_session
from app.config import app_settings

class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file='../../.env',env_file_encoding='utf-8',extra='ignore')
    TEST_DATABASE_URL:str
    BASE_URL:str
    PASSWORD:str

TestConfig = Settings()

engine = create_engine(TestConfig.TEST_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def base_url():
    return TestConfig.BASE_URL


@pytest.fixture(scope="function")
def client():
    def override_create_session():
        with SessionLocal() as session:
            yield session

    app.dependency_overrides[create_session] = override_create_session
    with TestClient(app) as client:
        yield client
        app.dependency_overrides.clear()

@pytest.fixture(scope="function",autouse=True)
def apply_migrations():
    os.environ['DATABASE_URL'] = TestConfig.TEST_DATABASE_URL
    os.environ['ALEMBIC_URL'] = TestConfig.TEST_DATABASE_URL
    alembic_cfg = Config('alembic.ini')
    command.upgrade(alembic_cfg, 'head')
    yield
    command.downgrade(alembic_cfg, 'base')


@pytest.fixture(scope="function")
def auth_header(client ,apply_migrations,base_url):
    response = client.post(f"{base_url}/users/create",json={"user_name":"jniyonkuru","password":f"{TestConfig.PASSWORD}","role":"admin","email":"jacques@gmail.com","first_name":"jack","last_name":"niyonkuru"})
    response = client.post(f"{base_url}/users/token",data={"username":"jniyonkuru","password":f"{TestConfig.PASSWORD}"})
    access_token = response.json()["access_token"]
    return  f"Bearer {access_token}"





