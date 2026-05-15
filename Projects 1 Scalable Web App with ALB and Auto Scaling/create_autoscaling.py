import boto3

asg = boto3.client('autoscaling')
ec2 = boto3.client('ec2')

subnets = ec2.describe_subnets()['Subnets']
subnet_ids = ",".join([subnets[0]['SubnetId'], subnets[1]['SubnetId']])

asg.create_auto_scaling_group(
    AutoScalingGroupName='WebASG',
    LaunchTemplate={
        'LaunchTemplateName': 'WebAppTemplate45'
    },
    MinSize=2,
    MaxSize=5,
    DesiredCapacity=2,
    VPCZoneIdentifier=subnet_ids,
    TargetGroupARNs=['arn:aws:elasticloadbalancing:ap-south-1:303670280198:targetgroup/WebTargetGroup/1e7e374ed8558a05']
)

print("Auto Scaling Group Created")