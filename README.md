📦 ShopEasy Data Pipeline
A full-stack data engineering project demonstrating an end-to-end data pipeline using OLTP, OLAP, and Medallion Architecture. This project ingests raw sales data, cleans and transforms it, and aggregates it for analytics and reporting.
🎯 Project Overview
The ShopEasy project simulates an e-commerce data workflow with multiple layers:
1.Bronze Layer (Raw Data)
Raw CSV/transaction data ingested without transformations
Tables: categories, dates, products, sales, users
2.Silver Layer (Cleaned / Enriched Data)
Cleansed and standardized data for analytics
Tables: products, sales, users
3.Gold Layer (Aggregated / Business Insights)
Tables: sales_summary, top_customers
![Medallion Architecture](<img width="449" height="638" alt="Medallion Architecture" src="https://github.com/user-attachments/assets/e7c4876a-2fb7-4f1f-97dd-af85c976ddb7" />
)

Aggregated data for reporting and dashboards
Tables: sales_summary, top_customers
| Layer                   | Technology                                    |
| ----------------------- | --------------------------------------------- |
| OLTP (Transactional DB) | MySQL / SQLite                                |
| OLAP (Analytical DB)    | PostgreSQL                                    |
| Data Lakehouse          | Bronze/Silver/Gold using Delta Lake + PySpark |
| Scripting / ETL         | Python (pandas, PySpark, Jupyter Notebooks)   |
| Analytics               | Power BI (snapshot)                           |


ShopEasy/
│
├─ bronze/                  # Raw ingested data
│   ├─ categories
│   ├─ dates
│   ├─ products
│   ├─ sales
│   └─ users
│
├─ silver/                  # Cleaned and enriched data
│   ├─ products
│   ├─ sales
│   └─ users
│
├─ gold/                    # Aggregated data for reporting
│   ├─ sales_summary
│   └─ top_customers
│
├─ bronzz.ipynb             # Notebook for Bronze layer ingestion
├─ oltp.py                  # OLTP scripts (data insertion / extraction)
├─ olap.py                  # OLAP scripts (ETL for analytics)
├─ test.ipynb               # Testing / experimentation notebooks
└─ README.md                # Project documentation

⚡ Features
End-to-End Data Pipeline from raw data → cleaned → aggregated
Implements Medallion Architecture (Bronze/Silver/Gold layers)
Supports OLTP for transactional operations and OLAP for analytics
Ready for BI reporting (Power BI or any visualization tool)
Modular and easy to extend for new datasets

📊 Analytics / Reporting
Aggregated data in Gold layer can be used in Power BI


