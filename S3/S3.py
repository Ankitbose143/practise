import json
import boto3

BUCKET_NAME='bhabani1-cloudtrail-s3-demo-bucket'

def s3_client():
    s3=boto3.client('s3')
    return s3

def create_bucket(bucket_name):
    print(bucket_name)
    return s3_client().create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint':'ap-south-1'
        }
    )

def create_bucket_policy():
    bucket_policy= {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AddPerm",
                "Effect": "Allow",
                "Principal": "*",
                "Action": ["s3:*"],
                "Resource": ["arn:aws:s3:::bhabani1-cloudtrail-s3-demo-bucket/*"]
            }
        ]
    }
    policy_string = json.dumps(bucket_policy)
    return s3_client().put_bucket_policy(
        Bucket=BUCKET_NAME,
        Policy=policy_string
        # Policy='abcd'
    )

if __name__== '__main__':
    # print(create_bucket(BUCKET_NAME))
    print(create_bucket_policy())
