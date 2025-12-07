import boto3
import json

def lambda_handler(event, context):
    s3_client = boto3.client('s3', region_name='us-east-1')
     
    bucket_name = "employee-offer-letters"
    path = "Ashish Mishra/Offer Letter/offer-letter.txt"

    def read_offer_letter(bucket_name, path):
        obj = s3_client.get_object(Bucket=bucket_name,Key=path)
        content = obj["Body"].read().decode("utf-8")
        return content
    
    offer_letter_content = read_offer_letter(bucket_name, path)
    print(offer_letter_content)
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Offer letter content read successfully!', 'salary': offer_letter_content})
    }