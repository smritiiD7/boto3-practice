#Transfer of file from source to destination
import boto3
from utilitiesMethod import return_date_time

#The buckets where objects are stored
s3_resource = boto3.resource('s3', region_name='us-east-1')
current_time_meta_data = return_date_time()

bucket_src = f"s3-source-bucket-tsft"+current_time_meta_data
bucket_des = f"s3-destination-bucket-tsft"+current_time_meta_data

#CREATING BUCKETS
if bucket_src not in s3_resource.buckets.all():
    print(f"{bucket_src} bucket does not exists, creating now..")
    s3_resource.create_bucket(Bucket=bucket_src)
    print(f"{bucket_src} bucket has been created")


if bucket_des not in s3_resource.buckets.all():
    print(f"{bucket_des} bucket does not exists, creating now..")
    s3_resource.create_bucket(Bucket=bucket_des)
    print(f"{bucket_des} bucket has been created")


file_local_path = "resources/file_transfer/test.txt"
bck_src_path = "src/test.txt"
#uploading file from local to bucket_src
s3_resource.Bucket(bucket_src).upload_file(Filename=file_local_path, Key=bck_src_path)
print(f"FILE_UPLOADED_TO_SRC_BUCKET: {bucket_src}")

copy_source = {
    'Bucket': bucket_src,
    'Key': bck_src_path
}

destination_key = "des/test.txt"

s3_resource.Bucket(bucket_des).copy(copy_source, destination_key)
print(f"FILE_COPIED_TO_DESTINATION_BUCKET: {bucket_des}")

s3_resource.Object(bucket_src, bck_src_path).delete()
print(f"FILE_DELETED_FROM_SOURCE_BUCKET: {bucket_src}")





