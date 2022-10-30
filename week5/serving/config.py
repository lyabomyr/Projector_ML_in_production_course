model_file_name = 'model_random_forest.pkl'
remove_dir_name = 'wandb'
seldon_host = "http://localhost"
seldon_port = "7777"
seldon_endpoint = "/seldon/default/churnpredict/api/v1.0/predictions"
uri = f"{seldon_host}:{seldon_port}{seldon_endpoint}"
request_body = {"data": {"ndarray": [[619, 1, 0, 42, 2, 0.0, 1, 1, 1, 101348.88]]}}
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}
train_file = 'Churn_Modelling.csv'
test_file_for_predict = 'test_churn_modelling.csv'
