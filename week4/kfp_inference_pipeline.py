import os
import uuid
from typing import Optional
import kfp
import typer
from kfp import dsl
from kubernetes.client.models import V1EnvVar
from config import image, wandb_project, wandb_api_key

IMAGE = image
WANDB_PROJECT = wandb_project
WANDB_API_KEY = wandb_api_key


@dsl.pipeline(name="ml_inference_pipeline", description="ml_inference_pipeline")
def ml_retraining_pipeline():
    load_data = dsl.ContainerOp(
        name="load_data",
        command="python3 ml_decision_tree_sample/prepare_data.py Churn_Modelling.csv /tmp/".split(),
        image=IMAGE,
        file_outputs={"X_train": "/tmp/X_train.csv", "y_train": "/tmp/y_train.csv", "X_test": "/tmp/X_test.csv",
                      "y_test": "/tmp/y_test.csv"}
    )
    load_data.execution_options.caching_strategy.max_cache_staleness = "P0D"
    download_model = dsl.ContainerOp(
        name="upload_model",
        command="python3 ml_decision_tree_sample/load_model.py download model_random_forest.pkl /tmp/".split(),
        image=IMAGE,
        file_outputs={"model": "/tmp/model_random_forest.pkl"}
    )
    download_model.execution_options.caching_strategy.max_cache_staleness = "P0D"

    predict_by_model = dsl.ContainerOp(
        name="predict_model ",
        command="python3 ml_decision_tree_sample/predictor.py /tmp/model_random_forest.pkl /tmp/X_test.csv "
                "/tmp/y_test.csv /tmp/".split(),
        image=IMAGE,
        artifact_argument_paths=[
            dsl.InputArgumentPath(load_data.outputs["X_test"], path="/tmp/X_test.csv"),
            dsl.InputArgumentPath(download_model.outputs["model"], path="/tmp/model_random_forest.pkl"),
            dsl.InputArgumentPath(load_data.outputs["y_test"], path="/tmp/y_test.csv"),
        ],
        file_outputs={
            "predict": "/tmp/predict.csv",
        },
    )
    create_model_card = dsl.ContainerOp(
        name="create_model_card ",
        command="python3 ml_decision_tree_sample/generator_model_card.py /tmp/X_test.csv /tmp/y_test.csv /tmp/model_random_forest.pkl /tmp".split(),
        image=IMAGE,
        artifact_argument_paths=[
            dsl.InputArgumentPath(load_data.outputs["X_test"], path="/tmp/X_test.csv"),
            dsl.InputArgumentPath(load_data.outputs["y_test"], path="/tmp/y_test.csv"),
            dsl.InputArgumentPath(download_model.outputs["model"], path="/tmp/model_random_forest.pkl")
        ],
        file_outputs={
            "predict": "/tmp/card.html",
        },
    )

    env_var_project = V1EnvVar(name="WANDB_PROJECT", value=WANDB_PROJECT)
    upload_model = download_model.add_env_variable(env_var_project)

    env_var_password = V1EnvVar(name="WANDB_API_KEY", value=WANDB_API_KEY)
    upload_model = download_model.add_env_variable(env_var_password)


def compile_pipeline() -> str:
    path = "ml_traininig_pipeline.yaml"
    kfp.compiler.Compiler().compile(ml_retraining_pipeline, path)
    return path


def create_pipeline(client: kfp.Client, namespace: str):
    print("Creating experiment")
    _ = client.create_experiment("inference", namespace=namespace)
    print("Uploading pipeline")
    name = "ml-sample-inference"
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
