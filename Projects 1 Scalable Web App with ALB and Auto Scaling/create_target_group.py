import boto3

elbv2 = boto3.client('elbv2')
ec2 = boto3.client('ec2')

vpc_id = ec2.describe_vpcs()['Vpcs'][0]['VpcId']

response = elbv2.create_target_group(
    Name='WebTargetGroup',
    Protocol='HTTP',
    Port=80,
    VpcId=vpc_id,
    TargetType='instance'
)

print(response['TargetGroups'][0]['TargetGroupArn'])