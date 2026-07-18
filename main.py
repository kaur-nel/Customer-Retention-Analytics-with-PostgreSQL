import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. EXTRACT: Load the messy CSV
df = pd.read_csv('online_retail.csv', encoding='unicode_escape')
df.columns = df.columns.str.lower()
# 2. TRANSFORM: Clean the data
# Drop rows with no CustomerID
df_clean = df.dropna(subset=['customerid'])

# Remove refunds/cancellations (Quantity must be greater than 0)
df_clean = df_clean[df_clean['quantity'] > 0]

# Ensure the InvoiceDate is actually treated as a Date, not text
df_clean['invoicedate'] = pd.to_datetime(df_clean['invoicedate'])

# 3. LOAD: Push it into a local SQL database
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://username:password@localhost:5432/retail_project"
)

df_clean.to_sql('retaildata', engine, index=False, if_exists='replace')

print("ETL Complete! The clean data is now in the 'RetailData' SQL table.")

# 4. Write the Cohort SQL Query
queries = [
    """
    SELECT
        customerid,
        DATE_TRUNC('month', MIN(invoicedate)) AS acquisition_month
    FROM retaildata
    GROUP BY customerid
    ORDER BY customerid;
    """,

    """
    SELECT DISTINCT
        customerid,
        DATE_TRUNC('month', invoicedate) AS activity_month
    FROM retaildata
    ORDER BY customerid, activity_month;
    """ ,
    
    """
    WITH acquisition AS (
        SELECT
            customerid,
            DATE_TRUNC('month', MIN(invoicedate)) AS cohort_month
        FROM retaildata
        GROUP BY customerid
    ),

    activity AS (
        SELECT DISTINCT
            customerid,
            DATE_TRUNC('month', invoicedate) AS activity_month
        FROM retaildata
    )

    SELECT
        a.customerid,
        a.cohort_month,
        ac.activity_month,
        -- Calculate the difference in months (Month Index)
        (
            EXTRACT(YEAR FROM ac.activity_month) * 12 +
            EXTRACT(MONTH FROM ac.activity_month)
        ) -
        (
            EXTRACT(YEAR FROM a.cohort_month) * 12 +
            EXTRACT(MONTH FROM a.cohort_month)
        ) AS month_index
        FROM acquisition a
        JOIN activity ac
            ON a.customerid = ac.customerid
        ORDER BY a.customerid, month_index;
    """ ,
    
    """
    WITH acquisition AS (
        SELECT
            customerid,
            DATE_TRUNC('month', MIN(invoicedate)) AS cohort_month
        FROM retaildata
        GROUP BY customerid
    ),

    activity AS (
        SELECT DISTINCT
            customerid,
            DATE_TRUNC('month', invoicedate) AS activity_month
        FROM retaildata
    ),

    cohort_offsets AS (
        SELECT
            a.customerid,
            a.cohort_month,
            (
                EXTRACT(YEAR FROM ac.activity_month) * 12 +
                EXTRACT(MONTH FROM ac.activity_month)
            ) -
            (
                EXTRACT(YEAR FROM a.cohort_month) * 12 +
                EXTRACT(MONTH FROM a.cohort_month)
            ) AS month_index
        FROM acquisition a
        JOIN activity ac
            ON a.customerid = ac.customerid
    )

    -- Final Aggregation Step
    SELECT
        cohort_month,
        month_index,
        COUNT(DISTINCT customerid) AS active_users
    FROM cohort_offsets
    GROUP BY cohort_month, month_index
    ORDER BY cohort_month, month_index;
    """
]

for query in queries:
       # Run the query and view results
       df_results = pd.read_sql_query(query, engine)
       print(df_results)
       
       
cohort_df = df_results.copy()
cohort_df = pd.read_sql_query(queries[-1], engine)

cohort_pivot = cohort_df.pivot(
    index='cohort_month',
    columns='month_index',
    values='active_users'
)

print(cohort_pivot)

cohort_size = cohort_pivot[0]
retention = cohort_pivot.divide(cohort_size, axis=0) * 100
print(retention)

plt.figure(figsize=(12, 8))

sns.heatmap(
    retention,
    annot=True,
    fmt=".1f",
    cmap="YlGnBu",
    linewidths=0.5,
    vmin=0,
    vmax=100
)

plt.title("Customer Retention Heatmap")
plt.xlabel("Month Index")
plt.ylabel("Cohort Month")

plt.tight_layout()
plt.savefig(
    "cohort_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
