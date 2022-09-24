import concurrent
import time
import pandas as pd
import numpy as np
import os
from tqdm import tqdm
from concurrent.futures import wait
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV

path_to_train_file = os.path.abspath("Churn_Modelling.csv").replace('inference/', '')


def prepare_data(path_to_file=path_to_train_file):
    dataset = pd.read_csv(path_to_file)
    dataset.drop('RowNumber', axis=1, inplace=True)
    dataset.isnull()
    dataset = pd.get_dummies(dataset)
    data_separator = {'x': dataset.drop(columns=['CustomerId', 'Exited'], axis=1),
                      'y': dataset['Exited']}
    X_train, X_test, y_train, y_test = train_test_split(data_separator['x'], data_separator['y'], random_state=42,
                                                        test_size=0.2)
    data_to_predict = [{'x': X_train, 'y': y_train}, {'x': X_test, 'y': y_test}]
    return data_to_predict


def predict(predict_data, prepared_data=prepare_data()):
    clf_rf = RandomForestClassifier(max_depth=11, min_samples_leaf=2, min_samples_split=8,
                                    n_estimators=30, n_jobs=-1, random_state=0)
    clf_rf.fit(prepared_data[0]['x'], prepared_data[0]['y'])
    return clf_rf.predict(predict_data)


def run_inference(x_test=prepare_data()[1]['x'], batch_size: int = 2048):
    y_pred = []
    for i in tqdm(range(0, x_test.shape[0], batch_size)):
        x_batch = x_test[i: i + batch_size]
        y_batch = predict(x_batch)
        y_pred.append(y_batch)
    return np.concatenate(y_pred)


def run_inference_process_pool(x_test=prepare_data()[1]['x'], max_workers: int = 16):
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        chunk_size = len(x_test) // max_workers
        chunks = []
        for i in range(0, len(x_test), chunk_size):
            chunks.append(x_test[i: i + chunk_size])
        futures = []
        for chunk in chunks:
            future = executor.submit(run_inference, x_test=chunk)
            futures.append(future)
        wait(futures)
        y_pred = []
        for future in futures:
            y_batch = future.result()
            y_pred.append(y_batch)
    return np.concatenate(y_pred)


if __name__ == "__main__":
    start_time = time.time()
    print('run inference: ',run_inference(), f'total process time {time.time() - start_time}')
    start_time = time.time()
    print('run_inference_process_pool: ', run_inference_process_pool(), f'total process time {time.time() - start_time}')