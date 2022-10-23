build app_fastapi:
	 docker build -f week5/Dockerfile -t app-fastapi:latest --target app-fastapi .
run app-fastapi:
	docker run -it -p 8080:8080  app-fastapi:latest
build_app_streamlit:
	docker build -f week5/Dockerfile -t app-streamlit:latest --target streamlit .  
run_app_streamlit: build_app_streamlit
	docker run -it -p 8080:8080  app-streamlit:latest

build_app_seldon:
	docker build -f week5/Dockerfile -t app-seldon:latest --target app-seldon .  

run_app_seldon: build_app_seldon
	docker run -it -p 8080:8080  app-seldon:latest

build_n_push_to_docker_hub: run_app_seldon
	docker build -f week5/Dockerfile -t app-seldon:latest --target app-seldon .; docker tag app-seldon:latest lyabomyr/app-seldon:latest; docker push lyabomyr/app-seldon:latest



