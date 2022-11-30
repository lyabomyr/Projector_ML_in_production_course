FROM python:3.10.8 as base 
LABEL maintainer="lyabomyr@gmail.com"
RUN pip install --upgrade pip

WORKDIR /ml_project
COPY week6/requirements.txt /ml_project/requirements.txt
RUN pip install --no-cache-dir --upgrade -r  /ml_project/requirements.txt


# Define environment variables
ENV MODEL_NAME SeldonAPI
ENV SERVICE_TYPE MODEL
ENV PERSISTENCE 0
ENV WANDB_PROJECT="liunomyr"
ENV WANDB_API_KEY "0a14fd83112d8258ad9cb780edb9e9932241f5fc"
ENV SPACE_KEY "687de45"
ENV API_KEY "1e43dcb4c11743708ef" 
ENV PYTHONPATH "$PWD/ml_project"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY week6/model_monitoring/seldon_api.py /ml_project/SeldonAPI.py
COPY week6/model_monitoring /ml_project/model_monitoring
COPY week6/ml_decision_tree_sample  /ml_project/ml_decision_tree_sample
COPY week6/config.py /ml_project/config.py
COPY Churn_Modelling.csv /ml_project/Churn_Modelling.csv



FROM base AS app-seldon
# Port for GRPC
EXPOSE 5000
# Port for REST
EXPOSE 9000
RUN chown -R 8888 /ml_project
RUN mkdir /.cache
RUN chmod 777 /.cache
RUN mkdir /.config
RUN chmod 777 /.config

CMD exec seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE --persistence $PERSISTENCE


FROM base AS app-client-arize
CMD python3 model_monitoring/arize_examle.py