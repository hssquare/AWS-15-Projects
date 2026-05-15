import boto3

s3 = boto3.client('s3')

bucket_name = 'my-project-4-with-boto3'

s3.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'}
)

print("S3 Bucket Created:", bucket_name)