FROM python:latest

WORKDIR /producer/src
COPY /src ./
COPY /requirements ./requirements

RUN pip install -r requirements/local.txt

CMD [ "python", "-u", "./producer.py"]