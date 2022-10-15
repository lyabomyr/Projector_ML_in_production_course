from dotmap import DotMap


class conf_test:
    model_file_html_name = 'card.html'
    file_with_short_data = "short_test_data.csv"
    real_data_file = "Churn_Modelling.csv"

    model_card = DotMap({"max_depth": 11,
                  "min_samples_leaf": 3,
                  "min_samples_split": 2,
                  "n_estimators": 30,
                  "random_state": 42,
                  "patch_to_file": "short_test_data.csv",
                  "name": "test",
                  "model_card_overview": "test1",
                  "owner_name": "test2",
                  "owner_contact": "test3",
                  "reference1": "test4",
                  "reference2": "test5",
                  "risk_name": "test5",
                  "risk_mitigation_strategy": "test6",
                  "limitation": "test7",
                  "consider_use_cases": "test8",
                  "consider_user1": "test9",
                  "consider_user2": "test10",
                  "consider_user3": "test11",
                  "model_card_html_name": "card.html"})

