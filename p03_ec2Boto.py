import boto3

ec2_resource = boto3.resource('ec2', region_name='us-east-1')

instance_name = 'boto3Instance'

instance_id = None

#launch ec2, if it does not exists

new_instance = ec2_resource.create_instances (
    
    ImageId="ami-0fa3fe0fa7920f68e",
    InstanceType='t3.micro',
    MinCount=1,
    MaxCount=1,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': instance_name
                },
            ]
        },
    ]
)