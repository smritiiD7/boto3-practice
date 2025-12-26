import json
import os
import uuid
from datetime import datetime
import boto3
from utilitiesMethod import FileTypeEnum, FileStatusEnum

s3_resource = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sqs = boto3.client("sqs")

TABLE_NAME = os.environ['DDB_TABLE']
IMAGE_BUCKET = os.environ['IMAGE_BUCKET']
PDF_BUCKET = os.environ['PDF_BUCKET']
CSV_BUCKET = os.environ['CSV_BUCKET']
DEFAULT_BUCKET = os.environ['DEFAULT_BUCKET']
DELETE_QUEUE_URL = os.environ['DELETE_QUEUE_URL']

table = dynamodb.Table(TABLE_NAME)

def get_destination_bucket(file_key: str):
    file_extension = file_key.split('.')[-1].lower()
    if file_extension in [FileTypeEnum.JPG.value, FileTypeEnum.JPEG.value, FileTypeEnum.PNG.value]:
        return IMAGE_BUCKET 
    elif file_extension == FileTypeEnum.PDF.value:
        return PDF_BUCKET       
    elif file_extension == FileTypeEnum.CSV.value:
        return CSV_BUCKET
    return DEFAULT_BUCKET

def lambda_handler(event, context):
    for record in event["Records"]:
        source_bucket = record["s3"]["bucket"]["name"]
        file_key = record["s3"]["object"]["key"]

        file_id = str(uuid.uuid4())
        destination_bucket = get_destination_bucket(file_key)

        # updating DynamoDB with initial status on manual upload FILE_MANUALLY_UPLOADED
        table.put_item(
            Item={
                'file_id': file_id,
                'file_name': file_key,
                'source_bucket': source_bucket,
                'destination_bucket': destination_bucket,
                'timestamp': datetime.utcnow().isoformat(),
                'status' : FileStatusEnum.FILE_MANUALLY_UPLOADED.value
            }
        )

        s3_resource.copy_object(
            Bucket=destination_bucket,
            CopySource={'Bucket': source_bucket, 'Key': file_key},
            Key=file_key
        )

#sending message to SQS for deletion as payload
        sqs.send_message(
        QueueUrl=DELETE_QUEUE_URL,
        MessageBody=json.dumps({
        "file_id": file_id,
        "source_bucket": source_bucket,
        "source_key": file_key,
        "destination_bucket": destination_bucket,
        "timestamp": datetime.utcnow().isoformat()
    })
)

        # updating the DynamoDB with status after file transfer FILE_TRANSFERRED_TO_DESTINATION
        table.put_item(
            Item={
                'file_id': file_id,
                'file_name': file_key,
                'source_bucket': source_bucket,
                'destination_bucket': destination_bucket,
                'timestamp': datetime.utcnow().isoformat(),
                'status' : FileStatusEnum.FILE_TRANSFERRED_TO_DESTINATION.value
            }
        )

        """s3_resource.delete_object(
            Bucket=source_bucket,
            Key=file_key
        ) """

        # updating the DynamoDB with status after file deletion FILE_DELETED_FROM_SOURCE
        """table.put_item(
            Item={
                'file_id': file_id,
                'file_name': file_key,
                'source_bucket': source_bucket,
                'destination_bucket': destination_bucket,
                'timestamp': datetime.utcnow().isoformat(),
                'status' : FileStatusEnum.FILE_DELETED_FROM_SOURCE.value
            }
        )"""
        
    return {"statusCode" : 200}