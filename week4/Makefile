build:
	docker build -f week4/Dockerfile -t kfp_train:latest .
push:
	docker tag kfp_train:latest lyabomyr/kfp_train:latest;  docker push lyabomyr/kfp_train:latest
pull:
	docker pull lyabomyr/kfp_train:latest
build&push&runpipeline:
	docker build -f week4/Dockerfile -t kfp_train:latest .; docker tag kfp_train:latest lyabomyr/kfp_train:latest;  docker push lyabomyr/kfp_train:latest; cd week4;python3 kfp_train_pipeline.py http://0.0.0.0:8888; cd ..
