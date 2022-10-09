import typer
import os, sys
import pandas as pd
import model_card_toolkit as mctlib
import uuid
from datetime import date
from predictor import create_confusion_matrix, create_graph_importance, create_graph_svc
from prepare_data import prepare_data
from pathlib import Path


def generate_model_card(xtest: str, ytest: str, path_to_model_file: str, path_to_push_html: str):
    X_test = pd.read_csv(xtest)
    y_test = pd.read_csv(ytest)

    model_card_output_path = f'{os.path}'.replace(os.path.basename(sys.argv[0]), '')
    mct = mctlib.ModelCardToolkit(model_card_output_path)
    model_card = mct.scaffold_assets()
    model_card.model_details.name = 'Bank Customer Churn Prediction'
    model_card.model_details.overview = (
        'Based on this model, the quality of our customers will be assessed. (What is the estimated churn of our customers) image statistic')
    model_card.model_details.owners = [
        mctlib.Owner(name='DS engineer', contact='lyabomy@gmail.com')]
    model_card.model_details.references = [
        mctlib.Reference(
            reference='https://www.kaggle.com/datasets/shantanudhakadd/bank-customer-churn-prediction/code'),
        mctlib.Reference(
            reference='https://learn.microsoft.com/en-us/dynamics365/industry/financial-services/churn-prediction')
    ]
    model_card.model_details.version.name = str(uuid.uuid4())
    model_card.model_details.version.date = str(date.today())
    model_card.considerations.ethical_considerations = [mctlib.Risk(
        name=('The client may leave for his own reasons that cannot be predicted'),
        mitigation_strategy='need to increase recall'
    )]

    model_card.considerations.limitations = [mctlib.Limitation(description='Determination of client reliability')]
    model_card.considerations.use_cases = [mctlib.UseCase(description='Determination of client reliability')]
    model_card.considerations.users = [mctlib.User(description='marketing team'),
                                       mctlib.User(description='analytic team'),
                                       mctlib.User(description='manager team')]
    model_card.model_parameters.data.append(mctlib.Dataset())
    model_card.model_parameters.data[0].graphics.description = (
        f'{len(X_test)} rows with {len(X_test.columns)} features')
    model_card.model_parameters.data[0].graphics.collection = [
        mctlib.Graphic(image=create_graph_importance(X_test, path_to_model_file))]
    model_card.quantitative_analysis.graphics.description = (
        'ROC curve and confusion matrix')
    model_card.quantitative_analysis.graphics.collection = [
        mctlib.Graphic(image=create_confusion_matrix(X_test, y_test, path_to_model_file)),
        mctlib.Graphic(image=create_graph_svc(X_test, y_test, path_to_model_file))]

    mct.update_model_card(model_card)
    html = mct.export_format()
    with open(Path(path_to_push_html) / 'card.html', "wt") as f:
        f.write(html)


if __name__ == '__main__':
    typer.run(generate_model_card)
