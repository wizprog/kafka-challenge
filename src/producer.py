import json
import time
import logger
from kafka import KafkaProducer


def consume_data(data_file=None):
    if data_file is None:
        data_file = "./data/stream.jsonl"
      
    with open('./data/stream.jsonl', 'r') as json_file:
        json_list = list(json_file)

    return json_list


def create_kafka_producer(kafka_host=None):
    if kafka_host is None:
        kafka_host = "localhost:9092"

    producer = KafkaProducer(
        bootstrap_servers=kafka_host
    )

    return producer


def receipt(err, msg):
    if err is not None:
        print('Error: {}'.format(err))
    else:
        message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
        logger.logger.info(message)
        print(message)

def produce():
    producer = create_kafka_producer()
    data_set = consume_data()
    key_list = ["uid", "ts"]
    
    start_time = time.time()
    produced_messages = 0
    for data in data_set:
        elapsed_time = time.time() - start_time
        if elapsed_time >= 1:
            print(f'Produced {produced_messages} messages per second')
            produced_messages = 0
            start_time = time.time()

        data = json.loads(data)
        usable_dict = {
            key: data[key] for key in key_list
        }
        message = json.dumps(usable_dict)
        producer.send('user-tracker', message.encode('utf-8'))
        producer.flush()
        produced_messages += 1

    print("Producer finished")

if __name__ == '__main__':
    produce()