# Relational Databases (SQL) — Complete Guide

Purpose: Standalone reference for indexes, transactions, query optimization, schema design, and normalization vs denormalization.

## Indexes

- What: Data structures (typically B-tree) that map key values to row locations for fast lookup.
- Common types:
  - B-tree: default, good for ranges and equality.
  - Hash: equality lookup (Postgres hash indexes limited).
  - GIN/GiST: for array / full-text / geometric types.
- Design tips:
  - Index columns used in WHERE, JOIN, ORDER BY.
  - Use composite indexes with the most selective column first (left-most prefix rule).
  - Beware: each index adds write overhead, storage cost, and maintenance during bulk imports.
- Example: CREATE INDEX idx_users_email ON users(email);

## Transactions & isolation levels

- ACID properties.
- Typical isolation levels:
  - READ UNCOMMITTED: dirty reads allowed (rarely used).
  - READ COMMITTED: each statement sees committed data at start of statement (default in many DBs).
  - REPEATABLE READ: statements in transaction see a snapshot (no non-repeatable reads).
  - SERIALIZABLE: highest isolation; may abort conflicts to ensure serial behavior.
- Use explicit transactions for multi-statement invariants. In PostgreSQL use SERIALIZABLE only when needed; it can lead to transaction retries.

## Joins, subqueries, window functions

- Joins:
  - INNER JOIN returns matched rows.
  - LEFT JOIN returns all left rows with NULL for missing right rows.
  - CROSS JOIN multiplies rows.
- Subqueries:
  - Correlated subqueries execute per row (expensive).
  - Uncorrelated can often be optimized or replaced by JOINs.
- Window functions:
  - Compute aggregates across rows related to the current row without collapsing rows.
  - Examples: ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC), SUM(amount) OVER (PARTITION BY day).
- Use CASE expressions and window functions to replace complex self-joins when appropriate.

## Query optimization basics

- Use EXPLAIN / EXPLAIN ANALYZE to inspect execution plans and bottlenecks.
- Common anti-patterns:
  - SELECT \* when you only need some columns (cost of I/O and memory).
  - Correlated subqueries that run per row.
  - Missing indexes for predicates/joins.
- Rewrite strategies:
  - Materialize expensive subqueries into temporary tables or CTEs (beware of optimization fences).
  - Use covering indexes to satisfy queries without touching the table.
  - Batch operations and use bulk inserts/updates.

## Migrations and schema design

- Migration strategy for zero-downtime:
  1. Add nullable column or new table/column.
  2. Backfill data in background job.
  3. Make column non-nullable and add constraints.
  4. Remove old columns if needed in a later deploy.
- Use database-native types appropriately (JSONB in Postgres for semi-structured data).
- Version-control migrations and review generated SQL.

## Normalization vs pragmatic denormalization

- Normalization reduces redundancy and ensures consistency (1NF..3NF).
- Denormalization trades duplication for read performance (precomputed aggregates, flattened tables).
- When to denormalize: read-heavy workloads with tight latency requirements; ensure strong write paths and use background jobs to maintain denormalized copies.

## Practical examples

- Optimize frequent lookup:
  - users(email) — unique index on email: CREATE UNIQUE INDEX users_email_idx ON users(email);
- Use partial indexes for sparse predicates:
  - CREATE INDEX idx_active_users ON users(last_login) WHERE active = true;

## Interview prompts

- Explain differences between READ COMMITTED and SERIALIZABLE and give an example anomaly.
- How do you approach a slow JOIN between two large tables (tens of millions of rows)?

Quick commands:

- PostgreSQL explain: EXPLAIN ANALYZE SELECT ...;
- Show table indexes: \d+ table_name (psql)
