from typing import List, Union, Dict, Any
import pandas as pd
from sklearn.model_selection import train_test_split


def common_prepare(dataset: pd.DataFrame) -> pd.DataFrame:
    dataset = dataset.drop(['RowNumber', 'Surname', 'CustomerId'], axis=1)
    dataset = dataset.replace({'Gender': {'Female': 0, 'Male': 1}})
    dataset = dataset.replace({'Geography': {'France': 1, 'Spain': 2, 'Germany': 3}})
    return dataset


def prepare_data_for_train(dataset: pd.DataFrame) -> List[Union[Dict[str, Any], Dict[str, Any]]]:
    dataset = pd.get_dummies(common_prepare(dataset))
    data_separator = {'x': dataset.drop(columns=['Exited'], axis=1),
                      'y': dataset['Exited']}
    X_train, X_test, y_train, y_test = train_test_split(data_separator['x'], data_separator['y'], random_state=42,
                                                        test_size=0.2)
    data_to_predict = [{'x': X_train, 'y': y_train}, {'x': X_test, 'y': y_test}]
    return data_to_predict


def prepare_data_for_predict(dataset: pd.DataFrame) -> pd.DataFrame:
    if 'Unnamed: 0' in dataset:
        dataset = common_prepare(dataset).drop('Unnamed: 0', axis=1)
    else:
        dataset = common_prepare(dataset)
    return dataset