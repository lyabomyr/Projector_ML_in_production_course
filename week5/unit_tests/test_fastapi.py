import pytest
import io
from pandas import json_normalize
import pandas as pd
from fastapi import FastAPI
from fastapi.testclient import TestClient
from serving.fast_api import app
from serving.config import model_file_name
import logging

@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    response = client.get("/")
    logging.warning(response.json())
    assert response.status_code == 200
    assert response.json() == {
         "message": "please add \'/docs\' to ur url and u will be transferred to swagger page with list of request "
                  "example url http://127.0.0.1:8000/docs"}


def test_train(client):
    url = '/train_model_and_push_to_wandb/'
    files = {'file': open('Churn_Modelling.csv', 'rb')}
    response = client.post(url, files=files)
    assert response.json() == {'text_mes': 'Complete train and sent to wandb with model_name',
                            'model_name': 'model_random_forest.pkl'}
    assert response.status_code == 200


def test_predict(client):
    url = '/batch_predict_csv_file/'
    files = {'file': open('test_churn_modelling.csv', 'rb')}
    response = client.post(url, files=files)
    df = pd.read_csv(io.StringIO(response.text))
    assert response.status_code == 200
    assert df.shape[0] >= 2, 'data is empty'
    assert df.shape[1] == 14, 'data columns != 14'
