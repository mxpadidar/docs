# Database Concepts

## **Relational vs. NoSQL Databases**

**Relational** databases (e.g., PostgreSQL, MySQL, SQL Server) store data in fixed-schema tables with defined columns and data types.

- **Structure:** **Schema-on-Write**. Requires data structure to be strictly defined before data can be inserted.

- **Relationships:** Data is connected using **keys** (Foreign and Primary Keys), allowing complex joins across multiple tables.

- **Integrity:** Strong support for **ACID properties**, ensuring data consistency and reliability.

- **Scaling:** Primarily scales **vertically** (upgrading server hardware), though read-scaling via replication is common.

**NoSQL databases** (e.g., MongoDB, Cassandra, Redis) are designed for flexibility, scalability, and performance. Unlike relational databases, they don’t enforce a fixed schema — data structures can evolve freely over time.

They’re built to scale **horizontally**, distributing data across multiple servers for high throughput and fault tolerance. NoSQL systems typically prioritize **availability and partition tolerance** over strict consistency, following the **BASE** principle (_Basically Available, Soft-state, Eventually consistent_).

Data can be stored and retrieved without predefined schemas, making NoSQL a strong fit for dynamic, large-scale, or unstructured data environments such as real-time analytics, caching, and big data applications.

- **Document Databases** — Store data as flexible, JSON or BSON-like documents. They’re ideal when records vary in structure or need to evolve over time. Common use cases include content management systems, product catalogs, and user profile storage.

- **Key-Value Stores** — Work like hash tables where each unique key maps directly to a value. They’re extremely fast and simple, making them perfect for caching, session storage, and quick lookups. Redis and DynamoDB are popular examples.

- **Graph Databases** — Model data as **nodes** (entities) and **edges** (relationships), allowing complex relationship queries. They’re used in social networks, recommendation systems, and fraud detection.

- **Column-Family Databases** — Organize data by **columns instead of rows**, optimizing for wide datasets and large-scale reads/writes. Common in analytics and high-availability distributed systems, such as Cassandra or HBase.

---

## **Data Modeling: Normalization and Relationships**

Data modeling structures the data within a relational database to reduce redundancy and improve integrity and efficiency.

### Normalization

**Normalization** is the process of structuring a database to eliminate redundant data and ensure dependencies make sense (data is stored where it belongs).

- **Purpose:** Minimizes data anomalies (inconsistencies), saving storage space and improving integrity.
- **Normal Forms (NF):** Databases are typically modeled to the **Third Normal Form (3NF)**, ensuring that non-key columns depend only on the primary key, not on other non-key columns.
- **Denormalization:** Intentionally adding controlled redundancy (duplication) to a normalized structure to optimize **read performance** by avoiding complex joins.

### Relationships

Relationships define how data in different tables is linked using foreign keys.

- **One-to-One:** Each record in Table A relates to exactly one record in Table B (e.g., a User has one Profile).
- **One-to-Many:** Each record in Table A relates to many records in Table B, but each record in B relates to only one in A (e.g., a Customer has many Orders).
- **Many-to-Many:** Records in Table A relate to many records in B, and vice-versa. This requires an **intermediate join table** to link the two primary tables (e.g., a Student enrolls in many Courses, and a Course has many Students).

---

## **Database Indexing**

An **index** is a data structure that speeds up data retrieval operations on a database table.
Instead of scanning every row (a **full table scan**), the database uses the index to **quickly locate** rows that match a query condition — similar to how a book index lets you jump directly to the right page.

Indexes are one of the most critical performance tools in database optimization. Proper indexing can turn queries that take seconds into millisecond responses — but poor or excessive indexing can slow down writes and consume unnecessary storage.

### How Indexes Work

Most modern relational databases (PostgreSQL, MySQL, etc.) implement indexes using **B-tree** or **Hash** structures:

- **B-tree Index (most common):**
  Keeps data sorted by key values, enabling fast lookups, ordered traversals, and range queries (`BETWEEN`, `<`, `>`).
  Ideal for queries like:

  ```sql
  SELECT * FROM users WHERE age BETWEEN 20 AND 30;
  ```

- **Hash Index:**
  Uses hash maps for constant-time equality lookups (`=`).
  Perfect for queries like:

  ```sql
  SELECT * FROM users WHERE id = 101;
  ```

When a query runs, the database checks its **query planner** to decide whether to use an index or a full table scan, based on cost estimation.

