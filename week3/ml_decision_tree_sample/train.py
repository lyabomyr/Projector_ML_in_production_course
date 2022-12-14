import hydra
from omegaconf import DictConfig
import sklearn
import wandb
from sklearn.ensemble import RandomForestClassifier
from prepare_data import prepare_data

def init_connect(train_file, common_range):
    prepared_data = prepare_data(train_file)
    parange = common_range
    wandb.init(project="ml_week3", entity="liunomyr")
    wandb.define_metric("train/step")
    X_train = prepared_data[0]['x']
    X_test = prepared_data[1]['x']
    y_train = prepared_data[0]['y']
    y_test = prepared_data[1]['y']
    for max_depth in range(1, parange):
        for min_samples_leaf in range(1, parange, 2):
            for min_samples_split in range(2, parange, 3):
                for n_estimators in range(2, parange, 4):
                    enumeration_of_parameters(X_train, X_test, y_train, y_test, max_depth,min_samples_leaf,min_samples_split,n_estimators)


def enumeration_of_parameters(X_train, X_test, y_train, y_test, max_depth,min_samples_leaf,min_samples_split,n_estimators):
    clf = RandomForestClassifier(max_depth=max_depth, min_samples_leaf=min_samples_leaf,
                                                 min_samples_split=min_samples_split,
                                                 n_estimators=n_estimators, random_state=0)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    if sklearn.metrics.precision_score(y_test, y_pred) > 0.7:
        wandb.log({
                    "precision": sklearn.metrics.precision_score(y_test, y_pred, zero_division=0),
                    "recall": sklearn.metrics.recall_score(y_test, y_pred, zero_division=0),
                    "f1_score": sklearn.metrics.f1_score(y_test, y_pred, zero_division=0),
                    "accuracy": sklearn.metrics.accuracy_score(y_test, y_pred),
                    "train data": {"max_depth": max_depth, "min_samples_leaf": min_samples_leaf,
                                   "min_samples_split": min_samples_split,
                                   "n_estimators": n_estimators}
                        })
@hydra.main(version_base=None, config_path="conf", config_name="train")
def run_train(cfg: DictConfig):
    init_connect(cfg.path.train_file, cfg.range_parametrs.common_range,)

if __name__ == '__main__':
    run_train()