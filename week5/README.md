#### Deploy FastAPI on Deta
Install the CLI¶
```
curl -fsSL https://get.deta.dev/cli.sh | sh
```

 open new shell and put command in derictiry with main.pt file
 ```
 deta --help
 dete login
 deta new
 ```
 open endpoint URL from json in terminal


install seldon

Configure and install ambassador

```
kind create cluster --name seldonapp
kubectl create namespace seldon-system
kubectl apply -f https://github.com/datawire/ambassador-operator/releases/latest/download/ambassador-operator-crds.yaml
kubectl apply -n ambassador -f https://github.com/datawire/ambassador-operator/releases/latest/download/ambassador-operator-kind.yaml
kubectl wait --timeout=180s -n ambassador --for=condition=deployed ambassadorinstallations/ambassador
```
Next install seldon-core
```
kubectl create namespace seldon-system
helm install seldon-core seldon-core-operator \
    --repo https://storage.googleapis.com/seldon-charts \
    --set usageMetrics.enabled=true \
    --set ambassador.enabled=true \
    --namespace seldon-system
```
Port Forward:
```kubectl port-forward  --address 0.0.0.0 -n ambassador svc/ambassador 7777:80
```

run custom yaml file:
go to swager
http://localhost:7777/seldon/default/churnpredict/api/v1.0/doc/#/

curl request

```curl -X POST "http://localhost:7777/seldon/default/churnpredict/api/v1.0/predictions" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"data\":{\"ndarray\":[[619, 1, 0, 42, 2, 0.0, 1, 1, 1, 101348.88]]}}"
```
For run seldon u can use:
```
https://docs.seldon.io/projects/seldon-core/en/latest/install/kind.html
```


### DEPLOYMENT kubernetis  YAML files
create cluster:
```kind create cluster --name fastapindstreamlit
```

deploy fast-api yaml file:
```
kubectl apply -f week5/k8s/fast-api-service.yaml
kubectl port-forward service/fastapi-service 8081:8000
```

deploy  streamlit
```
kubectl apply -f week5/k8s/streamlite-service.yaml
kubectl port-forward service/streamlite-service 8081:8000
```

Run local benchmark test:

```
python3 week5/serving/fast_api.py
locust -f week5/unit_tests/locust_test_benchmark.py --headless --host http://0.0.0.0:8000 -r 1 -u 10 --run-time 5m
```

### TEST benchmark batch predict

```
Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
POST     /batch_predict_csv_file/                                                         404     0(0.00%) |    144      99     323    130 |    1.68        0.00
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                       404     0(0.00%) |    144      99     323    130 |    1.68        0.00

Response time percentiles (approximated)
Type     Name                                                                                  50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
--------|--------------------------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
POST     /batch_predict_csv_file/                                                              130    150    170    180    210    240    270    300    320    320    320    404
--------|--------------------------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
         Aggregated                                                                            130    150    170    180    210    240    270    300    320    320    320    404
```

Test set up:

```
OS: Ubuntu 20.04.5 LTS x86_64
Host: 20L50002RT ThinkPad T480
Kernel: 5.13.0-28-generic
Uptime: 2 days, 22 hours, 26 mins
Shell: bash 5.0.17
CPU: Intel i5-8250U (8) @ 3.400GHz
GPU: Intel UHD Graphics 620
Memory: 13529MiB / 23806MiB
```

### PR BENCHMARK for model forward pass

for check bechmark use next command:

```
pytest week5/unit_tests/test_benchmark-forwardpass.py
```
result:
```
------------------------------------------------------------------------------------------------------- benchmark: 2 tests -------------------------------------------------------------------------------------------------------
Name (time in ms)                                       Min                    Max                  Mean              StdDev                 Median                 IQR            Outliers      OPS            Rounds  Iterations
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_benchmark_port_forwarding_batch_predict        50.1079 (1.0)         126.3824 (1.0)         68.4082 (1.0)       23.2159 (1.0)          57.2554 (1.0)       27.4293 (1.0)           2;2  14.6181 (1.0)          19           1
test_load_file                                   9,675.8480 (193.10)   10,133.3141 (80.18)    9,915.8369 (144.95)   213.4681 (9.19)     10,035.8939 (175.28)   370.2745 (13.50)         3;0   0.1008 (0.01)          5           1
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```


#### PR optimizing inference for your model

```
FOR run optimozation inference_process_pool
In this case, on the current volume of data, inferrence optimization is not needed,
but if in the future our users will upload large csv files, then this optimization will be useful
```

-------------------------------------------------- benchmark: 1 tests --------------------------------------------------
Name (time in ms)               Min       Max      Mean  StdDev    Median      IQR  Outliers     OPS  Rounds  Iterations
------------------------------------------------------------------------------------------------------------------------
test_optimized_predict     219.1527  243.4966  233.9585  9.7740  234.9246  14.4210       1;0  4.2743       5           1
------------------------------------------------------------------------------------------------------------------------
