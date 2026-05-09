from pathlib import Path

from pydantic_settings import BaseSettings,SettingsConfigDict

BASE_DIR=Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=BASE_DIR / '.env',env_file_encoding='utf-8',extra='ignore')
    DATABASE_URL:str
    ALEMBIC_URL:str
    PASSWORD:str
    SECRET_KEY:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    ALGORITHM:str
    TEST_DATABASE_URL:str


app_settings=Settings()



