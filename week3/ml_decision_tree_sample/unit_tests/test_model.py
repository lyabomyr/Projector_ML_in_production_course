import sys, os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname('ml_decision_tree_sample'), '..')))
from predictor import model_for_predict
from prepare_data import prepare_data
from generator_model_card import generate_model_card


def test_overfit_batch():
    clf = model_for_predict(max_depth=11, min_samples_leaf=3, min_samples_split=2,
                            n_estimators=30,
                            random_state=42, patch_to_file='short_test_data.csv')
    predicted_y = clf.predict(prepare_data('short_test_data.csv')[0]['x'])
    test_y = prepare_data('short_test_data.csv')[0]['y'].to_numpy()
    assert (predicted_y == test_y).all(), 'model not work'


def test_model_card_to_completion():
    generate_model_card(max_depth=11, min_samples_leaf=3,
                        min_samples_split=2,
                        n_estimators=30,
                        random_state=42, patch_to_file='short_test_data.csv',
                        name='test', model_card_overview='test1',
                        owner_name='test2', owner_contact='test3',
                        reference1='test4', reference2='test5',
                        risk_name='test5',
                        risk_mitigation_strategy='test6',
                        limitation='test7',
                        consider_use_cases='test8',
                        consider_user1='test9',
                        consider_user2='test10',
                        consider_user3='test11',
                        model_card_html_name='card.html'
                        )
    assert os.path.exists('card.html'), 'card.html are not created '
    os.remove('card.html')

