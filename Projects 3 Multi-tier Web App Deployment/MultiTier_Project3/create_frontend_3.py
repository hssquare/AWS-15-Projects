import boto3, base64

ec2 = boto3.client("ec2")

script = """#!/bin/bash
dnf install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<h1>Frontend Server</h1>" > /var/www/html/index.html
"""

ec2.run_instances(
    ImageId="ami-0e12ffc2dd465f6e4",
    InstanceType="t3.micro",
    MinCount=1,
    MaxCount=1,
    SecurityGroupIds=["sg-0a8b5e19a0e002589"],
    UserData=base64.b64encode(script.encode()).decode()
)

print("Frontend Created")