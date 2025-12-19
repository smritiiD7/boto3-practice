import os
import uuid
from datetime import datetime
import boto3

s3_resource = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

TABLE_NAME = os.environ['DDB_TABLE']
IMAGE_BUCKET = os.environ['IMAGE_BUCKET']
PDF_BUCKET = os.environ['PDF_BUCKET']
CSV_BUCKET = os.environ['CSV_BUCKET']
DEFAULT_BUCKET = os.environ['DEFAULT_BUCKET']

table = dynamodb.Table(TABLE_NAME)

def get_destination_bucket(file_key: str):
    file_extension = file_key.split('.')[-1].lower()
    if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
        return IMAGE_BUCKET 
    elif file_extension == 'pdf':
        return PDF_BUCKET       
    elif file_extension == 'csv':
        return CSV_BUCKET
    return DEFAULT_BUCKET

def lambda_handler(event, context):
    for record in event["Records"]:
        source_bucket = record["s3"]["bucket"]["name"]
        file_key = record["s3"]["object"]["key"]

        file_id = str(uuid.uuid4())
        destination_bucket = get_destination_bucket(file_key)

        s3_resource.copy_object(
            Bucket=destination_bucket,
            CopySource={'Bucket': source_bucket, 'Key': file_key},
            Key=file_key
        )

        s3_resource.delete_object(
            Bucket=source_bucket,
            Key=file_key
        )

        timestamp = datetime.utcnow().isoformat()


        table.put_item(
            Item={
                'file_id': file_id,
                'file_name': file_key,
                'source_bucket': source_bucket,
                'destination_bucket': destination_bucket,
                'timestamp': timestamp
            }
        )

        return {"statusCode" : 200}