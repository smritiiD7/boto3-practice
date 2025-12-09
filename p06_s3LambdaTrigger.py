import boto3

s3_client  = boto3.client('s3')

src_bucket = "richa07-botobucket-src"
des_bucket = "richa07-botobucket-dst"



def lambda_handler(event, context):
    record = event["Records"][0]
    src_key = record["s3"]["object"]["key"]

    des_key = src_key

    s3_client.copy_object(
        Bucket = des_bucket,
        CopySource = {'Bucket': src_bucket, 'Key': src_key},
        Key = des_key
    )

    return {
        "status": "File Copied Successfully",
        "message": f"File copied from {src_bucket}/{src_key} to {des_bucket}/{des_key}"
    }