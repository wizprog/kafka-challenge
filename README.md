# Data Engineer Solution by Marko Babic


## RUNNING THE SOLUTION

- Currently running producer and consumer as separate python processes.
- Trying to run them inside of containers.

## BENCHMARKING

- Benchmaring the code, calculating FPS, input rate.

## OPTIMIZING


## SCALABILITY

- Scaling the number of consumers and producers.
- Spliting data into mulitple partitions and combining into single frames on the end.


## you want to display the results as soon as possible

- Tradeoff, accurracy vs latency of calculation

## document your approach on how you decide when to output the data

- After the sliding window

## document the estimated error in counting

- All data that is not in the current window frame of calculations will be considered as a mistake


##  edge cases

- Importing old data represents a problem for calculations 
- Larger time frame for wich we are calculating unique users means similar sliding window frame for  

## COMMANDS 

# Reset offset

- docker-compose -f local.yml exec broker kafka-consumer-groups --bootstrap-server localhost:9092 --group python-consumer --topic user-tracker --reset-offsets --to-earliest --execute

# Create topic

- docker-compose -f local.yml exec broker kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic user-tracker
