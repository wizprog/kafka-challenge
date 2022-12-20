import logger

from kafka import KafkaProducer, KafkaConsumer


def create_kafka_producer(kafka_host=None):
    if kafka_host is None:
        kafka_host = "localhost:9092"

    producer = KafkaProducer(
        bootstrap_servers=kafka_host
    )

    return producer


def create_kafka_consumer(kafka_host=None, group_id="python-consumer"):
    if kafka_host is None:
        kafka_host = "localhost:9092"

    consumer = KafkaConsumer(
        bootstrap_servers=kafka_host,
        group_id=group_id,
        auto_offset_reset="earliest",
    )
    logger.logger.info('Kafka Consumer has been initiated...')
    return consumer