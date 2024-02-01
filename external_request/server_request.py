import requests
import json

BASE_URL = "https://api.baubuddy.de"


def get_access_token():
    """
    Requests an access token from server for authorization
    :return:
    """
    url = f'{BASE_URL}/index.php/login'

    payload = json.dumps({
        "username": "365",
        "password": "1"
    })
    headers = {
        'Authorization': 'Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()["oauth"]["access_token"]


def get_resources(token):
    """
    Requests resources from server using access token obtained

    :param token:
    :return:
    """
    url = f'{BASE_URL}/dev/index.php/v1/vehicles/select/active'

    payload = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def get_color_code(token, label_id):
    """
    "Requests color codes using `labelIds` field in the vehicle info
    :param token:
    :param label_id:
    :return:
    """

    url = f'{BASE_URL}/dev/index.php/v1/labels/{label_id}'

    payload = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()
