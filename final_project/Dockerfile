FROM python:3.10.8 as base
LABEL maintainer="lyabomyr@gmail.com"
RUN pip install --upgrade pip

WORKDIR /ml_project
COPY final_project/requirements.txt /ml_project/requirements.txt
RUN pip install --no-cache-dir --upgrade -r  /ml_project/requirements.txt


ENV WANDB_PROJECT="liunomyr"
ENV PYTHONPATH="$PWD/final_project"

COPY final_project/ml_decision_tree /ml_project/ml_decision_tree
COPY final_project/serving_streamlit.py  /ml_project/streamlit_app.py

CMD streamlit run --server.address 0.0.0.0 --server.port 8080 streamlit_app.py
