import json
import os
import boto3
from datetime import datetime
from utilitiesMethod import FileStatusEnum

s3_resource = boto3.client('s3')
dynamodb_resource = boto3.resource('dynamodb')
TABLE_NAME = os.environ["DDB_TABLE"]
table = dynamodb_resource.Table(TABLE_NAME)

def lambda_handler(event, context):
    for record in event["Records"]:
        body = json.load(record["body"])

        file_id = body["file_id"]
        source_bucket = body["source_bucket"]
        source_key = body["source_key"]
        # Deleting the file from source bucket
        s3_resource.delete_object(

            Bucket=source_bucket,
            key = source_key
        )

        #final updation of dynamodb
        table.put_item(
            Item={
                'file_id': file_id,
                'file_name': source_key,
                'source_bucket': source_bucket,
                'timestamp': datetime.utcnow().isoformat(),
                'status' : FileStatusEnum.FILE_DELETED_FROM_SOURCE.value
            }
        )