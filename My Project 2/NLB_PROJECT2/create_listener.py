import boto3

elb = boto3.client('elbv2')

elb.create_listener(
    LoadBalancerArn='arn:aws:elasticloadbalancing:ap-south-1:892353389386:loadbalancer/net/MyNLB/89ca8ea069dcec4e',
    Protocol='TCP',
    Port=80,
    DefaultActions=[
        {
            'Type': 'forward',
            'TargetGroupArn': 'arn:aws:elasticloadbalancing:ap-south-1:892353389386:targetgroup/NLBTargetGroup/bf9c4137ed52e850'
        }
    ]
)

print("Listener Created")