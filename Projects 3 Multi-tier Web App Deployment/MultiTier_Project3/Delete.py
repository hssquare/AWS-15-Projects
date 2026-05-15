import boto3
import time

region = "ap-south-1"

ec2 = boto3.client("ec2", region_name=region)
elb = boto3.client("elbv2", region_name=region)
rds = boto3.client("rds", region_name=region)

# -----------------------------------
# Names used in your project
# -----------------------------------
LOAD_BALANCER = "MultiTierALB"
DB_INSTANCE = "multitierdb"

SECURITY_GROUPS = [
    "FrontendSG",
    "BackendSG",
    "DBSG"
]

print("Starting Multi-tier cleanup...")

# -----------------------------------
# 1. Delete Load Balancer
# -----------------------------------
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

print("Waiting 30 seconds...")
time.sleep(30)

# -----------------------------------
# 2. Delete RDS Database
# -----------------------------------
try:
    rds.delete_db_instance(
        DBInstanceIdentifier=DB_INSTANCE,
        SkipFinalSnapshot=True,
        DeleteAutomatedBackups=True
    )
    print("RDS deletion started")
except:
    print("RDS not found")

# -----------------------------------
# 3. Terminate All EC2 Instances
# -----------------------------------
try:
    reservations = ec2.describe_instances()["Reservations"]

    ids = []

    for r in reservations:
        for i in r["Instances"]:
            state = i["State"]["Name"]
            if state != "terminated":
                ids.append(i["InstanceId"])

    if ids:
        ec2.terminate_instances(InstanceIds=ids)
        print("Instances terminated:", ids)
    else:
        print("No EC2 instances found")

except:
    print("Error deleting EC2")

print("Waiting 20 seconds...")
time.sleep(20)

# -----------------------------------
# 4. Delete Security Groups
# -----------------------------------
try:
    groups = ec2.describe_security_groups()["SecurityGroups"]

    for sg in groups:
        if sg["GroupName"] in SECURITY_GROUPS:
            try:
                ec2.delete_security_group(
                    GroupId=sg["GroupId"]
                )
                print("Deleted SG:", sg["GroupName"])
            except:
                print("Could not delete:", sg["GroupName"])

except:
    print("Security groups not found")

print("Cleanup Completed")