from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    BOB_API_KEY: str
    GITHUB_TOKEN: str
    DATABASE_URL: str = "sqlite:///./prism.db"
    BOB_MAX_TIMEOUT_SECONDS: int = 45
    BOB_CHAT_MODE: str = "ask"

settings = Settings()
