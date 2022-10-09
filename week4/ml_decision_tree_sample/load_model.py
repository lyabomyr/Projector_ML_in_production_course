import wandb
import typer
from pathlib import Path



def model_loader(mode:str ,model_name:str , model_path: str):
    with wandb.init() as run:
        if mode == 'upload':
            artifact = wandb.Artifact(model_name, type='model')
            artifact.add_file(Path(model_path) / model_name)
            run.log_artifact(artifact)
        else:
            artifact = run.use_artifact(f'{model_name}:latest', type="model")
            artifact_dir = artifact.download(root=model_path)
            print(f"{artifact_dir}")

if __name__ == '__main__':
    typer.run(model_loader)

