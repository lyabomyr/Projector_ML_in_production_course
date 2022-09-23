FROM python:latest
LABEL maintainer="lyabomyr@gmail.com"
RUN pip install --upgrade pip

WORKDIR /ml_project
COPY ../requirements.txt /ml_project/requirements.txt
RUN pip install --no-cache-dir --upgrade -r  /ml_project/requirements.txt
#RUN python3 -m pip install -r /ml_project/requirements.txt
COPY simpleserver.py /ml_project/simpleserver.py

CMD ["uvicorn", "simpleserver:app","--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]
#CMD ["python", "./simpleserver.py"]