### When to Use an Index

Indexes are most useful when they significantly reduce the number of rows scanned.
Add an index when:

- The column is frequently used in `WHERE`, `JOIN`, or `ORDER BY` clauses.
- The column is a **foreign key** or part of a **frequently filtered relationship**.
- The table is large, and reads are much more frequent than writes.
- The column has **high selectivity** (many unique or varied values, e.g., `email`, `user_id`).

**Example:**

```sql
CREATE INDEX idx_users_email ON users(email);
```

Now queries filtering by `email` will locate rows instantly without scanning the entire table.

### When Not to Use an Index

Indexes are not free — they speed up reads but slow down writes.
Avoid indexing when:

- The column has **low selectivity** (e.g., boolean or gender fields).
- The table is **small**, where a full scan is faster than maintaining an index.
- The table handles **high write volume** — every insert, update, and delete also modifies the index.
- The index will rarely be used by queries.

Excessive indexing can degrade write performance and increase storage requirements.

### Types of Indexes

- **Primary Index:** Automatically created on the primary key column.
- **Unique Index:** Ensures all indexed values are distinct (e.g., for emails or usernames).
- **Composite Index:** Covers multiple columns in a specific order.

  ```sql
  CREATE INDEX idx_orders_user_status ON orders(user_id, status);
  ```

  Useful for queries filtering by both columns in the same order.

- **Partial Index:** Applies only to rows matching a condition, saving space.

  ```sql
  CREATE INDEX idx_active_users ON users(email) WHERE active = true;
  ```

- **Covering Index:** Includes all columns needed by a query, so the database can serve results directly from the index without reading the main table.
- **Full-Text Index:** Specialized for text search (used for `MATCH ... AGAINST` or `to_tsvector()` in PostgreSQL).
- **GIN / GiST Indexes (PostgreSQL):** Optimized for arrays, JSON, or geometric data types.

### Performance Trade-offs

Indexes offer major performance benefits but come with certain costs that need to be balanced carefully.

They make **read-heavy operations** much faster — especially `SELECT`, `JOIN`, and `ORDER BY` queries — since the database can locate rows without scanning the entire table. They also enable **efficient sorting and range lookups**, making them invaluable for large datasets.

However, the trade-offs are clear: every time you perform an `INSERT`, `UPDATE`, or `DELETE`, the index must also be updated, which slightly slows down write operations. Additionally, indexes consume **extra disk space** and require **ongoing maintenance** to remain optimized — much like keeping a library’s catalog up to date as new books arrive or old ones are removed.

In short: indexes **speed up reads** but **slow down writes** and **increase storage costs**, so they should be added thoughtfully where they provide real query benefits.

### Best Practices

- Always analyze queries with `EXPLAIN` or `EXPLAIN ANALYZE` to verify index usage.
- Index columns used in filtering or joining — not every column.
- Create **composite indexes** in the order your queries use the columns.
- Drop unused or redundant indexes — they waste resources.
- Rebuild or **VACUUM** indexes periodically in databases like PostgreSQL.
- Combine indexing with **query optimization** — sometimes restructuring a query is more effective than adding an index.
- For distributed or sharded databases, ensure indexes align with your **partitioning keys**.

### **Quick Example: Before vs. After Index**

Without index:

```sql
SELECT * FROM orders WHERE user_id = 501;
-- Full table scan: reads 1M rows
```

With index:

```sql
CREATE INDEX idx_orders_user_id ON orders(user_id);
SELECT * FROM orders WHERE user_id = 501;
-- Index scan: reads only matching rows
```

Execution time may drop from seconds to milliseconds, depending on table size.

### **Clustered vs. Non-Clustered Indexes**

Indexes can be **clustered** or **non-clustered**, depending on how they store and organize data on disk.

#### **Clustered Index**

- The **table’s actual data** is stored **in the order of the index**.
- The index and the table data are **physically the same** — there’s no separate structure.
- Each table can only have **one clustered index**, since the data can only be sorted one way.
- Usually created automatically on the **PRIMARY KEY**.

**Example:**

```sql
CREATE CLUSTERED INDEX idx_users_id ON users(id);
```

> The table’s rows are now stored on disk in order of `id`.
> This makes range queries like `WHERE id BETWEEN 100 AND 200` extremely fast.

**Trade-off:**
Inserting new rows can be slower since data must be physically reordered to maintain index order.

#### **Non-Clustered Index**

