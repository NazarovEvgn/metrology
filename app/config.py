from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Metrology Backend"
    env: str = "dev"
    debug: bool = True
    version: str = "0.1.0"

    database_url: str = Field(
        default="postgresql+psycopg://metrology:metrology@localhost:5432/metrology",
        description="SQLAlchemy-compatible DB URL",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="METROLOGY_",
        extra="ignore",
    )


settings = Settings()
