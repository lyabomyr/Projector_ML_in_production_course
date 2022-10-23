import requests
from serving.config import uri, request_body, headers


def test_connection():
    r = requests.post(uri, json=request_body, headers=headers)
    r.close()
    assert r.status_code == 200

def test_response_body():
    r = requests.post(uri, json=request_body, headers=headers)
    print(r.json().keys())
    # print(r.keys())
    print(r.json()["jsonData"])
    assert "meta" in r.json().keys()
    assert "jsonData" in r.json().keys()

print(test_response_body())