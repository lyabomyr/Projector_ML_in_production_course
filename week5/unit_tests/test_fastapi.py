class TestFastapi:
    client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/")
        logging.warning(response.json())
        assert response.status_code == 200
        assert response.json() == {
            "message": "please add \'/docs\' to ur url and u will be transferred to swagger page with list of request "
                    "example url http://127.0.0.1:8000/docs"}


    def test_train(self):
        url = '/train_model_and_push_to_wandb/'
        files = {'file': open('Churn_Modelling.csv', 'rb')}
        response = self.client.post(url, files=files)
        assert response.json() == {'text_mes': 'Complete train and sent to wandb with model_name',
                                'model_name': 'model_random_forest.pkl'}
        assert response.status_code == 200


    def test_predict(self):
        url = '/batch_predict_csv_file/'
        files = {'file': open('test_churn_modelling.csv', 'rb')}
        response = self.client.post(url, files=files)
        df = pd.read_csv(io.StringIO(response.text))
        assert response.status_code == 200
        assert df.shape[0] >= 2, 'data is empty'
        assert df.shape[1] == 14, 'data columns != 14'
