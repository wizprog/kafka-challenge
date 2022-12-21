FROM python:latest

WORKDIR /result_consumer/src
COPY /src ./
COPY /requirements ./requirements

RUN pip install -r requirements/local.txt

CMD [ "python", "./result_consumer.py"]