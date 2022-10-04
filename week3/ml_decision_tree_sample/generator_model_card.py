import hydra
from omegaconf import DictConfig
import os, sys
import model_card_toolkit as mctlib
import uuid
from datetime import date
from predictor import create_confusion_matrix, create_graph_importance, create_graph_svc
from prepare_data import prepare_data


def generate_model_card(max_depth, min_samples_leaf, min_samples_split, n_estimators,
                        random_state, patch_to_file,name, model_card_overview,
                        owner_name,owner_contact, reference1, reference2,
                        risk_name,risk_mitigation_strategy, limitation,consider_use_cases,
                        consider_user1,consider_user2, consider_user3,model_card_html_name):
    X_test = prepare_data(patch_to_file)[1]['x']
    model_card_output_path = f'{os.path}'.replace(os.path.basename(sys.argv[0]), '')
    mct = mctlib.ModelCardToolkit(model_card_output_path)
    model_card = mct.scaffold_assets()
    model_card.model_details.name = name
    model_card.model_details.overview = (model_card_overview)
    model_card.model_details.owners = [
        mctlib.Owner(name=owner_name, contact=owner_contact)]
    model_card.model_details.references = [
        mctlib.Reference(
            reference=reference1),
        mctlib.Reference(
            reference=reference2)
    ]
    model_card.model_details.version.name = str(uuid.uuid4())
    model_card.model_details.version.date = str(date.today())
    model_card.considerations.ethical_considerations = [mctlib.Risk(
        name=(risk_name),
        mitigation_strategy=risk_mitigation_strategy
    )]

    model_card.considerations.limitations = [mctlib.Limitation(description=limitation)]
    model_card.considerations.use_cases = [mctlib.UseCase(description=consider_use_cases)]
    model_card.considerations.users = [mctlib.User(description=consider_user1),
                                       mctlib.User(description=consider_user2),
                                       mctlib.User(description=consider_user3)]
    model_card.model_parameters.data.append(mctlib.Dataset())
    model_card.model_parameters.data[0].graphics.description = (
        f'{len(X_test)} rows with {len(X_test.columns)} features')
    model_card.model_parameters.data[0].graphics.collection = [
        mctlib.Graphic(image=create_graph_importance(max_depth, min_samples_leaf,
                                                     min_samples_split, n_estimators,
                                                     random_state,patch_to_file))]
    model_card.quantitative_analysis.graphics.description = (
        'ROC curve and confusion matrix')
    model_card.quantitative_analysis.graphics.collection = [
        mctlib.Graphic(image=create_confusion_matrix(max_depth, min_samples_leaf,
                                                     min_samples_split, n_estimators,
                                                     random_state, patch_to_file)),
        mctlib.Graphic(image=create_graph_svc(max_depth, min_samples_leaf,
                                              min_samples_split, n_estimators,
                                              random_state, patch_to_file))]

    mct.update_model_card(model_card)
    html = mct.export_format()
    with open(model_card_html_name, "wt") as f:
        f.write(html)


@hydra.main(version_base=None, config_path="conf", config_name="model_card")
def start_generate_model_card(cfg: DictConfig):
    generate_model_card(max_depth=cfg.param.max_depth, min_samples_leaf=cfg.param.min_samples_leaf,
                        min_samples_split=cfg.param.min_samples_split, n_estimators=cfg.param.n_estimators,
                        random_state=cfg.param.random_state, patch_to_file=cfg.patch.train_file,
                        name = cfg.modcard.name, model_card_overview= cfg.modcard.model_card_overview,
                        owner_name= cfg.modcard.owner_name, owner_contact= cfg.modcard.owner_contact,
                        reference1= cfg.modcard.reference1, reference2= cfg.modcard.reference2,
                        risk_name = cfg.modcard.risk_name, risk_mitigation_strategy = cfg.modcard.risk_mitigation_strategy,
                        limitation= cfg.modcard.limitation, consider_use_cases = cfg.modcard.consider_use_cases,
                        consider_user1 = cfg.modcard.consider_user1, consider_user2 = cfg.modcard.consider_user2,
                        consider_user3 =cfg.modcard.consider_user3,
                        model_card_html_name = cfg.modcard.model_card_html_name
                        )
    print('done')


if __name__ == '__main__':
    start_generate_model_card()
