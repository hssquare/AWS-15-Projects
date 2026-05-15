import boto3

elbv2 = boto3.client('elbv2')

elbv2.create_listener(
    LoadBalancerArn='arn:aws:elasticloadbalancing:ap-south-1:303670280198:loadbalancer/app/WebALB/8ee0105bbc115d15',
    Protocol='HTTP',
    Port=80,
    DefaultActions=[
        {
            'Type': 'forward',
            'TargetGroupArn': 'arn:aws:elasticloadbalancing:ap-south-1:303670280198:targetgroup/WebTargetGroup/1e7e374ed8558a05'
        }
    ]
)

print("Listener Created")