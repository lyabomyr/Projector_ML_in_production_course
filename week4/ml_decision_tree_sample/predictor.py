import typer
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import RocCurveDisplay
from sklearn.metrics import f1_score
import pandas as pd
import base64
from io import BytesIO
from matplotlib import pyplot as plt
import joblib


def plot_to_str():
    img = BytesIO()
    plt.savefig(img, format='png')
    return base64.encodebytes(img.getvalue()).decode('utf-8')


def model_for_predict(path_to_model_file: str, x_train:str, y_test:str, patch_to_result:str):
    X_test = pd.read_csv(x_train)
    y_train = pd.read_csv(y_test)
    clf = joblib.load(path_to_model_file)
    predict = clf.predict(X_test)
    print(f'f1_scrore = {f1_score(y_train.to_numpy(), predict)}')

    return pd.DataFrame(predict).to_csv(Path(patch_to_result) / 'predict.csv')


def create_graph_svc(X_test, y_test, path_to_model_file):
    clf = joblib.load(path_to_model_file)
    svc_disp = RocCurveDisplay.from_estimator(clf, X_test, y_test)
    svc_disp = plot_to_str()
    return svc_disp


def create_graph_importance(X_test, path_to_model_file):
    clf = joblib.load(path_to_model_file)
    importance = clf.best_estimator_.feature_importances_
    feature_importance_df = pd.DataFrame({'features': list(X_test),
                                          'feature_importance': importance})
    feature_importance_df.sort_values('feature_importance', ascending=False)
    importance_analys = feature_importance_df.plot(kind='bar', x='features', y='feature_importance').get_figure()
    importance_analys = plot_to_str()
    return importance_analys


def create_confusion_matrix(X_test, y_test, path_to_model_file):
    clf = joblib.load(path_to_model_file)
    confusion_matrix_png = plot_confusion_matrix(clf, X_test, y_test)
    confusion_matrix_png = plot_to_str()
    return confusion_matrix_png

if __name__ == "__main__":
    typer.run(model_for_predict)