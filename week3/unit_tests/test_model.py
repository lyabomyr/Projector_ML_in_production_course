import pytest
import os
from predictor import model_for_predict
from prepare_data import prepare_data
from generator_model_card import generate_model_card
from pytestconf import conf_test

def test_overfit_batch():
    clf = model_for_predict(max_depth=11, min_samples_leaf=3, min_samples_split=2,
                            n_estimators=30,
                            random_state=42, patch_to_file= conf_test.file_with_short_data)
    predicted_y = clf.predict(prepare_data(conf_test.file_with_short_data)[0]['x'])
    test_y = prepare_data(conf_test.file_with_short_data)[0]['y'].to_numpy()
    assert (predicted_y == test_y).all(), 'model not work'

def test_model_card_to_completion():
    generate_model_card(conf_test.model_card)
    assert os.path.exists(conf_test.model_file_html_name), f'{conf_test.model_file_html_name} are not created '
    os.remove(conf_test.model_file_html_name)

