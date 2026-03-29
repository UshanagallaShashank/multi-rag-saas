from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str

    redis_url: str = ""

    jwt_secret: str

    jwt_expire_minutes: int = 60

    encryption_key: str

    upload_dir: str = "/tmp/ragforge"

    openai_api_key: str = ""

    gemini_api_key: str = ""

settings = Settings()
