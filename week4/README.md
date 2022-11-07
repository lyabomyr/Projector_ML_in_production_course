for deploy kubflow
1. Create cluster
```
kind create cluster --name ml-in-production-course-week-4
```
2.Download yaml file or generate yml file used kustomize
for generate yml file:
```
 mkdir kfp-yml
 export PIPELINE_VERSION=1.8.5
 kubectl kustomize "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION" > kfp-yml/res.yaml
 kubectl kustomize "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION" > kfp-yml/pipelines.yaml
```
or download yaml file from kubflow:
```
 mkdir kfp-yml
 export PIPELINE_VERSION=1.8.5
 kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
 kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
 kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"
```

3. deploy kubflow in kubernetes used downloaded yml files:
```
kubectl create -f kfp-yml/res.yaml
kubectl create -f kfp-yml/pipelines.yaml
```
4. Access to UI and MINIO (wake up ports)
```
kubectl port-forward --address=0.0.0.0 svc/minio-service 9000:9000 -n kubeflow
```
("For login to minio use credention from pipelines.yaml in kind secret {stringData:}")
```
kubectl port-forward --address=0.0.0.0 svc/ml-pipeline-ui 8888:80 -n kubeflow
```

For run upload pypline use command:
```
python3 kfp_train_pipeline.py http://0.0.0.0:8888
```

Then:
 1. open pipline link http://0.0.0.0:8888
 2. click on create pipeline> create run > add run to experiment> create run
 3. go to run and check logs


Deploy AirFlow 
 ```
  mkdir airflow-home
  export AIRFLOW_HOME=$PWD/airflow-home
  AIRFLOW_VERSION=2.4.1
  PYTHON_VERSION="$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
  CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
  pip3 install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
  airflow standalone
 ```
 tranfer by link http://0.0.0.0:8080 and login with credention which showed in standalone logs
# Inside airflow.cfg
enable_xcom_pickling = True  # needed for Great Expectations airflow provider
load_examples = False  # don't clutter webserver with examples
```
 airflow db reset -y
 airflow db init
 airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org
```
```
airflow webserver --port 8080
airflow scheduler
```
set configuration for kubernetis pods in airflow
go to link http://0.0.0.0:8080>>login>>Admin(tab)>>Connection>>select kubernetes config>>click Edit
Edit kubeConfigPath(ls ~/.kube/config >> example "/home/lubomir/.kube/config") and add namespace (ex: "default")
