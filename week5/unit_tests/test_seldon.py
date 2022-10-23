import requests
from serving.config import uri, request_body, headers


def test_connection():
    r = requests.post(uri, json=request_body, headers=headers)
    r.close()
    assert r.status_code == 200


