from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator, AnyUrl


class PostgresDSN(AnyUrl):
    allowed_schemes = {'postgresql+asyncpg', 'postgresql'}
    user_required = True


class Configuration(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    OBJECTS_API_URL: str
    AUCTIONS_API_URL: str
    DATE_MODIFIED: str

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDSN] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
            cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True
        env_file = ".env.example"


settings = Configuration()
