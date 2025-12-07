import boto3

s3_resource = boto3.client('s3', region_name='us-east-1')
bucket_name = "employee-offer-letters"

path_list = ["Ashish Mishra/Offer Letter/offer-letter.txt", "Smriti Dubey/Offer Letter/offer-letter.txt"]



def read_offer_letter(bucket_name, path):
    obj = s3_resource.get_object(Bucket=bucket_name,Key=path)
    content = obj["Body"].read().decode("utf-8")
    return content

for offerletter in path_list:

    offer_letter_content = read_offer_letter(bucket_name, offerletter)
    print(offer_letter_content)

    


    