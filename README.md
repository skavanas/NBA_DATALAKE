# NBA Data Lake
## About:
This project is an **NBA Player's Data Lake**, designed to fetch, store, and query NBA player statistics using various AWS services. The project integrates **AWS S3**, **AWS Glue**, and **AWS Athena** to manage data and metadata efficiently.
The data is fetched from the **Sportsdata.io API** and stored in **AWS S3**, which serves as the central storage for the data. The **AWS Glue Data Catalog** is used to store the metadata, and **AWS Glue Crawlers** are set up to manage the schema (though it’s already known). **AWS Athena** is used to query the stored data using SQL-like queries.

## Project overview :
<p align="center">
  <img src="https://github.com/user-attachments/assets/77a3a25b-38db-4eb3-a922-00fe5a3f2d00" width="75%" alt="Image 1" style="float:left; margin-right: 10px;">
  <img src="https://github.com/user-attachments/assets/a755f8e4-9db2-4534-9cd2-bd2151988645" width="25%" alt="Image 2" style="float:left;">
</p>

# Steps
1. **Data Fetching**: We fetched data from **Sportsdata.io API** using a **Python** script (boto3).
2. **Data Storage**: We stored that data in a  **AWS s3 bucket**.
3. **Metadata Management**: We used AWS glue for :
* **AWS Glue data catalog** to store metadata of our NBA players' fetched data so it will act as a central repository for other services (AWS Athena,...) . 
* **AWS Glue crawler**, here we already knew the schema of our data, so if we didn't know it, we should create a crawler.
4. **Querying**: We configured AWS Athena (querying context, results location ).

# Technologies that are used in this project :
- **AWS S3**: For data storage
- **AWS Glue**: For managing metadata and schema
- **AWS Athena**: For querying data
- **Python (boto3)**: For interacting with AWS services

# Use Cases:
- Query NBA player statistics with SQL-like commands via **Athena**.
- Store and manage data in a **centralized data lake** in **S3**.
- Use **AWS Glue** to manage metadata and data cataloging.

# How to Get Started:
1. Clone the repository.
2. Configure your AWS environment and `.env` file.
3. Run the Python script to fetch NBA player data and store it in **S3**.
4. Set up **AWS Glue** and **Athena** as per the project setup instructions.


Feel free to contribute to this project by opening issues, creating pull requests, or providing feedback!!!



