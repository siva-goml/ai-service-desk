from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")
    APP_NAME: str = "AI SERVICE DESK"
    API_VERSION: str = "1.0.0"
    DEBUG: bool
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    AWS_SECRET_ACCESS_KEY:str
    AWS_ACCESS_KEY_ID:str
    AWS_DEMO_MODE:str
    DATABASE_READY:str
    BEDROCK_MODEL_ID:str
    AWS_REGION:str


settings = Settings()
