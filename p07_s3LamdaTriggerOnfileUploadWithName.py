import boto3

s3_client  = boto3.client('s3')

src_bucket = "inter-bucket-transfer-tsft202512041"
des_bucket = "employee-offer-letters"

def lambda_handler(event, context):
    record = event["Records"][0]
    src_key = record["s3"]["object"]["key"]

    # Extract the file name from the source key
    file_name = src_key.split('/')[-1]

   #extracting the employee ID from the file name assuming the format is "employeeID_*.* -> Ye hoga useful for the project 
    emp_id = file_name.split('_')[0]


    #check if the folder with employee ID exists in the destination bucket
    result  = s3_client.list_objects_v2(
        Bucket = des_bucket,
        Prefix = emp_id + '/'
    )

    folder_exists = 'Contents' in result #yaha basically check kar raha hai ki contents key exist karti hai ya nahi

    if not folder_exists:
        #create a folder with employee ID in the destination bucket
        s3_client.put_object(
            Bucket = des_bucket,
            Key = emp_id + '/'
        )
    des_key = emp_id + '/' + file_name

    s3_client.copy_object(
        Bucket = des_bucket,
        CopySource = {'Bucket': src_bucket, 'Key': src_key},
        Key = des_key
    )

    return { 
        "status": "File Copied Successfully",
        "message": f"File copied from {src_bucket}/{src_key} to {des_bucket}/{des_key}"
    }