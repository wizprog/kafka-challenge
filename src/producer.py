import glob
import json
import time
import logger

from utils import create_kafka_producer


def consume_data(data_file=None):
    if data_file is None:
        data_file = glob.glob("data/*")[0]
      
    with open(data_file, 'r') as json_file:
        json_list = list(json_file)

    return json_list

def produce():
    producer = None
    try:
        producer = create_kafka_producer()
    except:
        print("Error occured on producer creation...")
        return

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