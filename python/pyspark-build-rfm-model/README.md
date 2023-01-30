# Build a recency, frequency and monetary (RFM) model in PySpark:

Given a table of customer orders over the past 90-days, such as:

```bash
customer_id	last_order	num_orders	total_revenue
```

Where:

* `customer_id`: is unique customer identifier
* `last_order`: denotes most recent order N days ago
* `num_orders`: total number of orders in last 90-days
* `total_revenue`: total revenue of purchases

In a PySpark session, load the pre-processed customer order data:

```python
def calculate_quantiles(arr: list = [], quantiles: list = [0.25, 0.5, 0.75]):
    """Given a list of values, calculate the given quantiles.

    Args:
        arr: array of values to compute quantiles
        quantiles: quantiles to be calculated

    Returns:
        qarr: quantile array

    """
    qarr = np.quantile(a=arr, q=quantiles)
    return qarr


from pyspark.sql.functions import concat, when, lit, col

# Calculate quantiles for each metric:
r_quartile = calculate_quantiles(arr=range(0, 91))  # Since back-fill date range is fixed to 90-days.
f_quartile = calculate_quantiles(arr=data.select('num_orders').distinct().collect())
m_quartile = calculate_quantiles(arr=data.select('total_revenue').distinct().collect())i

# Score each user according to their RFM profile:
rfm = (data.withColumn('recency',
                       when(col("last_order") >= r_quartile[2], 1).
                       when((col("last_order") >= r_quartile[1]) & (col("last_order") < r_quartile[2]), 2).
                       when((col("last_order") >= r_quartile[0]) & (col("last_order") < r_quartile[1]), 3).
                       otherwise(4)))
rfm = (rfm.withColumn('frequency',
                      when(col("num_orders") >= f_quartile[2], 4).
                      when((col("num_orders") >= f_quartile[1]) & (col("num_orders") < f_quartile[2]), 3).
                      when((col("num_orders") >= f_quartile[0]) & (col("num_orders") < f_quartile[1]), 2).
                      otherwise(1)))
rfm = (rfm.withColumn('monetary', when(col("total_revenue") >= m_quartile[2], 4).
                      when((col("total_revenue") >= m_quartile[1]) & (col("total_revenue") < m_quartile[2]), 3).
                      when((col("total_revenue") >= m_quartile[0]) & (col("total_revenue") < m_quartile[1]), 2).
                      otherwise(1)))

# Add a composite RFM column:
rfm = rfm.withColumn('rfm', concat(col('recency'), col('frequency'), col('monetary')))
```
