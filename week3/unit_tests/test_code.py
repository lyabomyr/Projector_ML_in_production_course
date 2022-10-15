from prepare_data import prepare_data
from predictor import model_for_predict
from pytestconf import conf_test
import pandas.api.types as ptypes



def test_prepare_data():
    prepared_data = prepare_data(conf_test.file_with_short_data)
    assert type(prepared_data) == list, ' data is not  list'
    assert len(prepared_data) == 2, 'result prepare data haven\' 2 elements'
    assert type(prepared_data[0]) == dict, 'first element in list is not a dict'
    assert type(prepared_data[1]) == dict, 'second element in list is not a dict'
    assert type(prepared_data[1]) == dict, 'second element in list is not a dict'
    assert ptypes.is_integer_dtype(prepared_data[0]['x'].Gender_Male), 'Gender_Male column are not  integer type'
    assert ptypes.is_integer_dtype(prepared_data[0]['x'].Gender_Female), 'Gender_Female column are not integer type'
    assert ptypes.is_integer_dtype(prepared_data[0]['x'].Geography_Spain), 'Geography_Spain column are not integer type'
    assert ptypes.is_integer_dtype(
        prepared_data[0]['x'].Geography_Germany), 'Geography_Germany column are not integer type'
    assert ptypes.is_integer_dtype(
        prepared_data[0]['x'].Geography_France), 'Geography_France column are not integer type'
    assert ptypes.is_integer_dtype(prepared_data[0]['x'].IsActiveMember), 'IsActiveMember column are not integer type'
    assert ptypes.is_integer_dtype(prepared_data[0]['x'].Age), 'Age column are not integer type'

def test_predict_function():
    clf = model_for_predict(max_depth=11, min_samples_leaf=3, min_samples_split=2,
                            n_estimators=30,
                            random_state=42, patch_to_file=conf_test.file_with_short_data)
    assert clf is not None, 'CLF returned None'
