FROM python:3.7
LABEL maintainer="lyabomyr@gmail.com"
RUN pip install --upgrade pip

WORKDIR /ml_decission_tree
COPY week3/ml_decision_tree_sample /ml_decission_tree/ml_decision_tree_sample
COPY week3/requirements.txt /ml_decission_tree/requirements.txt
COPY Churn_Modelling.csv /ml_decission_tree/Churn_Modelling.csv

RUN pip install model-card-toolkit
RUN pip install --no-cache-dir --upgrade -r  /ml_decission_tree/requirements.txt
RUN cd ml_decision_tree_sample/unit_tests/; pytest
CMD ["cd", "ml_decision_tree_sample/unit_tests/;", "pytest"]


