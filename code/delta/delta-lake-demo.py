# Day 5 — Delta Lake on Databricks
# All cells use workspace.delta_demo catalog
# Tested on Databricks Community Edition — May 2026

# ── Cell 1 — Create Delta table ──────────────────────────────────────
from pyspark.sql.types import *
import pyspark.sql.functions as F

data = [
    (1, 1, "2024-01-01", "completed",  99.99),
    (2, 2, "2024-01-02", "returned",   49.99),
    (3, 1, "2024-01-03", "completed", 149.99),
]

schema = StructType([
    StructField("order_id",    IntegerType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("order_date",  StringType(),  True),
    StructField("status",      StringType(),  True),
    StructField("amount",      DoubleType(),  True),
])

df = spark.createDataFrame(data, schema)
spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.delta_demo")
df.write.format("delta").mode("overwrite").saveAsTable("workspace.delta_demo.orders")
print("Delta table created successfully!")
df.show()

# ── Cell 2 — Query with SQL ───────────────────────────────────────────
spark.sql("""
    SELECT
        status,
        COUNT(*)    as order_count,
        ROUND(SUM(amount), 2) as total_amount
    FROM workspace.delta_demo.orders
    GROUP BY status
    ORDER BY status
""").show()

# ── Cell 3 — ACID Update ──────────────────────────────────────────────
from delta.tables import DeltaTable

delta_table = DeltaTable.forName(spark, "workspace.delta_demo.orders")
delta_table.update(
    condition = F.col("order_id") == 2,
    set = {"status": F.lit("completed")}
)
print("After ACID update — order 2 changed from returned to completed:")
spark.table("workspace.delta_demo.orders").show()

# ── Cell 4 — Time Travel ──────────────────────────────────────────────
df_v0 = spark.read.format("delta") \
    .option("versionAsOf", 0) \
    .table("workspace.delta_demo.orders")

print("Version 0 — original data before update:")
df_v0.show()
print("Current version — after update:")
spark.table("workspace.delta_demo.orders").show()

# ── Cell 5 — Transaction Log ──────────────────────────────────────────
delta_table = DeltaTable.forName(spark, "workspace.delta_demo.orders")
print("Full transaction history:")
delta_table.history().select(
    "version",
    "timestamp",
    "operation",
    "operationParameters"
).show(truncate=False)

# ── Cell 6 — Delete and Restore ───────────────────────────────────────
delta_table.delete(condition = F.col("order_id") == 3)
print("After delete — only 2 rows:")
spark.table("workspace.delta_demo.orders").show()

spark.sql("RESTORE TABLE workspace.delta_demo.orders TO VERSION AS OF 0")
print("After restore to version 0 — all 3 rows back with original status:")
spark.table("workspace.delta_demo.orders").show()
