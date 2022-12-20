import json
import time

from collections import defaultdict
from utils import create_kafka_consumer, create_kafka_producer
from consts import HOUR, USER_TOPIC, RESULT_USER_TOPIC

def filter_stale_entries(dictionary, threshold_ts, producer):
    keys = dictionary.keys()
    tobe_filtered = list(filter(lambda x: int(x) > threshold_ts, keys))
    for stale_entry in tobe_filtered:
        item = dictionary.pop(stale_entry, None)
        # Collecting the data that got out of the slide window frame
        unique_users_per_minute = len(item)
        message = {
            "created": time.time(),
            "data": {
                "unique_users_per_minute": unique_users_per_minute
            },
        }
        print(f"For timestamp {stale_entry} there are {unique_users_per_minute} unique keys")
        producer.send(RESULT_USER_TOPIC, message.encode('utf-8'))
        producer.flush()
    return dictionary
        

def consume():
    producer = None
    consumer = None
    try:
        consumer = create_kafka_consumer()
        producer = create_kafka_producer()
    except:
        print("Error occured on consumer creation...")
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

            user_dict = filter_stale_entries(user_dict, min_key, producer) if tobe_filtered else user_dict

            if rounded_ts < min_key:
                miss_count += 1
                continue
            
            old = user_dict.get(str_rounded_ts, set())
            old.add(uid)
            user_dict.update({str_rounded_ts: old})   


if __name__ == '__main__':
    consume()