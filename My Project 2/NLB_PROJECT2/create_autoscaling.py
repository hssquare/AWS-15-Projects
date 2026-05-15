import boto3

asg = boto3.client('autoscaling')
ec2 = boto3.client('ec2')

subnets = ec2.describe_subnets()['Subnets']

ids = ",".join([
    subnets[0]['SubnetId'],
    subnets[1]['SubnetId']
])

asg.create_auto_scaling_group(
    AutoScalingGroupName='NLBASG',
    LaunchTemplate={
        'LaunchTemplateName': 'NLBTemplate2',
        'Version': '$Latest'
    },
    MinSize=2,
    MaxSize=5,
    DesiredCapacity=2,
    VPCZoneIdentifier=ids,
    TargetGroupARNs=['arn:aws:elasticloadbalancing:ap-south-1:892353389386:targetgroup/NLBTargetGroup/bf9c4137ed52e850']
)

print("Auto Scaling Group Created")