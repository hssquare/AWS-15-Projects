import boto3

elb = boto3.client('elbv2')
ec2 = boto3.client('ec2')

vpc = ec2.describe_vpcs()['Vpcs'][0]['VpcId']

response = elb.create_target_group(
    Name='NLBTargetGroup',
    Protocol='TCP',
    Port=80,
    VpcId=vpc,
    TargetType='instance'
)

print(response['TargetGroups'][0]['TargetGroupArn'])