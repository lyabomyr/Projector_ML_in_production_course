For download minio image used command
---- docker pull minio/minio
And next run container  with available logs
docker run   -p 9000:9000   -p 9001:9001   --name minio1   -e "MINIO_ROOT_USER=testkey"   -e "MINIO_ROOT_PASSWORD=testsecret" -v /home/dev/mdata:/data   quay.io/minio/minio server /data --console-address ":9001"



For running in kubernetis
first create cluster:
(U can use kind or minicube)
kind create cluster --name ml-in-production-course-week-2

then running deploy job

kubectl create -f minio_service/minio_deploy.yml

in this file we have 4 job 1. Create storage (PersistentVolumeClaim),
2. Create Service for api communication
3. Create Service for ui communication
4. Forward storage for ui

then do forwarding ports: <  kubectl port-forward svc/minio-api 9000:9000  >





