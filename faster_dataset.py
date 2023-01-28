import pandas as pd
#
# # Create a dataframe with the information
# Dask: Dask is a powerful library for parallel and distributed computing in Python. It can handle large datasets using multiple cores and/or multiple machines and it can be a good option for data larger than 1 lakh records.
#
# Swifter: Swifter is a library that aims to make it easy to parallelize operations on Pandas dataframes. It can be used to speed up operations on large datasets by performing them in parallel. However, it's not as efficient as dask when dealing with large datasets.
#
# Numba: Numba can be used to accelerate the performance of Python code. It can be used to speed up operations on large datasets by compiling Python code to machine code. It can be a good option for data larger than 1 lakh records, but it's not as efficient as dask or cudf
#
# Ray: Ray is a library for parallel and distributed computing in Python. It can be used to parallelize operations on dataframes and perform them much faster than using Pandas alone. It's similar to Dask, but it's more focused on performance and ease of use.
#
# Modin: Modin is a library that aims to make it easy to parallelize operations on Pandas dataframes. It can be used to speed up operations on large datasets by performing them in parallel. However, it's not as efficient as dask when dealing with large datasets.
#
# Apache Arrow: Apache Arrow is a library for working with columnar data in memory. It can be used to optimize performance when working with large datasets by reducing the amount of data that needs to be read from disk or sent over the network. It's not as efficient as dask or cudf when dealing with large datasets.
#
# cuDF: cuDF is a library for working with GPU Dataframe, it's a part of the RAPIDS ecosystem and it's designed to handle large datasets. It can be very efficient when working with large datasets, especially when the dataset is too big to fit in memory and the operations are mainly numerical operations.
df = pd.DataFrame({'Library': ['Dask', 'cuDF', 'Vaex', 'Modin', 'RAPIDS', 'PySpark', 'Koalas', 'PyData'],
                   'Description': ['A distributed computing library', 'A GPU-accelerated dataframe library',
                                   'A high-performance library for lazy Out-of-Core DataFrames',
                                   'An alternative to Pandas that runs on top of Dask',
                                   'A suite of libraries for working with large datasets on GPUs',
                                   'Python library for Spark programming',
                                   'A library that provides a DataFrame API similar to Pandas but it runs on top of Apache Spark',
                                   'Set of libraries for working with large datasets in Python']})

# Save the dataframe to an excel file
df.to_excel('large_datasets_libraries.xlsx', index=False)