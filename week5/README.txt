Deploy FastAPI on Deta
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
```
kubectl port-forward  --address 0.0.0.0 -n ambassador svc/ambassador 7777:80
```

run custom yaml file:
go to swager
http://localhost:7777/seldon/default/churnpredict/api/v1.0/doc/#/

curl request

```
curl -X POST "http://localhost:7777/seldon/default/churnpredict/api/v1.0/predictions" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"data\":{\"ndarray\":[[619, 1, 0, 42, 2, 0.0, 1, 1, 1, 101348.88]]}}"
```


For run seldon u can use:
    https://docs.seldon.io/projects/seldon-core/en/latest/install/kind.html