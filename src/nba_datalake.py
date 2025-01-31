import boto3
import requests
import json
import time
import os 
from dotenv import load_dotenv

load_dotenv()

#loading environement variables from .env

region=os.getenv("region")
url=os.getenv("API_URL")
api_key=os.getenv("API_KEY")
bucket=os.getenv("bucket_name")
glue_db_name=os.getenv("glue_db")

#creating aws clients (s3,athena,glue)

s3_client=boto3.client("s3")
glue_client=boto3.client("glue")
athena_client=boto3.client("athena")

#function to create s3 bucket if doesn't exists 
def Create_s3():
    if s3_client.head_bucket('bucket'):
           print(f"bucket : {bucket} already exists")
    else:
        try:        
            if region=="us-east-1":
                response= s3_client.create_bucket(Bucket='bucket',)
            else:
                response= s3_client.create_bucket(
                    Bucket='bucket',
                    CreateBucketConfiguration={
                        'LocationConstraint':region,
                        },
                    )
        except Exception as e:
            print(f"cannot create the s3 bucket:{e}")

#create glue

def Create_glue():
    try:
        response=glue_client.create_database(
            DatabaseInput={
                'Name': glue_db_name,
                'Description': 'this db is just for NBA data ',
            }
        )
        print(f"glue db created successfully")
    except Exception as e:
        print(f"cannot create the glue db {e}")

#get data from datasports api
def fetch_data():
    try:
        headers = {"Ocp-Apim-Subscription-Key": api_key}
        response=requests.get("url",headers=headers)
        response.raise_for_status()
        print(f"data fetched successfully")
        return response.json()
    except Exception as e:
        print(f"cannot fetch data {e}")
        return []

