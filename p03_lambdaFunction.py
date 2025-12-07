import json
from datetime import datetime

def return_time():
  now = datetime.now()
  formatted = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
  return formatted

def lambda_handler(event, context):
    # hello demo by smriti
    time = return_time()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda demo with ashish' + {time})
    }