FROM python:3.10

ENV TZ=Europe/Moscow

ARG req=requirements.txt

WORKDIR app

COPY *.py ./
COPY src/* ./
COPY requirements.txt ./
COPY templates ./

RUN pip install -r $req

ENTRYPOINT ["python3","main.py"]

