import boto3
import base64

ec2 = boto3.client('ec2')

user_data = """#!/bin/bash
dnf update -y
dnf install -y httpd
systemctl enable httpd
systemctl start httpd
echo "Hello from Auto Scaling Server" > /var/www/html/index.html
"""

encoded = base64.b64encode(user_data.encode()).decode()

response = ec2.create_launch_template(
    LaunchTemplateName='WebAppTemplate45',
    LaunchTemplateData={
        'ImageId': 'ami-0e12ffc2dd465f6e4',
        'InstanceType': 't3.micro',
        'KeyName': 'WebAppKey',
        'SecurityGroupIds': ['sg-0c1ccca643cdff1a6'],
        'UserData': encoded
    }
)

print("Created")