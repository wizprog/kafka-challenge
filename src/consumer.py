import json
import time
import logger

from kafka import KafkaConsumer
from collections import defaultdict


HOUR = 60
USER_TOPIC = "user-tracker"

def create_kafka_consumer(kafka_host=None):
    if kafka_host is None:
        kafka_host = "localhost:9092"

    consumer = KafkaConsumer(
        bootstrap_servers=kafka_host,
        group_id="python-consumer",
        auto_offset_reset="earliest",
    )
    logger.logger.info('Kafka Consumer has been initiated...')
    return consumer


def filter_stale_entries(dictionary, threshold_ts):
    keys = dictionary.keys()
    tobe_filtered = list(filter(lambda x: int(x) > threshold_ts, keys))
    for stale_entry in tobe_filtered:
        item = dictionary.pop(stale_entry, None)
        print(f"For timestamp {stale_entry} there are {len(item)} unique keys")
    return dictionary
        

def consume():
    consumer = create_kafka_consumer()
    # available_topics = consumer.topics()
    # print('Available topics to consume: ', available_topics)
    # user_topic = available_topics.pop()
    # if user_topic is None:
    #     logger.logger.info("No topic found, ending program...")
    #     return
    consumer.subscribe([USER_TOPIC])
    user_dict = defaultdict()
    max_key = 0
    start_time = time.time()
    counting_frames = 0
    miss_count = 0
    hit_count = 0

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= 1:
            print(f'Consumed {counting_frames} messages per second')

            if hit_count + miss_count > 0 and miss_count > 0:
                print(f"Miss percentage {round((miss_count * 100) / (hit_count + miss_count), 2)} %")
            counting_frames = 0
            start_time = time.time()

        for message in consumer:
            counting_frames += 1

            elapsed_time = time.time() - start_time
            if elapsed_time >= 1:
                print(f'Consumed {counting_frames} messages per second')
                if hit_count + miss_count > 0 and miss_count > 0:
                    print(f"Miss percentage {(miss_count * 100) / (hit_count + miss_count)} %")
                counting_frames = 0
                start_time = time.time()

            data = json.loads(message.value)
            ts = data["ts"]
            uid = data["uid"]
            rounded_ts = ts // HOUR
            str_rounded_ts = str(rounded_ts)

            tobe_filtered = False
            if rounded_ts > max_key:
                max_key = rounded_ts
                print(f"max_key changed: {max_key}")
                tobe_filtered = True

            min_key = int(max_key) - HOUR

            user_dict = filter_stale_entries(user_dict, min_key) if tobe_filtered else user_dict

            if rounded_ts < min_key:
                miss_count += 1
                continue
            
            old = user_dict.get(str_rounded_ts, set())
            old.add(uid)
            user_dict.update({str_rounded_ts: old})   


if __name__ == '__main__':
    consume()