# Project overview :
### This project is an NBA player's data Lake, as you can see in the global schema of this project :
<p align="center">
  <img src="https://github.com/user-attachments/assets/77a3a25b-38db-4eb3-a922-00fe5a3f2d00" width="75%" alt="Image 1" style="float:left; margin-right: 10px;">
  <img src="https://github.com/user-attachments/assets/a755f8e4-9db2-4534-9cd2-bd2151988645" width="25%" alt="Image 2" style="float:left;">
</p>


# Steps
### - We fetched data from Sportsdataio using a Python script (boto3).
### - We stored that data in a AWS s3 bucket.
### - We used AWS glue for :
* AWS Glue data catalog to store metadata of our NBA players' fetched data so it will act as a central repository for other services (AWS Athena,...) . 
* AWS Glue crawler, here we already knew the schema of our data, so if we didn't know it, we should create a crawler.
### - We configured AWS Athena (querying context, results location ).
# Technologies that are used in this project :
### AWS S3 , AWS Glue , AWS Athena
### Python (boto 3)



