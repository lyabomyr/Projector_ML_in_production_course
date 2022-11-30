import pandas as pd
import typer
from ml_decision_tree_sample.prepare_data import prepare_data_for_train
from config import train_file
from alibi_detect.cd import MMDDrift
import numpy as np


def inference_multivariate(train_csv:str, test_csv:str):

    train_x = np.array(prepare_data_for_train(pd.read_csv(train_csv))[0]['x'])
    test_x = np.array(prepare_data_for_train(pd.read_csv(test_csv))[1]['x'])
    
    cd_mmd = MMDDrift(train_x, p_val = .05, backend='pytorch')
    drift = cd_mmd.predict(test_x)

    if drift["data"]["is_drift"] == 1:
        print("Alert: data drift detected!")
        raise ValueError(drift)
    print(drift)


if __name__ == "__main__":
    typer.run(inference_multivariate)
