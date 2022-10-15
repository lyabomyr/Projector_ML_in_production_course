import hydra
from omegaconf import DictConfig
import os, sys
import model_card_toolkit as mctlib
import uuid
from datetime import date
from predictor import create_confusion_matrix, create_graph_importance, create_graph_svc
from prepare_data import prepare_data


def generate_model_card(cfg: DictConfig):
    X_test = prepare_data(cfg.patch_to_file)[1]['x']
    model_card_output_path = os.getcwd()
    mct = mctlib.ModelCardToolkit(model_card_output_path)
    model_card = mct.scaffold_assets()
    model_card.model_details.name = cfg.name
    model_card.model_details.overview = (cfg.model_card_overview)
    model_card.model_details.owners = [
        mctlib.Owner(name=cfg.owner_name, contact=cfg.owner_contact)]
    model_card.model_details.references = [
        mctlib.Reference(
            reference=cfg.reference1),
        mctlib.Reference(
            reference=cfg.reference2)
    ]
    model_card.model_details.version.name = str(uuid.uuid4())
    model_card.model_details.version.date = str(date.today())
    model_card.considerations.ethical_considerations = [mctlib.Risk(
        name=(cfg.risk_name),
        mitigation_strategy=cfg.risk_mitigation_strategy
    )]

    model_card.considerations.limitations = [mctlib.Limitation(description=cfg.limitation)]
    model_card.considerations.use_cases = [mctlib.UseCase(description=cfg.consider_use_cases)]
    model_card.considerations.users = [mctlib.User(description=cfg.consider_user1),
                                       mctlib.User(description=cfg.consider_user2),
                                       mctlib.User(description=cfg.consider_user3)]
    model_card.model_parameters.data.append(mctlib.Dataset())
    model_card.model_parameters.data[0].graphics.description = (
        f'{len(X_test)} rows with {len(X_test.columns)} features')
    model_card.model_parameters.data[0].graphics.collection = [
        mctlib.Graphic(image=create_graph_importance(cfg.max_depth, cfg.min_samples_leaf,
                                                     cfg.min_samples_split, cfg.n_estimators,
                                                     cfg.random_state, cfg.patch_to_file))]
    model_card.quantitative_analysis.graphics.description = (
        'ROC curve and confusion matrix')
    model_card.quantitative_analysis.graphics.collection = [
        mctlib.Graphic(image=create_confusion_matrix(cfg.max_depth, cfg.min_samples_leaf,
                                                     cfg.min_samples_split, cfg.n_estimators,
                                                     cfg.random_state, cfg.patch_to_file)),
        mctlib.Graphic(image=create_graph_svc(cfg.max_depth, cfg.min_samples_leaf,
                                              cfg.min_samples_split, cfg.n_estimators,
                                              cfg.random_state, cfg.patch_to_file))]

    mct.update_model_card(model_card)
    html = mct.export_format()
    with open(cfg.model_card_html_name, "wt") as f:
        f.write(html)


@hydra.main(version_base=None, config_path="conf", config_name="model_card")
def start_generate_model_card(cfg: DictConfig):
    generate_model_card(cfg)
    print('done')


if __name__ == '__main__':
    start_generate_model_card()
