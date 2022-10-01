import os
import model_card_toolkit as mctlib
import uuid
from datetime import date
from predictor import create_confusion_matrix, create_graph_importance, create_graph_svc
from prepare_data import prepare_data
from io import BytesIO
from matplotlib import pyplot as plt
import base64


def plot_to_str():
    img = BytesIO()
    plt.savefig(img, format='png')
    return base64.encodebytes(img.getvalue()).decode('utf-8')


def generate_model_card():
    model_card_output_path = f'{os.path}'.replace('generator_model_card.py', '')

    mct = mctlib.ModelCardToolkit(model_card_output_path)
    model_card = mct.scaffold_assets()
    model_card.model_details.name = 'Bank Customer Churn Prediction'
    model_card.model_details.overview = (
        'Based on this model, the quality of our customers will be assessed. (What is the estimated churn of our customers)'
        'image statistic')
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

    model_card.considerations.limitations = [mctlib.Limitation(description='Determination of client reliabilit')]
    model_card.considerations.use_cases = [mctlib.UseCase(description='Determination of client reliability')]
    model_card.considerations.users = [mctlib.User(description='marketing team, manager team'),
                                       mctlib.User(description=' analytic team'),
                                       mctlib.User(description='manager team')]

    X_test = prepare_data()[1]['x']

    model_card.model_parameters.data.append(mctlib.Dataset())
    model_card.model_parameters.data[0].graphics.description = (
        f'{len(X_test)} rows with {len(X_test.columns)} features')
    model_card.model_parameters.data[0].graphics.collection = [
        mctlib.Graphic(image=create_graph_importance())]

    model_card.quantitative_analysis.graphics.description = (
        'ROC curve and confusion matrix')
    model_card.quantitative_analysis.graphics.collection = [
        mctlib.Graphic(image=create_confusion_matrix()),
        mctlib.Graphic(image=create_graph_svc())]

    mct.update_model_card(model_card)
    html = mct.export_format()
    with open('card.html', "wt") as f:
        f.write(html)


generate_model_card()