- A **separate structure** from the table that stores key values and **pointers** to the actual data rows.
- The table data itself remains unsorted.
- You can create **multiple non-clustered indexes** on a table — one for each frequent query pattern.

**Example:**

```sql
CREATE NONCLUSTERED INDEX idx_users_email ON users(email);
```

> The database keeps a small sorted structure of `email` values that points to rows in the main table.
> This speeds up lookups like `WHERE email = 'user@example.com'`.

**Trade-off:**
Each additional index adds overhead on write operations (since every insert/update must update multiple indexes).

- **Clustered index** → defines the _physical_ sort order of the table.
- **Non-clustered index** → separate lookup table pointing to data rows.
- **Rule of thumb:**
  - Use a **clustered index** for your main access path (often the primary key).
  - Add **non-clustered indexes** for frequent lookups, joins, or filters.

## **Database Constraints**

**Constraints** are rules enforced by the database to keep data **valid, consistent, and reliable**.
They prevent invalid operations — like duplicate users, orphaned records, or negative prices — even if the application has bugs.

They’re critical for **data integrity** and ensure that your database always enforces the logic your code depends on.

### **Common Constraint Types**

**1. PRIMARY KEY**

Uniquely identifies each record. Automatically creates an index.

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT NOT NULL
);
```

> Each row must have a unique `id`. Two users can’t share the same primary key.

**2. UNIQUE**

Prevents duplicate values in a column or a set of columns.

```sql
ALTER TABLE users ADD CONSTRAINT unique_email UNIQUE(email);
```

> Guarantees that no two users can register with the same email.

**3. FOREIGN KEY**

Links data between tables and enforces referential integrity.

```sql
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id) ON DELETE CASCADE
);
```

> Every `orders.user_id` must exist in `users.id`.
> Deleting a user automatically deletes their orders (`CASCADE`).

**4. CHECK**

Ensures a column’s values meet certain conditions.

```sql
ALTER TABLE users ADD CONSTRAINT check_age CHECK (age >= 13);
```

> Prevents inserting a user with age less than 13.

**5. NOT NULL**

Forces a column to always have a value.

```sql
ALTER TABLE users ALTER COLUMN email SET NOT NULL;
```

> Guarantees that every user has an email — no missing fields.

**6. DEFAULT**

Sets an automatic value when none is provided.

```sql
ALTER TABLE users ALTER COLUMN created_at SET DEFAULT NOW();
```

> If `created_at` isn’t provided, it gets the current timestamp automatically.

### Constraints vs. Indexes

- **Constraints** = Ensure correctness.
- **Indexes** = Ensure speed.
- Some constraints (like `PRIMARY KEY` and `UNIQUE`) automatically create indexes, but others (like `CHECK` or `FOREIGN KEY`) do not.

### Best Practices

- Always define **constraints at the database level** — don’t rely only on backend validation.
- Use **foreign keys** to prevent broken relationships between tables.
- Add **check constraints** to enforce domain rules (e.g., `price > 0`).
- Combine constraints with **indexes** on frequently queried columns for performance.

---

## Race Conditions

A **race condition** occurs when multiple processes or threads attempt to access and modify the same resource concurrently, and the final outcome depends on the unpredictable timing of their execution. In simple terms, it’s when two operations “race” to complete first, leading to inconsistent or incorrect results.

### Why Race Conditions Happen

Race conditions appear in systems that support **concurrency** — where multiple tasks run at the same time without proper coordination. This can happen in application code (e.g., multithreading, async operations) or at the database level (e.g., concurrent updates to the same record).

Example scenario: two users try to withdraw money from the same bank account simultaneously. Both read the balance before either writes back the new value, resulting in an incorrect final balance.

### Common Examples

- **Application level:** Two background workers process the same job file at once, overwriting results.
- **Database level:** Two transactions update the same row simultaneously without isolation, causing lost updates.
- **File system level:** Multiple processes write to the same file concurrently, corrupting the file.

### How to Prevent Race Conditions

- Use **locks** (e.g., mutexes, database locks) to serialize access to shared resources.
- Apply proper **transaction isolation levels** in databases to prevent concurrent conflicts.
- Use **atomic operations** where possible — actions that complete fully or not at all.
- Implement **idempotent operations** in APIs so repeated calls produce the same effect.
- In distributed systems, coordinate through **message queues** or **centralized state management** instead of direct shared access.

### In Short

Race conditions are timing-related bugs that appear only under concurrency. They can silently corrupt data or cause unpredictable system behavior. The best defense is **controlled access** through locking, atomicity, and isolation.

---

## **Database Transactions and ACID Properties**

A **transaction** is a single logical unit of work in a database — typically a sequence of one or more operations (e.g., multiple `INSERT`, `UPDATE`, or `DELETE` statements) that must execute **as a whole**.
If any step fails, the database must **roll back** all changes to maintain a consistent state.
Transactions are essential for maintaining **data reliability**, especially in multi-user and concurrent environments.

The **ACID** properties define the guarantees that make transactions dependable and consistent.
Together, they ensure that even in the face of crashes, errors, or concurrent access, the database remains correct and stable.

### A — Atomicity

- A transaction is **all or nothing**.
- If one operation fails, the entire transaction is **rolled back** to its original state.
- Example: Transferring money — both the debit and credit must succeed, or neither happens.

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;  -- or ROLLBACK on failure
```

