from datetime import datetime, timedelta
import uuid
import pandas as pd
import joblib
from config import AzireConfig, model_file_name,train_file
from arize.pandas.logger import Client
from arize.utils.types import ModelTypes, Environments, Schema
from dataclasses import dataclass
from typing import Dict, List, Optional, Union
import numpy as np
import logging
from sklearn.metrics import f1_score
from ml_decision_tree_sample.load_model import model_loader
from ml_decision_tree_sample.predictor import model_for_predict 
from ml_decision_tree_sample.prepare_data import prepare_data_for_predict, prepare_data_for_train, common_prepare
from ml_decision_tree_sample.train import grid_train_model 
config =  AzireConfig()
 
train_df = pd.read_csv('../Churn_Modelling.csv', index_col=False)




class AzireCilentExamle:

    def __init__(self):
        self.df= pd.read_csv(train_file)
        self.train_x = prepare_data_for_train(self.df)[0]['x']
        self.train_y = prepare_data_for_train(self.df)[0]['y']
        self.test_x = prepare_data_for_train(self.df)[1]['x']
        self.test_y = prepare_data_for_train(self.df)[1]['y']
        self.train_df = pd.get_dummies(common_prepare(self.df))
        grid_train_model(self.test_x, self.test_y, model_file_name)
        

    def simulate_production_timestamps(self, X, days=30):
        t = datetime.now()
        current_ts, earlier_ts = t.timestamp(), (t - timedelta(days=days)).timestamp()
        return pd.Series(np.linspace(earlier_ts, current_ts, num=len(X)), index=X.index)

    def prepare_dataframe(self, x, y):
        self.clf = joblib.load(model_file_name)
        clf = self.clf 
        df = pd.DataFrame()
        df['CreditScore'] = x.CreditScore
        df['Age'] =  x.Age
        df['Balance'] = x.Balance
        df["simul_timestamp"] = self.simulate_production_timestamps(x)
        df["prediction_id"] = [str(uuid.uuid4()) for _ in range(len(y))]
        df["prediction_label"] = np.array(clf.predict(x)).astype(str)
        df["actual_label"] = np.array(y).astype(str)
        df["prediction_score"] = np.array(clf.predict_proba(x)[:,1])
        logging.debug(df)
        return df

    def send_to_arize(self, x, y, action):
        arize_client = Client(space_key=config.SPACE_KEY, api_key=config.API_KEY)
        schema = Schema(
            prediction_id_column_name="prediction_id",
            prediction_label_column_name="prediction_label",
            prediction_score_column_name="prediction_score",
            timestamp_column_name = "simul_timestamp",
            actual_label_column_name="actual_label",
            feature_column_names=['CreditScore', 'Age', 'Balance'],
        )
        res = arize_client.log(
            dataframe= self.prepare_dataframe(x, y),
            model_id= config.MODEL_ID,
            model_version= config.MODEL_VERSION,
            model_type=ModelTypes.SCORE_CATEGORICAL,
            environment=action,
            schema=schema,
        )
        if res.status_code != 200:
            logging.CRITICAL(f"❌ logging failed with response code {res.status_code}, {res.text}")
        else:
            logging.warning(f"✅ You have successfully logged training set to Arize")

    def client_send(self, selected_action):
        if selected_action.lower() == 'train':
            self.send_to_arize(self.train_x,
                               self.train_y, 
                               Environments.TRAINING)
            logging.info('Complete_'*20)
        if selected_action.lower() == 'test':
            self.send_to_arize(self.test_x,self.test_y,Environments.PRODUCTION)
            logging.info('Complete_'*20)




if __name__ == "__main__":
    AzireCilentExamle = AzireCilentExamle()
    AzireCilentExamle.client_send('train')
    AzireCilentExamle.client_send('test')