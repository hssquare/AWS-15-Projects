import boto3, base64

ec2 = boto3.client("ec2")

script = """#!/bin/bash
dnf install -y python3
echo "Backend Ready" > /home/ec2-user/app.txt
"""

ec2.run_instances(
    ImageId="ami-0e12ffc2dd465f6e4",
    InstanceType="t3.micro",
    MinCount=1,
    MaxCount=1,
    SecurityGroupIds=["sg-0e487b3c63fa3adbd"],
    UserData=base64.b64encode(script.encode()).decode()
)

print("Backend Created")