from datetime import datetime
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import models as k8s
from config import image, wandb_project, wandb_api_key

IMAGE = image
volume = k8s.V1Volume(name="training-storage",
                      persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name="training-storage"), )
volume_mount = k8s.V1VolumeMount(name="training-storage", mount_path="/tmp/", sub_path=None)

with DAG(start_date=datetime(2021, 1, 1),
         catchup=False, schedule_interval=None, dag_id="training_dag") as dag:
    load_data = KubernetesPodOperator(
        name="load_data",
        image=IMAGE,
        cmds=["python3", "ml_decision_tree_sample/prepare_data.py", "Churn_Modelling.csv", "/tmp/"],
        task_id="load_data",
        in_cluster=False,
        namespace="default",
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

    train_model = KubernetesPodOperator(
        name="train_model",
        image=IMAGE,
        cmds=["python3", "ml_decision_tree_sample/train.py", "/tmp/X_train.csv", "/tmp/y_train.csv", "/tmp/"],
        task_id="train_model",
        in_cluster=False,
        namespace="default",
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

    upload_model = KubernetesPodOperator(
        name="upload_model",
        image=IMAGE,
        cmds=["python3", "ml_decision_tree_sample/load_model.py", "upload", "model_random_forest.pkl", "/tmp/"],
        task_id="upload_model",
        env_vars={"WANDB_PROJECT": wandb_project, "WANDB_API_KEY": wandb_api_key},
        in_cluster=False,
        namespace="default",
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

    clean_up = KubernetesPodOperator(
        name="clean_up",
        image=IMAGE,
        cmds=["rm", "-rf", "/tmp/*"],
        task_id="clean_up",
        in_cluster=False,
        namespace="default",
        volumes=[volume],
        volume_mounts=[volume_mount],
        trigger_rule="all_done",
    )

    # clean_storage_before_start >>\
    load_data >> train_model >> upload_model >> clean_up
