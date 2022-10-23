import wandb


def model_loader(mode: str, model_name: str):
    with wandb.init() as run:
        if mode == 'upload':
            artifact = wandb.Artifact(model_name, type='model')
            artifact.add_file(model_name)
            run.log_artifact(artifact)
        else:
            artifact = run.use_artifact(f'{model_name}:latest', type="model")
            artifact = artifact.get_path(model_name)
            artifact.download(root='.')



# model_loader('download','model_random_forest')