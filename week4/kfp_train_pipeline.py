import os
import uuid
from typing import Optional
import kfp
import typer
from kfp import dsl
from kubernetes.client.models import V1EnvVar


IMAGE = 'lyabomyr/kfp_train:latest'
WANDB_PROJECT = 'liunomyr'
WANDB_API_KEY = '0a14fd83112d8258ad9cb780edb9e9932241f5fc'


@dsl.pipeline(name="ml_retraining_pipeline", description="ml_retraining_pipeline")
def ml_retraining_pipeline():
    load_data = dsl.ContainerOp(
        name="load_data",
        command="python3 ml_decision_tree_sample/prepare_data.py Churn_Modelling.csv /tmp/".split(),
        image=IMAGE,
        file_outputs={"X_train": "/tmp/X_train.csv", "y_train": "/tmp/y_train.csv", "X_test": "/tmp/X_test.csv",
                      "y_test": "/tmp/y_test.csv"}
    )
    load_data.execution_options.caching_strategy.max_cache_staleness = "P0D"
    train_model = dsl.ContainerOp(
        name="train_model ",
        command="python3 ml_decision_tree_sample/train.py /tmp/X_train.csv /tmp/y_train.csv /tmp/".split(),
        image=IMAGE,
        artifact_argument_paths=[
            dsl.InputArgumentPath(load_data.outputs["X_train"], path="/tmp/X_train.csv"),
            dsl.InputArgumentPath(load_data.outputs["y_train"], path="/tmp/y_train.csv"),
        ],
        file_outputs={"model": "/tmp/model_random_forest.pkl"}
    )
    upload_model = dsl.ContainerOp(
        name="upload_model",
        command="python3 ml_decision_tree_sample/load_model.py upload model_random_forest.pkl /tmp/".split(),
        image=IMAGE,
        artifact_argument_paths=[
            dsl.InputArgumentPath(train_model.outputs["model"], path="/tmp/model_random_forest.pkl"),
        ],
    )

    env_var_project = V1EnvVar(name="WANDB_PROJECT", value=WANDB_PROJECT)
    upload_model = upload_model.add_env_variable(env_var_project)

    env_var_password = V1EnvVar(name="WANDB_API_KEY", value=WANDB_API_KEY)
    upload_model = upload_model.add_env_variable(env_var_password)


def compile_pipeline() -> str:
    path = "ml_traininig_pipeline.yaml"
    kfp.compiler.Compiler().compile(ml_retraining_pipeline, path)
    return path


def create_pipeline(client: kfp.Client, namespace: str):
    print("Creating experiment")
    _ = client.create_experiment("training", namespace=namespace)
    print("Uploading pipeline")
    name = "ml-sample-training"
    if client.get_pipeline_id(name) is not None:
        print("Pipeline exists - upload new version.")
        pipeline_prev_version = client.get_pipeline(client.get_pipeline_id(name))
        version_name = f"{name}-{uuid.uuid4()}"
        pipeline = client.upload_pipeline_version(
            pipeline_package_path=compile_pipeline(),
            pipeline_version_name=version_name,
            pipeline_id=pipeline_prev_version.id,
        )
    else:
        pipeline = client.upload_pipeline(pipeline_package_path=compile_pipeline(), pipeline_name=name)
    print(f"pipeline {pipeline.id}")


def auto_create_pipelines(
        host: str,
        namespace: Optional[str] = None,
):
    client = kfp.Client(host=host)
    create_pipeline(client=client, namespace=namespace)


if __name__ == "__main__":
    typer.run(auto_create_pipelines)
