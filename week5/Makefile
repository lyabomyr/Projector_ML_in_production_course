build app_fastapi:
	 docker build -f week5/Dockerfile -t app-fastapi:latest --target app-fastapi .
run app-fastapi:
	docker run -it -p 8080:8080  app-fastapi:latest
push_fastapi:
	docker tag  app-fastapi:latest lyabomyr/app-fastapi:latest; docker push lyabomyr/app-fastapi:latest
build_app_streamlit:
	docker build -f week5/Dockerfile -t app-streamlit:latest --target streamlit .  
run_app_streamlit: build_app_streamlit
	docker run -it -p 8080:8080  app-streamlit:latest
push_app_streamlit:
	docker tag  app-streamlit:latest lyabomyr/app-streamlit:latest; docker push lyabomyr/push app-streamlit:latest

build_app_seldon:
	docker build -f week5/Dockerfile -t app-seldon:latest --target app-seldon .
run_app_seldon: build_app_seldon
	docker run -it -p 8080:8080  app-seldon:latest
build_n_push_to_docker_hub: run_app_seldon
	docker build -f week5/Dockerfile -t app-seldon:latest --target app-seldon .; docker tag app-seldon:latest lyabomyr/app-seldon:latest; docker push lyabomyr/app-seldon:latest
perfomanse_testing:
	locust -f week5/unit_tests/locust_test_benchmark.py --headless --host http://0.0.0.0:8000 -r 1 -u 10 --run-time 5m
benchmark_port_forwarding_test:
	pytest week5/unit_tests/test_benchmark-forwardpass.py
benchmark_optimize_inference:
	pytest week5/unit_tests/test_benchmark-forwardpass.py