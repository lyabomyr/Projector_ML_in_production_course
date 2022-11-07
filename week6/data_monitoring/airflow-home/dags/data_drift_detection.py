from datetime import datetime
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import models as k8s


volume = k8s.V1Volume(
    name="data-drift-detection",
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name="data-drift-detection"),
)
volume_mount = k8s.V1VolumeMount(name="data-drift-detection", mount_path="/tmp/", sub_path=None)

with DAG(start_date=datetime(2021, 1, 1),
         catchup=False, schedule_interval=None, dag_id="inference_dag") as dag:

    load_files = KubernetesPodOperator(
        name="download-files",
        image="lyabomyr/download-files:latest",
        cmds=["mv", "test.csv", "train.csv", "/tmp/"],
        task_id="load_data",
        in_cluster=False,
        namespace="default",
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

    multivariate_drift_detector = KubernetesPodOperator(
        name="multivariate-drift-detector",
        image="lyabomyr/multivariate-drift-detector:latest",
        cmds=["python3", "detector/multivariate_drift_detection.py","/tmp/train.csv" ,"/tmp/test.csv"],
        task_id="load_model",
        #env_vars={"WANDB_PROJECT": wandb_project, "WANDB_API_KEY": wandb_api_key},
        in_cluster=False,
        namespace="default",
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

    univariate_drift_detector = KubernetesPodOperator(
        name="predict_by_model",
        image='lyabomyr/download-files:latest',
        cmds=["python3", "detector/univariate_drift_detection.py","/tmp/train.csv" ,"/tmp/test.csv"],
        task_id="predict_by_model",
        in_cluster=False,
        namespace="default",
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

    clean_up = KubernetesPodOperator(
        name="clean_up",
        image="lyabomyr/download-files:latest",
        cmds=["rm", "-rf", "/tmp/*"],
        task_id="clean_up",
        in_cluster=False,
        namespace="default",
        volumes=[volume],
        volume_mounts=[volume_mount],
        trigger_rule="all_done",
    )

    load_files >> multivariate_drift_detector >> univariate_drift_detector >> clean_up