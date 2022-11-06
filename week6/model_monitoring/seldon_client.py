import requests
from config import SeldonClient

client_conf = SeldonClient()


PREDICT_URL = f"http://{client_conf.DOMAIN}:{client_conf.PORT}/seldon/default/{client_conf.MODEL}/api/v1.0/predictions"


def send_request():
    data = {"data":{"ndarray":[[619, 1, 0, 42, 2, 0.0, 1, 1, 1, 101348.88]]}}
    response = requests.post(PREDICT_URL, json=data)
    print(response)
    print(response.json())



if __name__ == "__main__":
    for _ in range(500):
        send_request()