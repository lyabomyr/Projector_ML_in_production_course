import wandb

wandb.init(project="ml_week3")

for i in range(10):
    wandb.log = {
        "precision": i+i,
        "recall": i+1,
        "f1_score": i-i+2,
        "accuracy": i+3,
        "clf_parametrs": i+5
    }
    print('complete')
