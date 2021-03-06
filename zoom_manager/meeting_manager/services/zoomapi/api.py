import base64
import json

import requests

from meeting_manager.models import ZoomCredentionals, ZoomMeetings, ZoomUsers

from .exceptions import (
    AccessTokenIsExpired,
    InvalidApiKeyOrSecret,
    InvalidTokenError,
    InvalidRefreshTokenError,
    UserDoesNotExist,
)
from .config_zoom_api import load_config


def encode_base64_auth_headers(client_id: str, client_secret: str) -> str:

    id_and_secret = f"{client_id}:{client_secret}"
    id_and_secret_ascii = id_and_secret.encode("ascii")
    encoded_data = base64.b64encode(id_and_secret_ascii)
    encoded_data_ascii = encoded_data.decode("ascii")
    auth_basic = f"Basic {encoded_data_ascii}"

    return auth_basic


def check_errors_and_access(json_resp: dict):

    if json_resp.get("message") == "Access token is expired.":
        raise AccessTokenIsExpired()

    elif json_resp.get("message") == "Invalid api key or secret.":
        raise InvalidApiKeyOrSecret()

    elif json_resp.get("message") == "Invalid access token.":
        raise InvalidTokenError()

    elif "User does not exist" in json_resp.get("message", "User exist"):
        raise UserDoesNotExist(json_resp["message"])


def refresh_token():

    config = load_config()

    access_token_url: str = config.access_token_url
    client_id: str = config.client_id
    client_secret: str = config.client_secret

    refresh_token_data = ZoomCredentionals.objects.get(name_data="refresh_token")
    access_token_data = ZoomCredentionals.objects.get(name_data="access_token")
    refresh_token = refresh_token_data.data

    headers_for_refresh = {
        "Authorization": encode_base64_auth_headers(client_id, client_secret),
        "Content-Type": "application/x-www-form-urlencoded",
    }

    params_for_refresh = {
        "grant_type": "refresh_token",
        "refresh_token": f"{refresh_token}",
    }

    response = requests.post(
        access_token_url, data=params_for_refresh, headers=headers_for_refresh
    )

    try:
        json_resp = response.json()
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


def get_users_list():

    access_token = ZoomCredentionals.objects.get(name_data="access_token").data
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get("https://api.zoom.us/v2/users", headers=headers)
        json_resp = response.json()

        check_errors_and_access(json_resp)

        users = json_resp["users"]
        user_list = []

        for user in users:
            user_id, first_name, last_name, user_email = (
                user["id"],
                user["first_name"],
                user["last_name"],
                user["email"],
            )
            user_list.append((user_id, first_name, last_name, user_email))
            zoom_user = ZoomUsers(user_id, first_name, last_name, user_email)
            zoom_user.save()

            return user_list

    except (AccessTokenIsExpired, InvalidApiKeyOrSecret, InvalidTokenError):

        if not refresh_token():
            return "Check your refresh_token for OAuth 2.0"

        print("???????????? ????????????????")
        get_users_list()


def get_meetings_from_all_users(zoom_users_id):

    access_token = ZoomCredentionals.objects.get(name_data="access_token").data
    headers = {"Authorization": f"Bearer {access_token}"}
    meetings_lst = []

    for user_id in zoom_users_id:
        try:
            response = requests.get(
                f"https://api.zoom.us/v2/users/{user_id}/meetings", headers=headers
            )

            json_resp: dict = response.json()

            check_errors_and_access(json_resp)

            lst_of_dict_meetings = json_resp["meetings"]

            if len(lst_of_dict_meetings) == 0:
                continue

            for meeting in lst_of_dict_meetings:
                uuid = meeting["uuid"]
                host_id = meeting["host_id"]
                topic = meeting["topic"]
                meet_type = meeting["type"]
                start_time = meeting["start_time"]
                duration = meeting["duration"]
                join_url = meeting["join_url"]

                meetings_lst.append(
                    (uuid, host_id, topic, start_time, duration, meet_type, join_url)
                )

                zoom_meeting = ZoomMeetings(
                    uuid, host_id, topic, start_time, duration, meet_type, join_url
                )
                zoom_meeting.save()

        except (AccessTokenIsExpired, InvalidApiKeyOrSecret, InvalidTokenError):
            if not refresh_token():
                return "Check your refresh_token for OAuth 2.0"

            print("???????????? ????????????????")
            return get_meetings_from_all_users(zoom_users_id=zoom_users_id)

        except UserDoesNotExist:
            return "User does not exist"

    return meetings_lst


def create_meeting(form: dict):

    access_token = ZoomCredentionals.objects.get(name_data="access_token").data
    headers = {"Authorization": f"Bearer {access_token}"}

    with open(
        "meeting_manager/services/zoomapi/json_template/create_template.json", "r"
    ) as tmp_request:
        request_json = json.load(tmp_request)

    user_id = form["host_email"]

    topic = form["topic"]
    start_time = f"{'T'.join([form['date'], form['time']])}+03:00"
    duration = int(form["duration"].split(":")[0]) * 60

    request_json["topic"] = topic
    request_json["start_time"] = start_time
    request_json["duration"] = duration

    if form.get("settings-auto_recording"):
        request_json["settings"]["auto_recording"] = form["settings-auto_recording"]

    print(request_json)

    try:
        response = requests.post(
            f"https://api.zoom.us/v2/users/{user_id}/meetings",
            headers=headers,
            json=request_json,
        )

        json_resp: dict = response.json()

        print(json_resp)
        check_errors_and_access(json_resp)

        return True

    except (AccessTokenIsExpired, InvalidApiKeyOrSecret, InvalidTokenError):

        if not refresh_token():
            return "Check your refresh_token for OAuth 2.0"

        create_meeting(form=form)
