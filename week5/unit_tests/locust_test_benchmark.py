from locust import HttpUser, task, between
import logging
import time


class FastApiBenchmark(HttpUser):
    @task
    def test_predict(self):
        url = '/batch_predict_csv_file/'
        files = {'file': open('test_churn_modelling.csv', 'rb')}
        self.client.post(url, files=files)

