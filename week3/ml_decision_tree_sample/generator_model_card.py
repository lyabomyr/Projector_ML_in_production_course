import hydra
from omegaconf import DictConfig
import os
import model_card_toolkit as mctlib
import uuid
from datetime import date
from predictor import create_confusion_matrix, create_graph_importance, create_graph_svc
from prepare_data import prepare_data

@hydra.main(version_base=None, config_path="conf", config_name="model_card")
def generate_model_card(cfg: DictConfig):
    X_test = prepare_data(cfg.patch.train_file)[1]['x']
    model_card_output_path = f'{os.path}'.replace('generator_model_card.py', '')
    mct = mctlib.ModelCardToolkit(model_card_output_path)
    model_card = mct.scaffold_assets()
    model_card.model_details.name = cfg.modcard.name
    model_card.model_details.overview = (cfg.modcard.model_card_overview)
    model_card.model_details.owners = [
        mctlib.Owner(name=cfg.modcard.owner_name, contact=cfg.modcard.owner_contact)]
    model_card.model_details.references = [
        mctlib.Reference(
            reference=cfg.modcard.reference1),
        mctlib.Reference(
            reference=cfg.modcard.reference2)
    ]
    model_card.model_details.version.name = str(uuid.uuid4())
    model_card.model_details.version.date = str(date.today())
    model_card.considerations.ethical_considerations = [mctlib.Risk(
        name=(cfg.modcard.risk_name),
        mitigation_strategy= cfg.modcard.risk_mitigation_strategy
    )]

    model_card.considerations.limitations = [mctlib.Limitation(description= cfg.modcard.limitation)]
    model_card.considerations.use_cases = [mctlib.UseCase(description= cfg.modcard.consider_use_cases)]
    model_card.considerations.users = [mctlib.User(description=cfg.modcard.consider_user1),
                                       mctlib.User(description=cfg.modcard.consider_user2),
                                       mctlib.User(description=cfg.modcard.consider_user3)]
    model_card.model_parameters.data.append(mctlib.Dataset())
    model_card.model_parameters.data[0].graphics.description = (
         f'{len(X_test)} rows with {len(X_test.columns)} features')
    model_card.model_parameters.data[0].graphics.collection = [
        mctlib.Graphic(image=create_graph_importance(cfg.param.max_depth,cfg.param.min_samples_leaf,
                                                     cfg.param.min_samples_split,cfg.param.n_estimators,
                                                     cfg.param.random_state,cfg.patch.train_file))]

    model_card.quantitative_analysis.graphics.description = (
         'ROC curve and confusion matrix')
    model_card.quantitative_analysis.graphics.collection = [
         mctlib.Graphic(image=create_confusion_matrix(cfg.param.max_depth,cfg.param.min_samples_leaf,
                                                     cfg.param.min_samples_split,cfg.param.n_estimators,
                                                     cfg.param.random_state,cfg.patch.train_file)),
         mctlib.Graphic(image=create_graph_svc(cfg.param.max_depth,cfg.param.min_samples_leaf,
                                                     cfg.param.min_samples_split,cfg.param.n_estimators,
                                                     cfg.param.random_state,cfg.patch.train_file))]

    mct.update_model_card(model_card)
    html = mct.export_format()
    with open(cfg.modcard.model_card_html_name, "wt") as f:
        f.write(html)


generate_model_card()
