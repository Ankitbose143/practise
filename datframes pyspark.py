from pyspark.sql import SparkSession
from pyspark.sql.functions import col, row_number, rank, dense_rank
from pyspark.sql.window import Window

# Initialize SparkSession
spark = SparkSession.builder.appName("WindowFunctions").getOrCreate()

# Sample DataFrame
data = [
    ('2025-01-01', 'Alice', 90000),
    ('2025-01-01', 'Bob', 85000),
    ('2025-01-01', 'Charlie', 85000),
    ('2025-01-02', 'David', 95000),
    ('2025-01-02', 'Eve', 90000)
]
columns = ['date', 'employee', 'salary']

df = spark.createDataFrame(data, columns)

# Define the Window Specification
window_spec = Window.partitionBy("date").orderBy(col("salary").desc())

# Calculate row_number
row_number_df = df.withColumn("row_number", row_number().over(window_spec))

# Calculate rank
rank_df = df.withColumn("rank", rank().over(window_spec))

# Calculate dense_rank
dense_rank_df = df.withColumn("dense_rank", dense_rank().over(window_spec))

# Show results
print("Row Number Result:")
row_number_df.show()

print("Rank Result:")
rank_df.show()

print("Dense Rank Result:")
dense_rank_df.show()
--------------------------------------------------------------------------------------------------
from pyspark.sql import SparkSession

# Initialize SparkSession
spark = SparkSession.builder.appName("JoinExample").getOrCreate()

# Sample DataFrames
data1 = [(1, 'Alice', 30), (2, 'Bob', 25), (3, 'Charlie', 35)]
data2 = [(1, 'Alice', 'HR'), (2, 'Bob', 'Finance'), (4, 'Eve', 'IT')]

columns1 = ['id', 'name', 'age']
columns2 = ['id', 'name', 'department']

df1 = spark.createDataFrame(data1, columns1)
df2 = spark.createDataFrame(data2, columns2)

# Join with multiple conditions
joined_df = df1.join(df2, (df1.id == df2.id) & (df1.name == df2.name), "inner")

# Show result
joined_df.show()

# Left Anti Join
left_anti_df = df1.join(df2, (df1.id == df2.id) & (df1.name == df2.name), "left_anti")

# Show result
left_anti_df.show()

# Right Join
right_join_df = df1.join(df2, (df1.id == df2.id) & (df1.name == df2.name), "right")

# Show result
right_join_df.show()


# Merge rows using union
merged_rows_df = df1.union(df2)

# Show result
merged_rows_df.show()

---------------------------------filter
# Filter rows where age > 25 and name is 'Alice'
filtered_rows_multi_cond_df = df1.filter((df1.age > 25) & (df1.name == "Alice"))

filtered_rows_multi_cond_df.show()

# Use 'where' to filter rows where id = 2
where_filtered_df = df1.where(df1.id == 2)

where_filtered_df.show()

# Filter rows where age > 25 and then select 'id' and 'name'
combined_filter_df = df1.filter(df1.age > 25).select("id", "name")

combined_filter_df.show()
--------------------------------union
# Union (removes duplicates)
union_df = df1.union(df2)

# Union and remove duplicates explicitly
union_distinct_df = df1.union(df2).distinct()

df2_aligned = df2.selectExpr("id", "name", "age as age")

aligned_union_df = df1.union(df2_aligned)
-----------------------------------cast

df_casted = df.withColumn("age", df["age"].cast(StringType()))

