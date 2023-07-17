import toml
from pydantic import BaseSettings, SecretStr
from pydantic.networks import AnyUrl


poetry_data = toml.load('pyproject.toml')['tool']['poetry']


class Settings(BaseSettings):
    # api vars
    API_V1: str = "/api/v1"

    # db settings
    PASS: SecretStr = None
    DATABASE_URL: AnyUrl = None

    # open-api settings
    title: str = poetry_data['name']
    descriprion: str = poetry_data['description']
    version: str = poetry_data['version']
    openapi_tags: list = [
        {
            "name": "users",
            "description": "Users api",
        },
    ]


settings = Settings()
