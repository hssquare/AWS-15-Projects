import boto3

ec2 = boto3.resource('ec2')

instance = ec2.create_instances(
    ImageId='ami-0f5ee92e2d63afc18',
    MinCount=1,
    MaxCount=1,
    InstanceType='t3.micro',
    KeyName='server-1'
)

print("EC2 Instance Launched:", instance[0].id)