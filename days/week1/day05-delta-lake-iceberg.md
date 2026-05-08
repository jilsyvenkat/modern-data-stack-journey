# Day 5 — Delta Lake & Apache Iceberg

## What I learned today
Open table formats solve the fundamental problem of raw data lakes —
Parquet files on S3/GCS/ADLS have no ACID guarantees, no schema
enforcement, no time travel, and no efficient row-level updates.
Delta Lake (Databricks), Apache Iceberg (Netflix/Apple), and Apache
Hudi (Uber) add a metadata and transaction log layer on top of
Parquet files — turning a folder of files into a proper ACID-compliant
table that works across multiple engines. Iceberg is the dominant
choice in 2026 — supported natively by Snowflake, AWS, GCP, and Azure.

## Key concepts

- **Open table format** — a metadata layer on top of Parquet files
  adding ACID transactions, schema evolution, time travel, and
  partition evolution without vendor lock-in.

- **Transaction log** — every change recorded in an immutable log.
  Foundation of ACID guarantees and time travel. Delta calls it
  the Delta Log. Iceberg calls it the Iceberg catalog.

- **ACID transactions** — Atomicity (all or nothing), Consistency
  (data always valid), Isolation (concurrent writes don't corrupt),
  Durability (committed data survives failures).

- **Schema evolution** — add, rename, or reorder columns without
  rewriting data files. Handled in metadata only. Delta and Iceberg
  both support this — critical for long-lived production tables.

- **Time travel** — query any historical snapshot. Delta uses version
  numbers (versionAsOf). Iceberg uses snapshot IDs and timestamps.
  Snowflake Time Travel uses AT (OFFSET) or AT (TIMESTAMP).

- **Partition evolution** — change how data is partitioned without
  rewriting existing files. Iceberg's hidden partitioning is
  particularly powerful — queries don't need to know the partition
  scheme.

- **Multi-engine support** — Iceberg tables readable by Spark,
  Snowflake, Trino, Flink, AWS Athena simultaneously. Write once,
  read anywhere. This is why Iceberg is winning in 2026.

## What I built today

### Delta Lake on Databricks:
- Created Delta table from Python DataFrame
- Registered as SQL table and queried with GROUP BY
- Ran ACID UPDATE — changed order status
- Demonstrated Time Travel with versionAsOf=0
- Viewed full transaction log with delta_table.history()
- Deleted a row and restored entire table to version 0

### Apache Iceberg on Snowflake:
- Created orders_iceberg_demo table from existing raw_orders seed
- Ran INSERT, UPDATE, DELETE — full ACID operations
- Demonstrated Time Travel with AT (OFFSET => -120)
- Compared before/after states with UNION ALL query
- Added two new columns via schema evolution — no data rewrite
- Cloned table instantly for dev environment (Zero-Copy from Day 2)
- Checked storage metrics — active, time travel, failsafe, clone bytes

## Connection to Day 2 Snowflake work

Day 2 features map directly to Iceberg concepts:

| Day 2 Feature | Iceberg Equivalent |
|---------------|-------------------|
| Time Travel AT (OFFSET) | Snapshot time travel |
| Zero-Copy Cloning | Iceberg branch/tag snapshots |
| Fail-safe | Extended snapshot retention |
| Dynamic Tables | Iceberg materialized views |
| Schema changes | Schema evolution |

Everything learned in Day 2 becomes more powerful when understood
in the context of open table formats — Snowflake's Time Travel IS
essentially Iceberg snapshot management under the hood.

## Errors I hit and how I fixed them

## Errors I hit and how I fixed them

| Error | Cause | Fix |
|---|---|---|
| DBFS_DISABLED — Public DBFS root is disabled | Databricks Community Edition disables DBFS root for security | Used Unity Catalog managed tables with saveAsTable() instead of save() to DBFS path |
| NO_SUCH_CATALOG_EXCEPTION — Catalog 'main' not found | Community Edition uses different catalog names than docs show | Ran SHOW CATALOGS to find available catalogs — used 'workspace' instead of 'main' |
| Row order different from expected | Spark distributed processing does not guarantee row order | Normal behaviour — add ORDER BY when order matters |
| Auto OPTIMIZE appeared in transaction log | Databricks automatically optimises Delta tables in background | Expected production behaviour — Auto Optimize compacts small files automatically |
## Open table format comparison

| Feature | Delta Lake | Apache Iceberg | Apache Hudi |
|---------|-----------|----------------|-------------|
| Created by | Databricks | Netflix & Apple | Uber |
| Language | Scala/Python | Java | Java |
| Best engine | Spark/Databricks | Multi-engine | Spark |
| Time travel | Version numbers | Snapshots | Commits |
| Schema evolution | Good | Excellent | Good |
| Multi-engine | Improving | Excellent | Good |
| Snowflake support | Limited | Native | Limited |
| AWS support | S3 Tables | Native Iceberg | Limited |
| Best use case | Databricks shops | Multi-cloud/engine | CDC/upserts |
| 2026 momentum | Strong on Databricks | Dominant overall | Niche |

## Old world vs new world

| Problem (old) | Solution (open table format) |
|---------------|------------------------------|
| Partial writes corrupt data | ACID transactions |
| Anyone writes wrong schema | Schema enforcement |
| Cannot query historical data | Time travel / snapshots |
| Must rewrite files to update | Row-level MERGE/UPDATE |
| Adding column breaks queries | Schema evolution |
| Vendor lock-in | Open standard, multi-engine |
| Slow full table scans | Partition pruning, file skipping |

## How this connects to my work experience

At TCS working with DataStage and flat file pipelines, partial write
failures were a real operational risk — if a job failed halfway
through writing a large file, data was corrupt and manual intervention
was needed overnight. ACID transactions in Delta/Iceberg eliminate
this entirely — either the full write commits or nothing changes.

At Optum managing IRE & UK healthcare data under HIPAA, schema
evolution is directly relevant — source systems add new fields
regularly, and the data platform needs to absorb those changes
without pipeline failures or full table rewrites. Iceberg schema
evolution handles this in metadata only — milliseconds, not hours.

The Zero-Copy Cloning I used in Day 2 for dev environments is
essentially Iceberg's branching concept — instant copies that
only store differences. I was already using Iceberg-style thinking
without knowing the formal terminology.

From a GDPR perspective, Iceberg's snapshot-based architecture means
you can verify exactly what data existed at any point in time —
directly supporting data subject access requests under Article 15
and erasure verification under Article 17.

## Talking points

- "I would choose Iceberg for any multi-cloud or multi-engine
  environment in 2026 — Snowflake, AWS, GCP, and Azure all treat
  it as first-class, eliminating vendor lock-in at the storage layer."

- "Delta Lake is the right choice if the team is already on
  Databricks — the integration is seamless and features like
  Z-ordering and Auto Optimize give significant query performance
  benefits within that ecosystem."

- "Schema evolution in Iceberg is metadata-only — adding a column
  to a table with a billion rows takes milliseconds, not hours.
  That is a fundamental operational improvement over raw Parquet."

- "Open table formats turn data lakes into data lakehouses — you
  get the cost efficiency of object storage with the reliability
  and queryability of a data warehouse. Best of both worlds."

- "The Zero-Copy Cloning I used in Snowflake is essentially the
  same concept as Iceberg branching — instant environment copies
  that only store differences. Snowflake implements Iceberg
  concepts natively."

- "For GDPR compliance, Iceberg snapshots give us an auditable
  record of exactly what data existed at any point — critical for
  data subject access requests and erasure verification."

## Resources
- Delta Lake docs: delta.io/learn
- Apache Iceberg docs: iceberg.apache.org/docs/latest
- Snowflake Iceberg: docs.snowflake.com/en/user-guide/tables-iceberg
- Databricks Community Edition: community.cloud.databricks.com
- My Delta code: /code/delta/delta-lake-demo.py
- My Iceberg/Snowflake code: /code/iceberg/snowflake-iceberg-demo.sql
