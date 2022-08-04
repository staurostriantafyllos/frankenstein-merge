# Frankenstein Merge

## Overview
A simple solution that helps a Data Engineer to:
* Identify the schema of a set of non-structured JSON files
* Identify schema changes while a stream of data are ingested to this process
* Identify errors at the data that are produced by heterogenous data types


## Build image
```
docker image build -t frankenstein-merge:latest .
```

## Case 1: Happy path
In this case, we continuously add data with new fields. At logs we see that a callback is called every time a new field is added.
```
docker run --rm -i frankenstein-merge:latest < datasets/events.jsonl
```

## Case 2: Some errors
In this case, we add some data that face issues that have to do with data type changes on the same fields.
```
docker run --rm -i frankenstein-merge:latest < datasets/erroneous_events.jsonl
```

## Case 3: Your tests
In this case, you can use, as a reference, the file datasets/custom_events.jsonl and add your own events to see how the process reacts to your data changes.
```
docker run --rm -i frankenstein-merge:latest < datasets/custom_events.jsonl
```

## Ideas

The callbacks, that are called, can:
* Log incidents to a managed log service
* Store the data changes to a DB
* Trigger an alerting mechanism
* Trigger another process (Lambda, SQS, etc)
