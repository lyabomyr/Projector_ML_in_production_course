from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib


def model_for_predict(X_test: pd.DataFrame, path_to_model_file: str):
    clf = joblib.load(path_to_model_file)
    predict = clf.predict(X_test)
    return pd.DataFrame(predict)
