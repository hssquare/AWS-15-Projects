import boto3

elb = boto3.client("elbv2")
ec2 = boto3.client("ec2")

subs = ec2.describe_subnets()["Subnets"]

ids = [subs[0]["SubnetId"], subs[1]["SubnetId"]]

res = elb.create_load_balancer(
    Name="MultiTierALB",
    Subnets=ids,
    Scheme="internet-facing",
    Type="application"
)

print(res["LoadBalancers"][0]["LoadBalancerArn"])
print(res["LoadBalancers"][0]["DNSName"])