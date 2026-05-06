# Day 3 — Apache Kafka & streaming basics

## What I learned today
Kafka is a distributed event streaming platform that acts as a
high-throughput, fault-tolerant middle layer between systems.
Coming from a batch ETL background (DataStage, Informatica, cron
jobs at TCS and Optum), the fundamental shift is from scheduled
data movement to continuous event flow. Data no longer waits for
a 2am job — it moves the moment it is created. Built and ran a
real producer-consumer pipeline on Redpanda Cloud (Kafka-compatible)
with messages flowing in real time between two terminals.

## Key concepts

- **Producer** — writes events to a Kafka topic. Any application
  that generates data — a banking transaction system, a web app,
  a healthcare monitor.

- **Consumer** — reads events from a Kafka topic. Tracks its
  position using an offset. Can pause, resume, and replay.

- **Topic** — named category for a stream of events. Like a
  database table name — you write to it and read from it.
  Example: orders, transactions, patient-events.

- **Partition** — how a topic is split across brokers for
  parallelism. More partitions = more throughput = more
  consumers reading simultaneously.

- **Offset** — the position of a message within a partition.
  Tracked by the consumer, not deleted by Kafka. This enables
  replayability — consumers can re-read from any point.

- **Consumer group** — multiple consumers sharing the work of
  reading a topic. Each partition is read by only one consumer
  in the group at a time.

- **Replayability** — consumers can re-read from offset 0 by
  using a new group.id. Messages persist on the broker
  independently of whether they have been consumed.

## What I built today
- Created a free Redpanda Cloud cluster (Kafka-compatible,
  no credit card) on AWS eu-west-2
- Created an orders topic with 1 partition
- Built producer.py — sends 5 order events with timestamps,
  order ID as key, full order details as JSON value
- Built consumer.py — reads events in real time, prints
  order details with offset number
- Successfully ran both in two terminals simultaneously —
  messages appeared in consumer in real time as producer sent them
- Demonstrated replayability by changing group.id to
  order-processor-2 and replaying all 5 messages from offset 0

## Errors I hit and how I fixed them

| Error | Cause | Fix |
|---|---|---|
| ModuleNotFoundError: confluent_kafka | Library not installed | pip install confluent-kafka |
| Unsupported protocol HTTPS | Pasted Redpanda console URL instead of bootstrap server | Used correct bootstrap server: d7tmih2e1n5c11g1k480.any.eu-west-2.mpx.prd.cloud.redpanda.com:9092 |
| Authentication failed | Confluent used PLAIN, Redpanda uses SCRAM | Changed sasl.mechanisms to SCRAM-SHA-256 |

## Pipeline output

Producer terminal:
\```
Producing order events...
Message delivered to orders partition [0] offset 0
Message delivered to orders partition [0] offset 1
Message delivered to orders partition [0] offset 2
Message delivered to orders partition [0] offset 3
Message delivered to orders partition [0] offset 4
All orders produced successfully!
\```

Consumer terminal:
\```
Listening for order events... (Ctrl+C to stop)
Received order: ID=1 | Customer=101 | Product=Laptop | Amount=€999.99 | Offset=0
Received order: ID=2 | Customer=102 | Product=Phone | Amount=€599.99 | Offset=1
Received order: ID=3 | Customer=103 | Product=Tablet | Amount=€399.99 | Offset=2
Received order: ID=4 | Customer=101 | Product=Mouse | Amount=€29.99 | Offset=3
Received order: ID=5 | Customer=104 | Product=Keyboard | Amount=€79.99 | Offset=4
\```

## Redpanda vs Confluent

| Factor | Confluent | Redpanda |
|--------|-----------|----------|
| Language | Java | C++ |
| Architecture | ZooKeeper + brokers | Single binary |
| Free tier | Credit card required | No card needed |
| Kafka compatible | Native Kafka | 100% API compatible |
| Ecosystem | Massive, market leader | Growing, newer |
| Best for | Enterprise production | Learning, simplicity |

## Streaming vs batch decision framework

| Factor | Use Streaming | Use Batch |
|--------|--------------|-----------|
| Latency needed | Sub-second to minutes | Hours acceptable |
| Data arrival | Continuous events | Files or snapshots |
| Use case | Fraud detection, alerts | Monthly reports, billing |
| Cost priority | Speed over cost | Cost over speed |
| Transformation | Simple, per-event | Complex, full dataset |

## How this connects to my work experience
At TCS and Optum all data movement was batch — overnight files,
scheduled jobs, 2am ETL runs. Kafka represents the real-time
layer that was always missing from those architectures.

In a banking context (HDFC Bank), Kafka would handle transaction
events in real time — fraud detection cannot wait for a 2am batch
job. A suspicious transaction needs to be flagged in milliseconds.

In healthcare (Optum), patient monitoring events need immediate
processing. A critical patient alert processed in the next morning's
batch report is not acceptable — Kafka enables immediate action.

The hybrid architecture I now understand:
Kafka (real-time ingestion) → Snowflake (storage) → dbt (batch
transformation) — three tools doing different jobs well together.

##talking points
- "Kafka decouples producers and consumers — the source system
  does not need to know who is consuming its events or how many
  consumers there are. I can add a new consumer without touching
  the producer at all."
- "Offsets give consumers full control over replayability —
  critical for recovery and reprocessing. If a downstream system
  fails, it simply re-reads from the last committed offset."
- "In our architecture Kafka handles ingestion and real-time
  actions, dbt handles batch transformation on the warehouse —
  two tools doing different jobs well."
- "I chose Redpanda over Confluent for learning — fully
  Kafka-compatible, no credit card required, simpler operations.
  In production I would evaluate Confluent for its ecosystem
  maturity and enterprise support."

## Resources
- Confluent developer docs: developer.confluent.io
- Redpanda docs: docs.redpanda.com
- Kafka the definitive guide (free):
  confluent.io/resources/kafka-the-definitive-guide
- My code: /code/kafka/producer.py and /code/kafka/consumer.py
