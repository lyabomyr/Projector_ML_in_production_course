import pandas as pd
import os
print(os.path.abspath("Churn_Modelling.csv"))

path_to_train_file = os.path.abspath("Churn_Modelling.csv").replace('/week3/ml_decision_tree_sample ', '')
print(path_to_train_file)
pd.read_csv(path_to_train_file)
