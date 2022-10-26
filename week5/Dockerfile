FROM python:3.10.8 as base
LABEL maintainer="lyabomyr@gmail.com"
RUN pip install --upgrade pip

WORKDIR /ml_project
COPY week5/requirements.txt /ml_project/requirements.txt
RUN pip install --no-cache-dir --upgrade -r  /ml_project/requirements.txt


ENV WANDB_PROJECT="liunomyr"
ENV WANDB_API_KEY="0a14fd83112d8258ad9cb780edb9e9932241f5fc"

ENV PYTHONPATH="$PWD/ml_project"
COPY week5/serving /ml_project/serving
COPY week5/unit_tests /ml_project/unit_tests
COPY Churn_Modelling.csv /ml_project/Churn_Modelling.csv
COPY week5/test_churn_modelling.csv /ml_project/test_churn_modelling.csv

RUN echo python --version
RUN echo $PYTHONPATH
RUN pytest unit_tests/test_fastapi.py
CMD [ "bash" ]

FROM base AS app-fastapi
CMD uvicorn --host 0.0.0.0 --port 8080 --workers 4 serving.fast_api:app

FROM base as streamlit
CMD streamlit run --server.address 0.0.0.0 --server.port 8080 serving/streamlit_app.py

FROM base AS app-seldon
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Port for GRPC
EXPOSE 5000
# Port for REST
EXPOSE 9000

# Define environment variables
ENV MODEL_NAME SeldonAPI
ENV SERVICE_TYPE MODEL

COPY week5/serving/seldon_api.py /ml_project/SeldonAPI.py

RUN chown -R 8888 /ml_project
RUN mkdir /.cache
RUN chmod 777 /.cache
RUN mkdir /.config
RUN chmod 777 /.config
ENV PERSISTENCE 0


CMD exec seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE --persistence $PERSISTENCE
