import typer
import pandas as pd
from ml_decision_tree_sample.prepare_data import prepare_data_for_train
from config import train_file
from alibi_detect.cd import KSDrift
import numpy as np


def univariable_inference(train_file:str, test_file:str):
    train_x = prepare_data_for_train(pd.read_csv(train_file))[0]['x']
    test_x = prepare_data_for_train(pd.read_csv(test_file))[1]['x']
    
    list_name = train_x.columns.to_list()[1:8]
    train_x = np.array(train_x)
    test_x = np.array(test_x)


    cd_1 = KSDrift(train_x[:, 1], p_val=.05)
    cd_2 = KSDrift(train_x[:, 2], p_val=.05)
    cd_3 = KSDrift(train_x[:, 3], p_val=.05)
    cd_4 = KSDrift(train_x[:, 4], p_val=.05)
    cd_5 = KSDrift(train_x[:, 5], p_val=.05)
    cd_6 = KSDrift(train_x[:, 6], p_val=.05)
    cd_7 = KSDrift(train_x[:, 7], p_val=.05)

    drift_1 = cd_1.predict(test_x[:, 1])
    drift_2 = cd_2.predict(test_x[:, 2])
    drift_3 = cd_3.predict(test_x[:, 3])
    drift_4 = cd_4.predict(test_x[:, 4])
    drift_5 = cd_5.predict(test_x[:, 5])
    drift_6 = cd_6.predict(test_x[:, 6])
    drift_7 = cd_7.predict(test_x[:, 7])

    drifts = [drift_1, drift_2, drift_3, drift_4, drift_5, drift_6, drift_7]

    assert len(drifts) == len(list_name)
    for result, colum_name in zip(drifts, list_name):
        if result["data"]["is_drift"] == 1:
            print(f"Alert: data drift detected for {result}!")
            raise ValueError(result)
        else:
            print(f"{colum_name}:{result}")


if __name__ == "__main__":
    typer.run(univariable_inference)