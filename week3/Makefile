test:
	 cd ml_decision_tree_sample/unit_tests/;pytest
test_code:
	cd ml_decision_tree_sample/unit_tests/; pytest test_code.py
test_model:
	cd ml_decision_tree_sample/unit_tests/; pytest test_model.py
test_data:
	cd ml_decision_tree_sample/unit_tests/; pytest test_data.py
train:
	cd ml_decision_tree_sample/; python3 train.py
model_card_generator:
	cd ml_decision_tree_sample/; python3 python3 generator_model_card.py
build_test:
	docker build -f Dockerfile -t test_project:latest
run_dev: build_test
	docker run -it -v ${PWD}:/main test_project:latest /bin/bash
