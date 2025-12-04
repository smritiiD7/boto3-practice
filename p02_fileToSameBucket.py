import boto3
from utilitiesMethod import return_date_time

#creating single bucket resource
s3_resource = boto3.resource('s3', region_name='us-east-1')
current_time_meta_data = return_date_time()

#s3 bucket name
bucket_name = f"intra-bucket-transfer-tsft"+current_time_meta_data

#CREATING BUCKET
if bucket_name not in s3_resource.buckets.all():
    print(f"{bucket_name} bucket does not exists, creating now..")
    s3_resource.create_bucket(Bucket=bucket_name)
    print(f"{bucket_name} bucket has been created")
else:
    print(f"{bucket_name} bucket already exists")

file_local_path = "resources/file_transfer/test.txt"
bck_src_path = "src/test.txt"  

#uploading file from local to bucket
s3_resource.Bucket(bucket_name).upload_file(Filename=file_local_path, Key=bck_src_path)
print(f"FILE_UPLOADED_TO_BUCKET: {bucket_name}")

#copying file within same bucket from source path to destination path
copy_source = {
    'Bucket': bucket_name,'Key': bck_src_path }

destination_key = "des/test.txt"

s3_resource.Bucket(bucket_name).copy(copy_source, destination_key)
print(f"FILE_COPIED_WITHIN_SAME_BUCKET: {bucket_name}")

#emptying source file after copy
# s3_resource.Object(bucket_name, bck_src_path).delete()  
# print(f"FILE_DELETED_FROM_SOURCE_PATH: {bucket_name}")

# Cleanup - Deleting the bucket
# s3_resource.Bucket(bucket_name).delete()
# print(f"BUCKET_DELETED: {bucket_name}")
