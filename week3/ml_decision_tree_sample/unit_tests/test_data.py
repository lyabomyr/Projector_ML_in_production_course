from great_expectations.dataset.pandas_dataset import PandasDataset
import pandas as pd
import pytest

@pytest.fixture
def read_csv():
    return pd.read_csv('../../Churn_Modelling.csv')

@pytest.fixture
def init_ge_df(read_csv):
    return PandasDataset(read_csv)


def test_data_shape(read_csv):
    df_train = read_csv
    assert df_train.shape[0] == 10000, 'data rows !=10000'
    assert df_train.shape[1] == 14, 'data columns != 14'

def test_data_order(init_ge_df):
    df = init_ge_df
    assert df.expect_column_values_to_be_unique(column="RowNumber")['success'], 'RowNumber is not unique'
    assert df.expect_column_values_to_be_unique(column="CustomerId")['success'], 'CustomerId is not unique'
    assert df.expect_column_values_to_be_of_type(column="Exited", type_="int")['success'], 'type for Exited column is ' \
                                                                                           'not int Exited '
    assert df.expect_column_values_to_not_be_null(column="Exited")['success'], 'column Exited have value like null'

def test_data_content(init_ge_df):
    df = init_ge_df
    assert df.expect_table_columns_to_match_ordered_list(column_list=[
        "RowNumber",
        "CustomerId",
        "Surname",
        "CreditScore",
        "Geography",
        "Gender",
        "Age",
        "Tenure",
        "Balance",
        "NumOfProducts",
        "HasCrCard",
        "IsActiveMember",
        "EstimatedSalary",
        "Exited"
    ])['success'], 'incorrect list columns'


