
For download minio image used command
----  >  docker pull minio/minio
And next run container  with available logs
> docker run   -p 9000:9000   -p 9001:9001   --name minio1   -e "MINIO_ROOT_USER=testkey"   -e "MINIO_ROOT_PASSWORD=testsecret" -v /home/dev/mdata:/data   quay.io/minio/minio server /data --console-address ":9001"



For running in kubernetis
first create cluster:
(U can use kind or minicube)
kind create cluster --name ml-in-production-course-week-2

then running deploy job

> kubectl create -f minio_service/minio_deploy.yml

in this file we have 4 job 1. Create storage (PersistentVolumeClaim),
2. Create Service for api communication
3. Create Service for ui communication
4. Forward storage for ui

then do forwarding ports: <  kubectl port-forward svc/minio-api 9000:9000  >
for UI kubectl port-forward svc/minio-ui 9001:9001


About inference
    time for one pricesing is a 0.4s
    time for multi processing is a 3.02s



init DVC
> pip install dvc
> git rm -r --cached 'Churn_Modelling.csv'
> git commit -m "stop tracking Churn_Modelling.csv"
> dvc add Churn_Modelling.csv
> dvc init --subdir
> git add Churn_Modelling.csv.dvc .gitignore
> dvc remote add -d minio   s3://testbucket
> dvc remote modify minio endpointurl http://0.0.0.0:9000
> git push
> export AWS_SECRET_ACCESS_KEY=testsecret
> export AWS_ACCESS_KEY_ID=testkey
> dvc push




labeling
> run docker container with label-studio
> docker run -it -p 8080:8080 -v `pwd`/mydata:/label-studio/data heartexlabs/label-studio:latest

open http://0.0.0.0:8080/
>> select sign up and  create account
>> create new project
>> select data import and import csv file (IMDB Dataset)
>> select label template
>> select labels (remove template labels and select own)
>> go to list text
>> click on label
>> select relation world in text
>> repid last action 50 times
>> export file to csv
Necessary skills for employee which will do labeling:
- Experience in watch movie
- English upper intermediate
- Good analytics skills
Labeling:
Should the movie description be classified by genre?
genre: erotic, action, war, fantastic, horror, documental, Comedi, Children, western, drama
For one description can be more than one genre
>> If films are very sentimental (love, tragedy)  is drama
>> if the film has intimate scenes that are erotic
>> if a film about superheroes or magic or something unexciting is fantastic
>> if a film about war is war
>> if a film about comedy history is a comedy
>> if a film about advantages for children is children
>> if a film about a detailed historical moment is documental
>> if a film about the wild west and cowboys is western
>> if the film is about crimes, action, drug is action
Corner cases:
if description is empty click on skip
if description haven't consistent information click on skip
Costs:
    one record cost 4 minutes  for analyze and select label
    we have 1000 records 1000 *4 = 4000 min = 67h
    1h = 5$
    total labeling cost = 335$ and Should wait 7 days

Deploy lakefs

  -- create deploy yml file for docker

  -- run command > kubectl create -f lakefs-deploy.yaml

forward port
  --> kubectl port-forward svc/my-lakefs 5000:80








