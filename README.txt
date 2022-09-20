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
for UI kubectl port-forward svc/minio-ui 9001:9001


init DVC
pip install dvc
git rm -r --cached 'Churn_Modelling.csv'
git commit -m "stop tracking Churn_Modelling.csv"
dvc add Churn_Modelling.csv
dvc init --subdir
git add Churn_Modelling.csv.dvc .gitignore
dvc remote add -d minio   s3://testbucket
dvc remote modify minio endpointurl http://0.0.0.0:9000
git push
export AWS_SECRET_ACCESS_KEY=testsecret
export AWS_ACCESS_KEY_ID=testkey
dvc push




labeling
run docker container with label-studio
docker run -it -p 8080:8080 -v `pwd`/mydata:/label-studio/data heartexlabs/label-studio:latest

open http://0.0.0.0:8080/
> select sign up and  create account
> create new project
> select data import and import csv file (IMDB Dataset)
> select label template
> select labels (remove template labels and select own)
> go to list text
> click on label
> select relation world in text
> repid last action 50 times
> export file to csv
one record cost 4 minutes  for analyze and select label
we have 1000 records 1000 *4 = 4000 min = 67h
1h = 5$
total labeling cost = 335$ and Should wait 7 days










