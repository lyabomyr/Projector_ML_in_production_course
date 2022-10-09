import pandas as pd
import typer
from pathlib import Path
from sklearn.model_selection import train_test_split


def prepare_data(path_to_file: str, patch_to_save_file: str):
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
    if patch_to_save_file != '':
        X_train.to_csv(Path(patch_to_save_file) / 'X_train.csv', index=False)
        y_train.to_csv(Path(patch_to_save_file) / 'y_train.csv', index=False)
        X_test.to_csv(Path(patch_to_save_file) / 'X_test.csv', index=False)
        y_test.to_csv(Path(patch_to_save_file) / 'y_test.csv', index=False)
    return data_to_predict


if __name__ == "__main__":
    typer.run(prepare_data)
