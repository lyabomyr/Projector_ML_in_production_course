FROM python
LABEL maintainer="lyabomyr@gmail.com"
RUN pip install --upgrade pip

WORKDIR /ml_decission_tree
COPY /ml_decision_tree_sample /ml_decission_tree/ml_decision_tree_sample
COPY requirements.txt /ml_decission_tree/requirements.txt
RUN cat requirements.txt | xargs -n 1 pip install
#RUN cd ml_decision_tree_sample/; source env/bin/activate; cd unit_tests/; pytest


