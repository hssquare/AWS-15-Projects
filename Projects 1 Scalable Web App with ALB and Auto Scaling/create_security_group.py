import boto3

ec2 = boto3.client('ec2')

vpcs = ec2.describe_vpcs()
vpc_id = vpcs['Vpcs'][0]['VpcId']

response = ec2.create_security_group(
    GroupName='WebAppSG',
    Description='Web Security Group',
    VpcId=vpc_id
)

sg_id = response['GroupId']

ec2.authorize_security_group_ingress(
    GroupId=sg_id,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
)

print("Security Group ID:", sg_id)