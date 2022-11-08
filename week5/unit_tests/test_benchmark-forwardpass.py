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

# --------------------------------------------- benchmark: 1 tests --------------------------------------------
# Name (time in s)         Min      Max     Mean  StdDev   Median     IQR  Outliers     OPS  Rounds  Iterations
# -------------------------------------------------------------------------------------------------------------
# test_load_model      10.2292  11.5095  10.5239  0.5529  10.2788  0.3966       1;1  0.0950       5           1
# -------------------------------------------------------------------------------------------------------------

def test_benchmark_port_forwarding_batch_predict(benchmark):
     benchmark(my_predict)

# ----------------------------------------------------------- benchmark: 1 tests -----------------------------------------------------------
# Name (time in ms)                                    Min      Max     Mean  StdDev   Median     IQR  Outliers      OPS  Rounds  Iterations
# ------------------------------------------------------------------------------------------------------------------------------------------
# test_benchmark_port_forwarding_batch_predict     42.1755  47.1522  43.5888  1.4053  43.0883  1.8938       4;1  22.9417      18           1
# ------------------------------------------------------------------------------------------------------------------------------------------


