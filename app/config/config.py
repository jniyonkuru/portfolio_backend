from pathlib import Path

from pydantic_settings import BaseSettings,SettingsConfigDict

BASE_DIR=Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=BASE_DIR / '.env',env_file_encoding='utf-8',extra='ignore')
    DATABASE_URL:str
    SECRET_KEY:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    ALGORITHM:str
    # Only needed for migrations / seeding, which read them straight from the
    # environment. Optional here so the running app doesn't require them.
    ALEMBIC_URL:str|None=None
    PASSWORD:str|None=None

app_settings=Settings()



