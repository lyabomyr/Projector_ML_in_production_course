build_app_multivariate_drift:
	docker build -f Dockerfile -t multivariate-drift-detector:latest --target multivariate-drift-detector .
build_n_push_multivariate_drift_to_docker_hub: build_app_multivariate_drift
	docker tag multivariate-drift-detector:latest lyabomyr/multivariate-drift-detector:latest; docker push lyabomyr/multivariate-drift-detector:latest

build_app_univarite_drift:
	docker build -f Dockerfile -t univarite-drift-detector:latest --target univarite-drift-detector .
build_univarite_drift_detector_n_push_to_docker_hub: build_app_univarite_drift
	docker tag univarite-drift-detector:latest lyabomyr/univarite-drift-detector:latest; docker push lyabomyr/univarite-drift-detector:latest

build_load_data:
	docker build -f Dockerfile -t download-files:latest --target download-files .
build_n_push_load_data: build_load_data
	docker tag download-files:latest lyabomyr/download-files:latest; docker push lyabomyr/download-files:latest


