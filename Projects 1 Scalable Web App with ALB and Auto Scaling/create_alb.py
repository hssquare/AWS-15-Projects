import boto3

elbv2 = boto3.client('elbv2')
ec2 = boto3.client('ec2')

subnets = ec2.describe_subnets()['Subnets']
subnet_ids = [subnets[0]['SubnetId'], subnets[1]['SubnetId']]

response = elbv2.create_load_balancer(
    Name='WebALB',
    Subnets=subnet_ids,
    SecurityGroups=['sg-0c1ccca643cdff1a6'],
    Scheme='internet-facing',
    Type='application'
)

print(response['LoadBalancers'][0]['LoadBalancerArn'])