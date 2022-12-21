FROM python:latest

WORKDIR /producer/src
COPY /src ./
COPY /requirements ./requirements
COPY /data ./data

RUN pip install -r requirements/local.txt

CMD [ "python", "-u", "./producer.py"]