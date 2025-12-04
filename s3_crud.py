import boto3

s3  = boto3.resource('s3', region_name="us-east-1")
bucket_name = 'richa07-botobucket01'

all_my_buckets = [bucket.name for bucket in s3.buckets.all()]

if bucket_name not in all_my_buckets:
    print(f"{bucket_name} bucket does not exists. Creating now...." )
    s3.create_bucket(Bucket=bucket_name)
    print(f"{bucket_name} bucket has been created")
else:
    print(f"{bucket_name} bucket already exists, no need to create new one.")

for bucket in s3.buckets.all():
    print(f"Listing down the bucket name: {bucket.name}")

file1_obj = 'file1.txt'
file2_obj= 'file2.txt'

s3.Bucket(bucket_name).upload_file(Filename=file1, Key=file1_bj)
s3.Bucket(bucket_name).upload_file(Filename=file2, Key=file2_obj)

obj = s3.Object(bucket_name, file1)
body = obj.get()['Body'].read()
print(body)

s3.Object(bucket_name, file1).put(Body=open(file2, 'rb')) #S3 put() expects the file body as a bytes stream, not text.
obj = s3.Object(bucket_name, file1)
body = obj.get()['Body'].read()
print(body)

s3.Object(bucket_name, file1).delete()

bucket = s3.Bucket(bucket_name)
