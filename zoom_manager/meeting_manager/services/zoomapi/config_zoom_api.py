from dataclasses import dataclass
from environs import Env


@dataclass
class Config:

    api_url: str
    access_token_url: str
    client_id: str
    client_secret: str


def load_config(path_to_env="./meeting_manager/services/.env_zoom"):

    env = Env()
    env.read_env(path_to_env)

    return Config(
        api_url=env.str("ZOOM_API_URL"),
        access_token_url=env.str("ZOOM_ACCESS_TOKEN_URL"),
        client_id=env.str("ZOOM_CLIENT_ID"),
        client_secret=env.str("ZOOM_CLIENT_SECRET"),
    )
