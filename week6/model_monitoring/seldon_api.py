import array
import time
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Optional, Union
import numpy as np
from ml_decision_tree_sample.load_model import model_loader
from ml_decision_tree_sample.predictor import model_for_predict
from ml_decision_tree_sample.prepare_data import prepare_data_for_predict, prepare_data_for_train
from ml_decision_tree_sample.train import grid_train_model

from config import model_file_name
import logging

logger = logging.getLogger()


@dataclass
class Score:
    tp: int = 0
    fp: int = 0
    tn: int = 0
    fn: int = 0


class SeldonAPI:
    def __init__(self):
        self.scores = Score()
        model_loader('download', model_file_name)
        self.inference_time = 0
        self.num_requests = 0

    def predict(self, X: Union[np.ndarray, List, str, bytes, Dict], names: Optional[List[str]] = None,
                meta: Optional[Dict] = None):
        start = time.perf_counter()
        df = pd.DataFrame(X,
                          columns=['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance',
                                   'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary'])
        logger.info(df)
        prediction = model_for_predict(df, model_file_name).to_dict()
        logger.info(prediction)
        self.inference_time = time.perf_counter() - start
        self.num_requests += 1
        return prediction

    def metrics(self):
        return [
            {"type": "TIMER", "key": "inference_time", "value": self.inference_time},
            {"type": "GAUGE", "key": f"request_num", "value": self.num_requests},
            {"type": "GAUGE", "key": f"true_pos", "value": self.scores.tp},
            {"type": "GAUGE", "key": f"true_neg", "value": self.scores.fp},
            {"type": "GAUGE", "key": f"false_pos", "value": self.scores.tn},
            {"type": "GAUGE", "key": f"false_neg", "value": self.scores.fn}
        ]

    def send_feedback(self, features, feature_names, reward, truth, routing=""):
        logger.info("features")
        logger.info(features)

        logger.info("truth")
        logger.info(truth)

        predictions = model_for_predict(features, model_file_name).to_dict()
        logger.info(predictions)
        if int(truth[0]) == 1:
            if int(predictions[0]) == int(truth[0]):
                self.scores.tp += 1
            else:
                self.scores.fn += 1
        else:
            if int(predictions[0]) == int(truth[0]):
                self.scores.tn += 1
            else:
                self.scores.fp += 1
        return []

        
