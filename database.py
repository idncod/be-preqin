import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def get_dynamodb():
    """Returns a DynamoDB resource instance."""
    return boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION", "eu-north-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

def get_table():
    """Returns the UsersTable DynamoDB table instance."""
    dynamodb = get_dynamodb()
    return dynamodb.Table("UsersTable")

