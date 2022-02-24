import boto3
from AWS_Credential import *
import json

AWS_REGION = "ap-south-1"
ec2 = boto3.resource("ec2",aws_access_key_id='AKIAUK7CTVLM57TQVWBW',aws_secret_access_key='Z8biMAKzMgZuNpZyCL7Dr77u2t/QzCkBN',region_name=AWS_REGION)

client = boto3.client('sns')

response = client.create_topic(Name='bhabani_sns_demo2')
print(response)

respons = client.subscribe( TopicArn='arn:aws:sns:ap-south-1:336837530167:bhabani_sns_demo2',Protocol='email',
                            Endpoint='swainbhabanishankar9937@gmail.com',ReturnSubscriptionArn=True)
print(respons)



# message = {"bhanani": "sidhu"}
# client = boto3.client('sns')
response = client.publish(
    TargetArn='arn:aws:sns:ap-south-1:336837530167:bhabani_sns_demo2',
    Message=json.dumps({'default':"BHABANI_SIDHU SNS_DEMO" }),
    MessageStructure='json')
print(response)