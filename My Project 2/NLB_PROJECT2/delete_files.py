import boto3
import time

region = "ap-south-1"

ec2 = boto3.client("ec2", region_name=region)
elb = boto3.client("elbv2", region_name=region)
asg = boto3.client("autoscaling", region_name=region)

# -----------------------------
# Names used in your project
# -----------------------------
AUTO_SCALING_GROUP = "NLBASG"
LOAD_BALANCER = "MyNLB"
TARGET_GROUP = "NLBTargetGroup"
LAUNCH_TEMPLATE = "NLBTemplate2"
KEY_PAIR = "NLBKey"
SECURITY_GROUP_NAME = "NLBSG"

print("Starting cleanup...")

# -----------------------------
# 1. Delete Auto Scaling Group
# -----------------------------
try:
    asg.update_auto_scaling_group(
        AutoScalingGroupName=AUTO_SCALING_GROUP,
        MinSize=0,
        MaxSize=0,
        DesiredCapacity=0
    )

    asg.delete_auto_scaling_group(
        AutoScalingGroupName=AUTO_SCALING_GROUP,
        ForceDelete=True
    )

    print("Auto Scaling Group deleted")
except:
    print("Auto Scaling Group not found / already deleted")

time.sleep(10)

# -----------------------------
# 2. Terminate EC2 Instances
# -----------------------------
try:
    instances = ec2.describe_instances()

    ids = []
    for r in instances["Reservations"]:
        for i in r["Instances"]:
            if i["State"]["Name"] != "terminated":
                ids.append(i["InstanceId"])

    if ids:
        ec2.terminate_instances(InstanceIds=ids)
        print("Instances terminated:", ids)
    else:
        print("No running instances")
except:
    print("No instances found")

time.sleep(10)

# -----------------------------
# 3. Delete Load Balancer
# -----------------------------
try:
    lbs = elb.describe_load_balancers()["LoadBalancers"]

    for lb in lbs:
        if lb["LoadBalancerName"] == LOAD_BALANCER:
            elb.delete_load_balancer(
                LoadBalancerArn=lb["LoadBalancerArn"]
            )
            print("Load Balancer deleted")
except:
    print("Load Balancer not found")

time.sleep(10)

# -----------------------------
# 4. Delete Target Group
# -----------------------------
try:
    tgs = elb.describe_target_groups()["TargetGroups"]

    for tg in tgs:
        if tg["TargetGroupName"] == TARGET_GROUP:
            elb.delete_target_group(
                TargetGroupArn=tg["TargetGroupArn"]
            )
            print("Target Group deleted")
except:
    print("Target Group not found")

# -----------------------------
# 5. Delete Launch Template
# -----------------------------
try:
    ec2.delete_launch_template(
        LaunchTemplateName=LAUNCH_TEMPLATE
    )
    print("Launch Template deleted")
except:
    print("Launch Template not found")

# -----------------------------
# 6. Delete Key Pair
# -----------------------------
try:
    ec2.delete_key_pair(KeyName=KEY_PAIR)
    print("Key Pair deleted")
except:
    print("Key Pair not found")

# -----------------------------
# 7. Delete Security Group
# -----------------------------
try:
    sgs = ec2.describe_security_groups()["SecurityGroups"]

    for sg in sgs:
        if sg["GroupName"] == SECURITY_GROUP_NAME:
            ec2.delete_security_group(
                GroupId=sg["GroupId"]
            )
            print("Security Group deleted")
except:
    print("Security Group not found")

print("Cleanup Completed Successfully")