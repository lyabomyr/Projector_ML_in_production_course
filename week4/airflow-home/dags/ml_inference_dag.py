from datetime import datetime
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import models as k8s
from config import image, wandb_project, wandb_api_key

IMAGE = image
volume = k8s.V1Volume(
    name="inference-storage",
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name="inference-storage"),
)
volume_mount = k8s.V1VolumeMount(name="inference-storage", mount_path="/tmp/", sub_path=None)

with DAG(start_date=datetime(2021, 1, 1),
         catchup=False, schedule_interval=None, dag_id="inference_dag") as dag:

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

    load_model = KubernetesPodOperator(
        name="load_model",
        image=IMAGE,
        cmds=["python3", "ml_decision_tree_sample/load_model.py", "download", "model_random_forest.pkl", "/tmp/"],
        task_id="load_model",
        env_vars={"WANDB_PROJECT": wandb_project, "WANDB_API_KEY": wandb_api_key},
        in_cluster=False,
        namespace="default",
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

    predict_by_model = KubernetesPodOperator(
        name="predict_by_model",
        image=IMAGE,
        cmds=["python3", "ml_decision_tree_sample/predictor.py", "/tmp/model_random_forest.pkl", "/tmp/X_test.csv", "/tmp/y_test.csv","/tmp/"],
        task_id="predict_by_model",
        in_cluster=False,
        namespace="default",
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

    generate_model_card = KubernetesPodOperator(
        name="generate_model_card",
        image=IMAGE,
        cmds=["python3", "ml_decision_tree_sample/predictor.py", "/tmp/model_random_forest.pkl", "/tmp/X_test.csv",
              "/tmp/y_test.csv", "/tmp/"],
        task_id="generate_model_card",
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

    load_data >> load_model >> predict_by_model >> generate_model_card >> clean_up