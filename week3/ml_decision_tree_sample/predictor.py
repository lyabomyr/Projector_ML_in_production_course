from sklearn.ensemble import RandomForestClassifier
from prepare_data import prepare_data
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import RocCurveDisplay
import pandas as pd
import base64
from io import BytesIO
from matplotlib import pyplot as plt


def plot_to_str():
    img = BytesIO()
    plt.savefig(img, format='png')
    return base64.encodebytes(img.getvalue()).decode('utf-8')


def model_for_predict(X_train=prepare_data()[0]['x'],
                      y_train=prepare_data()[0]['y']):
    clf = RandomForestClassifier(max_depth=11, min_samples_leaf=3,
                                 min_samples_split=2,
                                 n_estimators=30, random_state=42)
    clf.fit(X_train, y_train)
    return clf


def create_graph_svc(X_test=prepare_data()[1]['x'], y_test=prepare_data()[1]['y']):
    svc_disp = RocCurveDisplay.from_estimator(model_for_predict(), X_test, y_test)
    #svc_disp.figure_.savefig('RocCurveDisplay.png')
    svc_disp = plot_to_str()
    return svc_disp

def create_graph_importance(X_test=prepare_data()[1]['x']):
    importance = model_for_predict().feature_importances_
    feature_importance_df = pd.DataFrame({'features': list(X_test),
                                          'feature_importance': importance})
    feature_importance_df.sort_values('feature_importance', ascending=False)
    importance_analys = feature_importance_df.plot(kind='bar', x='features', y='feature_importance').get_figure()
    #importance_analys.savefig('importance.png')
    importance_analys = plot_to_str()
    return importance_analys

def create_confusion_matrix(X_test=prepare_data()[1]['x'], y_test=prepare_data()[1]['y']):
    confusion_matrix(y_test, model_for_predict().predict(X_test))
    confusion_matrix_png = plot_confusion_matrix(model_for_predict(), X_test, y_test)
    #confusion_matrix_png.figure_.savefig('confusion_matrix.png')
    confusion_matrix_png = plot_to_str()
    return confusion_matrix_png
