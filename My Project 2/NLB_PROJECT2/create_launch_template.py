import boto3
import base64

ec2 = boto3.client('ec2')

userdata = """#!/bin/bash
dnf update -y
dnf install -y httpd
systemctl start httpd
systemctl enable httpd
echo "Hello from NLB Auto Scaling Server" > /var/www/html/index.html
"""

encoded = base64.b64encode(userdata.encode()).decode()

response = ec2.create_launch_template(
    LaunchTemplateName='NLBTemplate2',
    LaunchTemplateData={
        'ImageId': 'ami-0e12ffc2dd465f6e4',
        'InstanceType': 't3.micro',
        'KeyName': 'NLBKey',
        'SecurityGroupIds': ['sg-031c0ee0de6030350'],
        'UserData': encoded
    }
)

print("Launch Template Created")