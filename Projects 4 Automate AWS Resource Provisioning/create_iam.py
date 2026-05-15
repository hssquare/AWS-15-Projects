import boto3
import json

iam = boto3.client('iam')

assume_role_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "ec2.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }
    ]
}

response = iam.create_role(
    RoleName='MyEC2Role',
    AssumeRolePolicyDocument=json.dumps(assume_role_policy)
)

iam.attach_role_policy(
    RoleName='MyEC2Role',
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess'
)

print("IAM Role Created")