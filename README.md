# Data Engineer Solution by Marko Babic

### RUNNING THE SOLUTION (OS X)

- You should have docker and python installed on your machine
- Start the containers by running: ``` docker-compose -f local.yml up -d ```
- Place the data file (ex. stream.jsonl) in the data folder, name of the file is not important, the first one in the dir will be used

#### Running like scripts 

- Run the producer (python script):
1. Create virtual env ``` virtualenv venv ```
2. Activate the env ``` source venv/bin/activate ```
3. Install the packages ``` pip install -r requirements/local.txt ```
4. Run the script ``` python3 src/producer.py ```

- Run the logic consumer (python script)
1. Activate the env ``` source venv/bin/activate ```
2. Run the script ``` python3 src/logic_consumer.py ```

- Run the result consumer (python script)
1. Activate the env ``` source venv/bin/activate ```
2. Run the script ``` python3 src/result_consumer.py ```


#### Running and reading from docker

1. Build all containers by running ``` docker-compose -f local.yml build ```
2. Start all containers by runnnig ``` docker-compose -f local.yml up -d zookeeper broker ```
3. Create the user-tracker topic by runnning ``` docker-compose -f local.yml exec broker kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic user-tracker ```
4. Create the user-data topic by running ``` docker-compose -f local.yml exec broker kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic user-data ```
5. Producer can't start producing if zookeeper and broker are not runnnig, so wait a couple of seconds before starting the producer by running ``` docker-compose -f local.yml up -d producer```
6. Start the logic_consumer and result_consumer by running ``` docker-compose -f local.yml up -d logic_consumer result_consumer```
7. Read the output by running ``` docker logs -f producer , docker logs -f logic_consumer or docker logs -f result_consumer```

- For some reason the docker solution is not efficient enough and it produce the data slowly. My suggestion would be to run the producer with a script and then use the containers for consumers. Unfortunately I didn't have time to fix this.

### REPORT

My solution for this challange is based on the sliding window technique. Beacause of the request to ingest historical data, the solution could not be based on the slide frame around the current time, instead I am using the data from the stream and use the most up-to-date time as the reference for the slide. The task says I should assume that all responses have a maximum delay of 5 seconds, but for the solution to be as realistic as it could be I didn't make that assumption, and I left the current logic with an hour long window slide so our data would be as accurate as possible. Every log that is out of the slide is viewed as a mistake and it's used to calculate the error rate. 


#### Document your approach on how you decide when to output the data

- In this solution the data is outputted when it gets out of the window slide. That suggests that we have a tradeoff between latency and accuracy. Larger window slide -> higher accuracy -> higher latancy. Smaller window slide -> lower latancy -> lower accuracy. 

### MEASURED PERFORMANCE METRICS / BENCHMARKING

Currently in the code I measure the following topics:

- Frames consumed per second
- Framed produced per second
- Error rate

Benchmarking is/should be done with different sizes of window slides.

### ERROR RATE

- All data that is not in the current window frame of calculations will be considered as a mistake

### SCALABILITY

- Scaling the number of consumers, producers and brokers would benefit the amount of data that we could simultaneously consume, produce and would make it more resistant to broker failures
- We could also split the storing topic into multiple partitions and split the data, in our case, based on different minute of the window slide offset, or some other decision, where we could benefit with faster data processing but with aggregation at the end

###  EDGE CASES

- Importing old data represents a problem for calculations 
- Larger time frame for which we are calculating unique users means similar sliding window frame 


### COMMANDS 

#### Reset offset

``` docker-compose -f local.yml exec broker kafka-consumer-groups --bootstrap-server localhost:9092 --group python-consumer --topic user-tracker --reset-offsets --to-earliest --execute ```

#### Create topic

``` docker-compose -f local.yml exec broker kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic user-tracker ```

#### List topics

``` docker-compose -f local.yml exec broker kafka-topics --list --bootstrap-server localhost:9092 ```