### C — Consistency

- Every transaction must bring the database from one **valid state** to another.
- All rules, constraints, and triggers must remain satisfied after the transaction completes.
- Example: You cannot insert an order for a non-existent user (foreign key constraint).

### I — Isolation

- Concurrent transactions must behave as if they were executed **sequentially**.
- Uncommitted changes in one transaction are **invisible** to others.
- Prevents issues like dirty reads or lost updates.
- Example: Two users updating the same record won’t overwrite each other’s uncommitted data.

### D — Durability

- Once a transaction is **committed**, it is permanently saved — even if the system crashes immediately afterward.
- Databases achieve this by writing to **non-volatile storage** (like write-ahead logs or disk pages) before confirming the commit.

### _In Short_

**Transaction** Logical unit of work that groups multiple operations.

**ACID** Guarantees that make transactions reliable: Atomic, Consistent, Isolated, Durable.

## **Database Locks**

Locks are mechanisms used by databases to control concurrent access to data, ensuring that multiple transactions can run safely without corrupting or overwriting each other’s changes.

When multiple clients read and modify the same data at once, locks help maintain isolation (the “I” in ACID) by preventing conflicts such as dirty reads, lost updates, or inconsistent states.

### Why Locks Exist

In multi-user environments, two transactions might try to modify the same record simultaneously. Without locking, one transaction could overwrite another’s uncommitted changes, or a query might read inconsistent data. Locks prevent these race conditions by serializing access to critical data until it’s safe to proceed.

### Types of Locks

**Shared Lock (Read Lock)** — Allows multiple transactions to read the same data simultaneously, but prevents any from modifying it until all shared locks are released.
_Example:_ Multiple users can view a product’s details at the same time.

**Exclusive Lock (Write Lock)** — Allows only one transaction to modify data and blocks both reads and writes from others until the lock is released.
_Example:_ When updating a product’s price, no one else can read or modify that row until the update completes.

**Row-Level Lock** — Locks a specific row in a table, providing fine-grained control and better concurrency. Common in relational databases like PostgreSQL and MySQL.

```sql
SELECT * FROM users WHERE id = 1 FOR UPDATE;
```

This locks the selected row for writing — other transactions trying to update it must wait.

**Table-Level Lock** — Locks an entire table, blocking any other read or write operations. It’s simpler but reduces concurrency.

```sql
LOCK TABLE users IN EXCLUSIVE MODE;
```

Often used for maintenance or bulk operations requiring full-table consistency.

**Advisory Locks (Application-Level)** — Locks manually controlled by the application, not tied to specific rows or tables. Useful for synchronizing background jobs or distributed tasks.

```sql
SELECT pg_advisory_lock(12345);
```

PostgreSQL allows creating named locks identified by integers, released manually when done.

### Locking Problems (Concurrency Issues)

Even with locks, concurrency issues can still occur depending on the isolation level. A **dirty read** happens when a transaction reads uncommitted data from another transaction. **Non-repeatable reads** occur when data changes between two reads in the same transaction. **Phantom reads** happen when new rows appear or disappear between identical queries. The most severe issue is a **deadlock**, where two transactions wait on each other’s locks indefinitely. Databases typically detect and resolve deadlocks automatically by aborting one of the transactions.

### Locking Best Practices

Keep transactions short, as long locks cause blocking. Access resources in a consistent order to minimize deadlocks. Prefer row-level locks over table-level locks when possible, and avoid explicit locking unless necessary—let the database’s isolation model handle most concurrency control. Always include retry logic for operations that fail due to lock contention.

