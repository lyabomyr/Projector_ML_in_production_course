import array
import time
import pandas as pd
from typing import Dict, List, Optional, Union
import numpy as np
from serving.ml_decision_tree_sample.load_model import model_loader
from serving.ml_decision_tree_sample.predictor import model_for_predict
from serving.ml_decision_tree_sample.prepare_data import prepare_data_for_predict, prepare_data_for_train
from serving.ml_decision_tree_sample.train import grid_train_model

from serving.config import model_file_name
import logging

logger = logging.getLogger()


class SeldonAPI:
    def __init__(self):
        model_loader('download', model_file_name)

    def predict(self, X: Union[np.ndarray, List, str, bytes, Dict], names: Optional[List[str]] = None,
                meta: Optional[Dict] = None):
        df = pd.DataFrame(X,
                          columns=['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance',
                                   'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary'])
        logger.info(df)
        prediction = model_for_predict(df, model_file_name).to_dict()
        logger.info(prediction)
        return prediction