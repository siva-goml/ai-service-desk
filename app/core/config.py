from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings (BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
    APP_NAME: str = "AI SERVICE DESK"
    API_VERSION: str = "1.0.0"
    DEBUG: bool
    DATABASE_URL: str 
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
settings = Settings()