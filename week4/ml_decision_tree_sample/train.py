import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path
from sklearn.model_selection import GridSearchCV
from prepare_data import prepare_data
import typer


def grid_train_model(x_train:str, y_train:str, path_to_save_file: str):
    train = pd.read_csv(x_train)
    pred_train = pd.read_csv(y_train)
    clf_rf = RandomForestClassifier(random_state=42, n_jobs=-1)
    parameters = {'criterion': ['gini', 'entropy'],
                  'max_depth': [11],
                  'min_samples_leaf': [3],
                  'min_samples_split': [2],
                  'n_estimators': [30]}
    grid = GridSearchCV(clf_rf, parameters, cv=3)
    grid.fit(train, pred_train.values.ravel())
    joblib.dump(grid, Path(path_to_save_file) / 'model_random_forest.pkl')


if __name__ == "__main__":
    typer.run(grid_train_model)
