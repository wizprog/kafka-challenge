FROM python:latest

WORKDIR /logic_consumer/src
COPY /src ./
COPY /requirements ./requirements

RUN pip install -r requirements/local.txt

CMD [ "python", "-u", "./logic_consumer.py"]