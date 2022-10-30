import pytest
import pytest_benchmark
from serving.ml_decision_tree_sample.predictor import model_for_predict
from serving.config import train_file, model_file_name, test_file_for_predict
from serving.ml_decision_tree_sample.prepare_data import prepare_data_for_train, common_prepare, \
    prepare_data_for_predict
from serving.ml_decision_tree_sample.load_model import model_loader
import pandas as pd



def download_model():
    model_loader('download', model_file_name)


def my_predict():
    input_df = pd.read_csv(test_file_for_predict)
    output_df = model_for_predict(prepare_data_for_predict(input_df), model_file_name)
    input_df['Exited'] = output_df
    result = input_df
    return result


def test_load_model(benchmark):
    benchmark(download_model)


def test_benchmark_port_forwarding_batch_predict(benchmark):
    benchmark(my_predict)
