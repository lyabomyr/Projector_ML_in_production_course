FROM python:3.7
LABEL maintainer="lyabomyr@gmail.com"
RUN pip install --upgrade pip
RUN pip install model-card-toolkit
COPY week3/requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r  /requirements.txt

COPY week3/ml_decision_tree_sample /ml_decision_tree_sample
COPY Churn_Modelling.csv /Churn_Modelling.csv
COPY week3/short_test_data.csv /short_test_data.csv
COPY week3/unit_tests /unit_tests

ENV PYTHONPATH="$PWD/ml_decision_tree_sample"
# RUN pytest unit_tests/
CMD ["pytest", "unit_tests/"]


