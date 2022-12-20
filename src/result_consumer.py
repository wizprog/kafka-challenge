import json

from utils import create_kafka_consumer
from consts import RESULT_USER_TOPIC

def consume():
    consumer = None
    try:
        consumer = create_kafka_consumer()
    except:
        print("Error occured on consumer creation...")

    consumer.subscribe([RESULT_USER_TOPIC])
    while True:
        for message in consumer:
            message_data = json.loads(message.value)
            unique_users_per_minute = message_data["data"]["unique_users_per_minute"]
            print(f"Unique users per minute: {unique_users_per_minute}")


if __name__ == '__main__':
    consume()