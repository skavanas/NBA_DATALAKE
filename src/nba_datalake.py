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
glue_table_name=os.getenv("glue_table")
athena_output=os.getenv("athena_output")

#creating aws clients (s3,athena,glue)

s3_client=boto3.client("s3")
glue_client=boto3.client("glue")
athena_client=boto3.client("athena")

#function to create s3 bucket if doesn't exists 
def Create_s3():
    try:
            s3_client.head_bucket(Bucket=bucket)
            print(f"bucket : {bucket} already exists")
    except:
        try:        
            if region=="us-east-1":
                response= s3_client.create_bucket(Bucket=bucket,)
            else:
                response= s3_client.create_bucket(
                    Bucket=bucket,
                    CreateBucketConfiguration={
                        'LocationConstraint':region,
                        },
                    )
        except Exception as e:
            print(f"cannot create the s3 bucket:{e}")

#create glue database

def Create_glue():
    try:
        if glue_client.get_database(Name=glue_db_name):
            print(f"glue database  {glue_db_name} already exists ")
        else:
            glue_client.create_database(
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
        response=requests.get(url,headers=headers)
        response.raise_for_status()
        print(f"data fetched successfully")
        return response.json()
    except Exception as e:
        print(f"cannot fetch data {e}")
        return []

#storing data form the api to s3 
def storing_data_s3(data):
    line_delimited_data="/n".join([json.dumps(d) for d in data])
    try:    
        response=s3_client.put_object(
            Body=line_delimited_data,
            Bucket=bucket,
            Key="data/nba_player_data.jsonl",
        )
        print(f"data uploaded to S3")
    except Exception as e :
        print(f"cannot store data in the s3 bucket : {e} ")

def Create_glue_table():
    try:
            glue_client.get_table(DatabaseName=glue_db_name, Name=glue_table_name)
            print("glue nba-players-data table already exists")
    except Exception as e:
        if e.response["Error"]["Code"] == "EntityNotFoundException":
            try:   
                glue_client.create_table(
                    DatabaseName=glue_db_name,
                    TableInput={
                        'Name': glue_table_name,
                        'Description': 'this data contains data about nba players',
                        'StorageDescriptor': {
                            'Columns': [
                                {"Name": "PlayerID", "Type": "int"},
                                {"Name": "FirstName", "Type": "string"},
                                {"Name": "LastName", "Type": "string"},
                                {"Name": "Team", "Type": "string"},
                                {"Name": "Position", "Type": "string"},
                                {"Name": "Points", "Type": "int"}
                            ],
                            "Location": f"s3://{bucket}/data/",
                            "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
                            "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                            "SerdeInfo": {
                                "SerializationLibrary": "org.openx.data.jsonserde.JsonSerDe"
                            },
                        }
                    },
                )
                print(f"table was created successfully....")
            except:
                print(f"error creating table :{e}")
        else:
            print(f"error creating table :{e}")
        
#comfiguration de athena 
def athena_config():
    try:
        response=athena_client.start_query_execution(
            QueryString="CREATE DATABASE IF NOT EXISTS nbadata2",
            QueryExecutionContext={
                'Database': glue_db_name,
            },
            ResultConfiguration={
               'OutputLocation': athena_output,
            }
        )
        print("Athena output location configured successfully.")
    except Exception as e:
        print(f"Error configuring Athena: {e}")

def main():
    print("setting up the NBA data Lake......")    
    #operating on s3
    Create_s3()
    NBAPlayersData=fetch_data()
    if NBAPlayersData:
        storing_data_s3(NBAPlayersData)  #ensuring that the fetched data isn't null
     
        #operating on AWS glue
        Create_glue()
        Create_glue_table()
        
        #AWS Athena 
        
        athena_config()

        print("data Lake is setted up successfully ..")
    
if __name__ == "__main__":
    main()




