# tweeter-realtime-npl

This repository is a project to implement the streaming data using kafka, using KSQL in pyspark and natural language processing. 

Exposer to API reuqest, kafka as de-coupling service and pyspark new feature KSQL to convert the structed-streaming data to datafram and process it using SQL. 

<b>Publisher</b> -> We are reading data from twitter on real time using the API and publishing it to kafka topic. 

<b>Consumer</b> -> Using pyspark we are reading all the messages published by publisher and beign processed as KSQL(Structued Streaming). 

Implementing the natural lanugage processing on the twitter do the sentiment analysis.
