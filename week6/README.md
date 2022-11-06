# **Model Monitoring**

## Setup cluster

### Create cluster with custom config 

`kind create cluster --name model-monitoring
`
_Seldon model monitoring_

### Setup local seldon

`
curl -L https://istio.io/downloadIstio | sh -
cd istio-1.15.3
export PATH=$PWD/bin:$PATH
kubectl label namespace default istio-injection=enabled
kubectl apply -f isio_depl_seldon.yaml
kubectl create namespace seldon-system
helm install seldon-core seldon-core-operator \
    --repo https://storage.googleapis.com/seldon-charts \
    --set usageMetrics.enabled=true \
    --set istio.enabled=true \
    --namespace seldon-system
helm install seldon-core-analytics seldon-core-analytics --repo https://storage.googleapis.com/seldon-charts --namespace seldon-system --set executor.user=0 --set executor.port=80 --set engine.port=80.
`
You can check that your Seldon Controller is running by doing:
`kubectl get pods -n seldon-system
`
_Or install using ambasador_

```
 kind create cluster --name model-monitoring --config=k8s/kind.yaml;
 kubectl apply -f https://github.com/datawire/ambassador-operator/releases/latest/download/ambassador-operator-crds.yaml;
 kubectl apply -n ambassador -f https://github.com/datawire/ambassador-operator/releases/latest/download/ambassador-operator-kind.yaml;
 kubectl wait --timeout=180s -n ambassador --for=condition=deployed ambassadorinstallations/ambassador;
 kubectl create namespace seldon-system;
 helm install seldon-core seldon-core-operator \
    --repo https://storage.googleapis.com/seldon-charts \
    --set usageMetrics.enabled=true \
    --set ambassador.enabled=true \
    --namespace seldon-system
 kubectl get pods -n seldon-system
 helm install seldon-core-analytics seldon-core-analytics --repo https://storage.googleapis.com/seldon-charts --namespace seldon-system
```
check that your Seldon Controller is running by doing
``` kubectl get pods -n seldon-system
```



You should see a `seldon-controller-manager` pod with `STATUS=Running.`

Then _Local Port Forwarding_ (`istio, grafana, prometheus`)

Port forwarding for istio
`
kubectl port-forward -n istio-system svc/istio-ingressgateway 8080:80
kubectl port-forward --address 0.0.0.0 -n seldon-system svc/seldon-core-analytics-grafana 3000:80
kubectl port-forward --address 0.0.0.0 -n seldon-system svc/seldon-core-analytics-prometheus-seldon 5000:80
`
Port forwarding for ambassador
```
kubectl port-forward --address 0.0.0.0 -n ambassador svc/ambassador 8000:80
kubectl port-forward --address 0.0.0.0 -n seldon-system svc/seldon-core-analytics-grafana 3000:80
kubectl port-forward --address 0.0.0.0 -n seldon-system svc/seldon-core-analytics-prometheus-seldon 5000:80
```





_go to  http://localhost:3000/ and u can see grafana UI. Default login and password for grafana are (admin and password)._
_go to  http://localhost:5000/ and u can see the UI of the prometheus._

[Prepare code](https://docs.seldon.io/projects/seldon-core/en/latest/python/python_component.html)

build and push container and  wrap container into Kubernetes

`
make wrap_seldon_container_into_kuber 
` 

* check request
`
curl -X POST "http://localhost:8000/seldon/default/churnpredict/api/v1.0/predictions" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"data\":{\"ndarray\":[[619, 1, 0, 42, 2, 0.0, 1, 1, 1, 101348.88]]}}"
`
health request
```curl -X POST http://0.0.0.0:7777/seldon/default/classifier-sample/api/v1.0/feedback -H "accept: application/json" -H "Content-Type: application/json" -d '{"request": "{\"data\":{\"ndarray\":[[619, 1, 0, 42, 2, 0.0, 1, 1, 1, 101348.88]]}}"}, "truth":{"jsonData": {"0": {"0":0}}}'
```
* to open model swagger use:


[http://0.0.0.0:8080/seldon/default/churnpredict/api/v1.0/doc/
](http://0.0.0.0:8080/seldon/default/churnpredict/api/v1.0/doc/)



or run python script with client

`python3 model_monitoring/seldon_client.py
`

##### Configure metrics:


 
##### Setting in Grafana
* go  to http://localhost:3000
* enter default login and password  (default `cred` admin and `password`)
* go to  Create --> Add panel --> Dashboard
* Select Prometheus 
* In the dropdown menu Metrics select metrics my prepared from seldon file
* Then press Apply 

image.png

##### Managed model monitoring tool for  model (Arize)

[info for Arize by link] 
(https://colab.research.google.com/github/Arize-ai/tutorials_python)

Get Arize API_KEY and SPACE_KEY by navigating to the settings page in your workspace


For run loggin use command
`python3 model_monitoring/arize_examle.py
`