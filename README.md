# Data Engineer Solution by Marko Babic

### RUNNING THE SOLUTION (OS X)

- You should have docker and python installed on your machine
- Start the containers by running: ``` docker-compose -f local.yml up -d ```
- Place the data file (ex. stream.jsonl) in the data folder, name of the file is not important, the first one in the dict will be used

- Run the producer (python script):
- - Create virtual env ``` virtualenv venv ```
- - Activate the env ``` source venv/bin/activate ```
- - Install the packages ``` pip install -r requirements/local.txt ```
- - Run the script ``` python3 src/producer.py ```

- Run the logic consumer (python script)
- - Activate the env ``` source venv/bin/activate ```
- - Run the script ``` python3 src/logic_consumer.py ```

- Run the result consumer (python script)
- - Activate the env ``` source venv/bin/activate ```
- - Run the script ``` python3 src/result_consumer.py ```

Trying to achieve: 
- Run the producer in a container
- Run the consumers in containers

### REPORT

My solution for this challange is based on the sliding window technique. Beacause of the request to ingest historical data, the solution could not be based on the slide frame around the current time, instead I am using the data from the stream and use the most up-to-date time as the reference for the slide. The task says I should assume that all response is within the 5 seconds delay from the current moment, but for the solution to be as much realistic as it could be I didn't take that assumption, and I left the current logic with an hour long window slide so we could have as much accurate data as it can be. Every log that is out of the slide is viewed as a mistake and it's used to calculate the error rate. 


#### Document your approach on how you decide when to output the data

- In this solution the data is outputed when it get's out of the window slide. That suggests that we have a tradef between latency and accuracy. Larger window slide -> more accurate data -> higher latancy. Smaller window slide -> lower latancy -> lower accuracy of data. 

### MEASURED PERFORMANCE METRICS / BENCHMARKING

Currently in the code I measure next topics:

- Frames consumed per second
- Framed produced per second
- Error rate

Benchmarking is/should be done with different sizes of window slides.

### ERROR RATE

- All data that is not in the current window frame of calculations will be considered as a mistake

### SCALABILITY

- Scaling the number of consumers, producers and brokers would benefit the amount of data that we could simultaneously consume, produce and make it more persistan in case of broker failure
- We could also split the storing topic into multiple partitions and split the data, in our case, based on different minute of the window slide offset, or some other decision, where we could benefit with faster data processing but with aggregation in the end

###  EDGE CASES

- Importing old data represents a problem for calculations 
- Larger time frame for wich we are calculating unique users means similar sliding window frame 


### COMMANDS 

#### Reset offset

``` docker-compose -f local.yml exec broker kafka-consumer-groups --bootstrap-server localhost:9092 --group python-consumer --topic user-tracker --reset-offsets --to-earliest --execute ```

#### Create topic

``` docker-compose -f local.yml exec broker kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic user-tracker ```
