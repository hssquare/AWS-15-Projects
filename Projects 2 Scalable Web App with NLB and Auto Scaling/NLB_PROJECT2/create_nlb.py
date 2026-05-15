import boto3

elb = boto3.client('elbv2')
ec2 = boto3.client('ec2')

subnets = ec2.describe_subnets()['Subnets']

subnet_ids = [
    subnets[0]['SubnetId'],
    subnets[1]['SubnetId']
]

response = elb.create_load_balancer(
    Name='MyNLB',
    Subnets=subnet_ids,
    Type='network',
    Scheme='internet-facing'
)

print(response['LoadBalancers'][0]['LoadBalancerArn'])
print(response['LoadBalancers'][0]['DNSName'])