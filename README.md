# Customer Retention Analytics using SQL Cohort Analysis
An end-to-end Data Analytics project that builds a complete ETL pipeline to measure customer retention using SQL Cohort Analysis on the UCI Online Retail (2010–2011) dataset.

Instead of performing all calculations in Python, this project leverages a relational database to execute heavy analytical operations, making the workflow more scalable and closer to real-world data engineering practices.

## Project Overview
Businesses spend significant resources acquiring new customers, but **customer retention** ultimately determines long-term profitability.

This project answers questions like:

- Are customers returning after their first purchase?
- How quickly does customer retention decline?
- Are marketing efforts creating loyal customers?

The pipeline performs:

- Extract raw transaction data
- lean anomalies using **Pandas**
- Load cleaned data into **PostgreSQL**
- Execute **SQL Cohort Analysis**
- Calculate monthly **Retention Rates**
- Generate a **Retention Heatmap**


**Dataset:** [Online Retail Dataset (UCI)](https://archive.ics.uci.edu/ml/datasets/Online+Retail)

## Features

- End-to-End **ETL Pipeline**
- Automated Data Cleaning using **Pandas**
- SQL Cohort Analysis using **Common Table Expressions (CTEs)**
- PostgreSQL Data Aggregation
- Monthly Customer Retention Analysis
- Retention Percentage Calculation
- Heatmap Visualization using **Seaborn**
- Database-first Analytical Workflow

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | ETL Pipeline |
| **Pandas** | Data Cleaning |
| **PostgreSQL** | Database |
| **SQLAlchemy** | Database Connectivity |
| **SQL (CTEs)** | Cohort Analysis |
| **Matplotlib** | Data Visualization |
| **Seaborn** | Retention Heatmap |


## Project Structure
```text
Customer-Retention-Analytics/
│
├── cohort_heatmap.png      # Generated retention heatmap
├── main.py                 # ETL pipeline & cohort analysis
├── online_retail.csv       # Raw dataset
├── README.md
└── requirements.txt
```


## Setup and Installation 

### Clone the Repository

```bash
git clone https://github.com/kaur-nel/Customer-Retention-Analysis.git
```

```bash
cd Customer-Retention-Analytics
```

---

### Install Dependencies

Using the requirements file:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install pandas matplotlib seaborn sqlalchemy psycopg2
```

---

### Create PostgreSQL Database

```sql
CREATE DATABASE retail_project;
```

---

### Configure the Database Connection

Open **main.py** and update the connection string.

```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://username:password@localhost:5432/retail_project"
)
```

---

### Run the Project

```bash
python main.py
```

The pipeline automatically:

- Cleans the raw dataset
- Loads data into PostgreSQL
- Executes SQL Cohort Analysis
- Calculates retention percentages
- Generates the heatmap
- Saves the visualization as:

```text
cohort_heatmap.png
```

### Output Screenshots

#### Pivot table 
![alt text](image-1.png)
#### Heatmap
![alt text](cohort_heatmap.png)



