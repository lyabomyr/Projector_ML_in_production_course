from concurrent.futures import wait
import numpy as np
import concurrent
import pandas as pd
import pytest_benchmark
from serving.ml_decision_tree_sample.predictor import model_for_predict
from serving.config import train_file, model_file_name, test_file_for_predict
from serving.ml_decision_tree_sample.prepare_data import prepare_data_for_train, common_prepare, \
    prepare_data_for_predict
from serving.ml_decision_tree_sample.load_model import model_loader
from serving.ml_decision_tree_sample.train import grid_train_model


def download_model():
    model_loader('download', model_file_name)


def my_predict(file):
    input_df = pd.read_csv(test_file_for_predict)
    output_df = model_for_predict(prepare_data_for_predict(input_df), model_file_name)
    input_df['Exited'] = output_df
    result = input_df
    return result


def run_inference(x_test=prepare_data_for_predict(pd.read_csv(test_file_for_predict)), batch_size: int = 1500):
    y_pred = []
    for i in range(0, x_test.shape[0], batch_size):
        x_batch = x_test[i: i + batch_size]
        y_batch = model_for_predict(x_batch, model_file_name)
        y_pred.append(y_batch)
    return np.concatenate(y_pred)


def run_inference_process_pool(X=prepare_data_for_predict(pd.read_csv(test_file_for_predict)), max_workers: int = 14):
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        chunk_size = len(X) // max_workers
        chunks = []
        for i in range(0, len(X), chunk_size):
            chunks.append(X[i: i + chunk_size])
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

def test_optimized_predict(benchmark):
    benchmark(run_inference_process_pool)


# -------------------------------------------------- benchmark: 1 tests -------------------------------------------------
# Name (time in ms)               Min       Max      Mean  StdDev    Median     IQR  Outliers     OPS  Rounds  Iterations
# -----------------------------------------------------------------------------------------------------------------------
# test_optimized_predict     162.6492  179.1311  170.1867  5.9578  170.0330  8.3828       2;0  5.8759       6           1
# -----------------------------------------------------------------------------------------------------------------------