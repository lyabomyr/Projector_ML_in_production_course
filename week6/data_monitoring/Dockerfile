FROM python:3.10.8 as base 
LABEL maintainer="lyabomyr@gmail.com"
WORKDIR /detector
COPY requirements.txt /detector/requirements.txt
RUN pip install -r requirements.txt


FROM base AS multivariate-drift-detector
COPY multivariate_drift_detection.py /detector/multivariate_drift_detection.py

FROM base AS univarite-drift-detector
COPY univariate_drift_detection.py /detector/univariate_drift_detection.py

FROM base AS download-files 
COPY train.csv /detector/train.csv
COPY test.csv /detector/test.csv