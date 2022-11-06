build_app_seldon:
	docker build -f Dockerfile -t app-seldon:latest --target app-seldon .
run_app_seldon: build_app_seldon
	docker run -it -p 7777:8080  app-seldon:latest
build_n_push_to_docker_hub: build_app_seldon
	docker tag app-seldon:latest lyabomyr/app-seldon:latest; docker push lyabomyr/app-seldon:latest
wrap_seldon_container_into_kuber: build_n_push_to_docker_hub
	kubectl apply -f k8s/seldon_deploy_model.yaml
build_client_arize:
	docker build -f Dockerfile -t app-client-arize:latest --target app-client-arize .
run_app_arize: build_client_arize
	docker run -it app-client-arize:latest
build_arize_n_push_to_docker_hub: build_client_arize
	docker tag app-client-arize:latest lyabomyr/app-client-arize:latest; docker push lyabomyr/app-client-arize:latest

	