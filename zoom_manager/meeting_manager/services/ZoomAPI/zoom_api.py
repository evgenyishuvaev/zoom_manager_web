import base64
from typing import Optional, Union, List
import requests

from meeting_manager.models import ZoomCredentionals, ZoomMeetings, ZoomUsers

from .exceptions import (
    AccessTokenIsExpired,
    InvalidApiKeyOrSecret,
    InvalidTokenError,
    InvalidRefreshTokenError
)
from .config_zoom_api import load_config

def encode_base64_auth_headers(client_id: str, client_secret: str ) -> str:
    
    id_and_secret = f"{client_id}:{client_secret}"
    id_and_secret_ascii = id_and_secret.encode("ascii")
    encoded_data = base64.b64encode(id_and_secret_ascii)
    encoded_data_ascii = encoded_data.decode("ascii")
    auth_basic = f"Basic {encoded_data_ascii}"
    
    return auth_basic


def check_access(json_resp : dict):

    if json_resp.get("message") == "Access token is expired.":
        raise AccessTokenIsExpired()

    elif json_resp.get("message") == "Invalid api key or secret.":
        raise InvalidApiKeyOrSecret()

    elif json_resp.get("message") == "Invalid access token.":
        raise InvalidTokenError()


def refresh_token() -> Optional[Union[bool, str]]:

    config = load_config()

    access_token_url : str = config.access_token_url
    client_id : str = config.client_id
    client_secret: str = config.client_secret

    refresh_token_data = ZoomCredentionals.objects.get(name_data="refresh_token")
    access_token_data = ZoomCredentionals.objects.get(name_data="access_token")
    refresh_token = refresh_token_data.data
    print(refresh_token)

    headers_for_refresh = {
        "Authorization": encode_base64_auth_headers(client_id, client_secret),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    params_for_refresh = {
        "grant_type": "refresh_token",
        "refresh_token": f"{refresh_token}"
    }


    response = requests.post(
            access_token_url,
            data=params_for_refresh,
            headers=headers_for_refresh
            )
        
    try:
        json_resp = response.json()
        print(json_resp)
        if "reason" in json_resp.keys() and json_resp["reason"] == "Invalid Token!":
            raise InvalidRefreshTokenError()

        data_list = list(json_resp.items())
        new_access_token = data_list[0]
        new_refresh_token = data_list[2]
    except InvalidRefreshTokenError:
        return False
    
    access_token_data.data = new_access_token[1]
    refresh_token_data.data = new_refresh_token[1]
    access_token_data.save()
    refresh_token_data.save()

    return "Token was refresh!"