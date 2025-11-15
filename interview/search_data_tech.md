# Search & Data Technology — Practical Guide

Purpose: When to use search engines vs databases, basics of Cassandra, and design of high-volume pipelines.

## When Elasticsearch is appropriate

- Use for full-text search, near real-time indexing, relevance scoring, complex search facets, and analytics over textual data.
- Not a replacement for a transactional DB: eventual consistency and limited transactional guarantees.
- Architecture: index -> shards -> replicas; map your shards/replicas to cluster capacity.

## Full-text search vs relational queries

- Full-text: inverted indices, tokenization, stemming, scoring, fuzzy matching, relevance.
- Relational: exact queries, joins, transactions, strong consistency.
- Best pattern: treat DB as source-of-truth, index into ES for searching; have near-real-time sync (change-data-capture or update hooks).

## Cassandra basics

- Wide-column store designed for high write throughput and availability.
- Partition key determines which node holds the data; choose partition keys carefully to avoid hotspots.
- Clustering keys define order within partition (for range queries).
- Data modeling: query-first approach; denormalize and duplicate data for fast reads.

## High-volume log/event pipeline basics

- Typical stages: producers -> broker (Kafka) -> stream processors (Flink/ksql/consumer apps) -> sinks (Elasticsearch, data lake S3, analytics DB).
- Design concerns:
  - Backpressure and retention policies.
  - Schema evolution: use Avro/Protobuf with schema registry.
  - Monitoring consumer lag and throughput.

## Interview prompts

- How do you keep Elasticsearch indexes in sync with the primary database?
- Sketch a data model in Cassandra for user activity feed supporting range queries per user.

Operational tips:

- For ES: monitor shard allocation, heap usage, refresh intervals, and index mapping for fields to avoid mapping explosion.
- For Kafka: monitor consumer lag, partition skew, and broker disk usage.