### In Short

Locks are the database’s concurrency control mechanism that enforce the Isolation part of ACID. They protect data integrity under parallel access, and when used correctly, they enable safe multi-user operations without creating performance bottlenecks.

---

## Optimizing Slow SQL Queries

Optimizing SQL performance starts with understanding **where the time is spent** — whether it’s scanning too many rows, missing indexes, or performing inefficient joins.

### 1. Use `EXPLAIN` or Query Plan Analysis

Start by inspecting the **query execution plan** using `EXPLAIN` (PostgreSQL, MySQL, etc.). It reveals how the database is fetching data — whether it’s using indexes or performing full table scans.
Look for:

- **Seq Scan (Full Table Scan):** likely needs indexing.
- **Nested Loops or Hash Joins:** may be too expensive on large tables.
- **Sorting or temporary disk usage:** may need better indexing or query limits.

### 2. Add Appropriate Indexes

If a query filters or sorts by a specific column, create an index on that column.
For example:

```sql
CREATE INDEX idx_users_email ON users(email);
```

Avoid over-indexing — too many indexes slow down writes.

### 3. Reduce Data Scanned

Only fetch what you need.

- Select specific columns instead of `SELECT *`.
- Use `LIMIT` for pagination.
- Filter early with `WHERE` to reduce dataset size.

### 4. Optimize Joins

- Ensure **join columns are indexed** on both sides.
- Avoid unnecessary joins — sometimes denormalized or cached data is faster.
- Prefer smaller, filtered subqueries or CTEs instead of joining full tables.

### 5. Use Caching

Cache frequently accessed query results in Redis, Memcached, or the application layer to avoid hitting the database repeatedly.

### 6. Analyze and Maintain Statistics

Databases rely on statistics to choose query plans. Run maintenance commands regularly:

- PostgreSQL: `ANALYZE` or `VACUUM ANALYZE`
- MySQL: `ANALYZE TABLE`

### 7. Consider Denormalization

For read-heavy systems, duplicating or precomputing certain fields (like total order count per user) can reduce join complexity and improve query speed.

### 8. Monitor Slow Query Logs

Enable and analyze **slow query logs** to identify recurring performance bottlenecks.

### In Short

Optimizing queries means reducing the **work the database must do** — by indexing wisely, minimizing scanned data, and leveraging caching. Always start with `EXPLAIN` to understand how the database interprets your query before changing it.

---

## Additional Database Concepts

Beyond indexing, transactions, and locks, several key concepts play important roles in how data is queried, grouped, and summarized.

### Aggregations

Aggregation refers to performing summary calculations on sets of rows, such as `COUNT()`, `SUM()`, `AVG()`, `MIN()`, or `MAX()`. These operations are often combined with `GROUP BY` to produce results per category — for example, counting users by country or calculating total sales per product.

```sql
SELECT country, COUNT(*) FROM users GROUP BY country;
```

### Group By vs. Distinct

Both `GROUP BY` and `DISTINCT` reduce duplicate data, but they serve different purposes.

- `DISTINCT` removes duplicate rows in the final output.
- `GROUP BY` organizes rows into groups for aggregation.

Example:

```sql
SELECT DISTINCT country FROM users;     -- unique countries
SELECT country, COUNT(*) FROM users GROUP BY country;  -- count per country
```

### Annotations (in ORM Contexts)

In frameworks like Django ORM, **annotations** allow adding calculated fields or aggregated results directly to querysets. This avoids separate post-processing in Python code.

```python
from django.db.models import Count
User.objects.values('country').annotate(total=Count('id'))
```

This produces one record per country with the total number of users, similar to a SQL `GROUP BY`.

### Filtering and Ordering

Filtering uses `WHERE` clauses or ORM equivalents (`filter()`) to limit results based on conditions. Ordering (`ORDER BY`) sorts the output for readability or logic, often paired with indexing for performance.

### Views and Materialized Views

- **Views** are saved SQL queries that behave like virtual tables, simplifying complex joins or filters.
- **Materialized Views** physically store the results, improving performance for costly aggregations at the cost of needing manual or scheduled refreshes.

### In Short

Aggregations and annotations summarize data efficiently. `GROUP BY` structures those summaries, while `DISTINCT` focuses on eliminating duplicates. Together with views and proper filtering, they form the foundation of efficient analytical querying.
