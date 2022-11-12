FROM python:3.9.15
WORKDIR /fs

COPY week7/requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN ln -s /usr/bin/python3 /usr/bin/python

COPY week7/feature_repo/ fs/feature_repo
RUN cd fs/feature_repo; feast apply
RUN cd fs/feature_repo; python training.py

CMD ["bash"]

