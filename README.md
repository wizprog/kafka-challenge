# Data Engineer Solution by Marko Babic

### Requirements:
- write a report: what did you do? what was the reasons you did it like that?
- measure at least one performance metric (e.g. frames per second)
- document your approach on how you decide **when** to output the data 
- document the estimated error in counting
- it should be possible to ingest historical data. e.g. from the last 2 years.


### RUNNING THE SOLUTION (OS X)

- You should have docker and python installed on your machine
- Start the containers by running: ``` docker-compose -f local.yml up -d ```
- Place the data file (ex. stream.jsonl) in the data folder, name of the file is not important, the first one in the dict will be used
- Run the producer (python script current version)
- Run the consumer (python script current version)

Trying to achieve: 
- Trying to run them as containers.

### REPORT

#### You want to display the results as soon as possible

- Tradeoff, accurracy vs latency of calculation

#### Document your approach on how you decide when to output the data

- After the sliding window

### MEASURED PERFORMANCE METRICS / BENCHMARKING

Currently in the code I measure next topics:

- Frames consumed per second
- Framed produced per second
- Error rate 

### ERROR RATE

- All data that is not in the current window frame of calculations will be considered as a mistake

### SCALABILITY

- Scaling the number of consumers and producers
- Spliting data into mulitple partitions and combining into single frames on the end

###  EDGE CASES

- Importing old data represents a problem for calculations 
- Larger time frame for wich we are calculating unique users means similar sliding window frame 


### COMMANDS 

#### Reset offset

``` docker-compose -f local.yml exec broker kafka-consumer-groups --bootstrap-server localhost:9092 --group python-consumer --topic user-tracker --reset-offsets --to-earliest --execute ```

#### Create topic

``` docker-compose -f local.yml exec broker kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic user-tracker ```
