FROM python:3.12

ENV TZ=Europe/Moscow
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG req=requirements.txt

WORKDIR app

COPY *.py ./
COPY src/* ./src/
COPY requirements.txt ./
COPY templates/* ./templates/

RUN pip install -r $req

ENV PYTHONPATH="/app/"

ENTRYPOINT ["python3","main.py"]

