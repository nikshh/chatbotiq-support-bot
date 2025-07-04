import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    token: str
    db_uri: str
    similarity_threshold: float = 0.10  # Minimum cosine similarity threshold for answer matching

    model_config = SettingsConfigDict(
        env_nested_delimiter="__", env_file=".env", case_sensitive=False, extra="allow"
    )


settings = Settings()

if __name__ == "__main__":
    print(settings)
