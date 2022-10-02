import pandas as pd
from sklearn.model_selection import train_test_split

def prepare_data(path_to_file):
    dataset = pd.read_csv(path_to_file)
    dataset.drop('RowNumber', axis=1, inplace=True)
    dataset.drop('Surname', axis=1, inplace=True)
    dataset.isnull()
    dataset = pd.get_dummies(dataset)
    data_separator = {'x': dataset.drop(columns=['CustomerId', 'Exited'], axis=1),
                      'y': dataset['Exited']}
    X_train, X_test, y_train, y_test = train_test_split(data_separator['x'], data_separator['y'], random_state=42,
                                                        test_size=0.2)
    data_to_predict = [{'x': X_train, 'y': y_train}, {'x': X_test, 'y': y_test}]
    return data_to_predict
