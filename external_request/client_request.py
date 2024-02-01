import requests

APP_URL = "http://127.0.0.1:5000/getCsv"


def transmit_csv(filename):
    payload = {}
    files = [
        ('file',
         ('vehicles.csv', open(filename, 'rb'), 'text/csv'))
    ]
    headers = {}

    response = requests.request("POST", APP_URL, headers=headers, data=payload, files=files)

    return response.json()
