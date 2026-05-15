import boto3

ec2 = boto3.client("ec2")
vpc = ec2.describe_vpcs()["Vpcs"][0]["VpcId"]

# Frontend SG
front = ec2.create_security_group(
    GroupName="FrontendSG",
    Description="Frontend",
    VpcId=vpc
)["GroupId"]

# Backend SG
back = ec2.create_security_group(
    GroupName="BackendSG",
    Description="Backend",
    VpcId=vpc
)["GroupId"]

# DB SG
db = ec2.create_security_group(
    GroupName="DBSG",
    Description="Database",
    VpcId=vpc
)["GroupId"]

# Allow HTTP frontend
ec2.authorize_security_group_ingress(
    GroupId=front,
    IpPermissions=[{
        "IpProtocol":"tcp",
        "FromPort":80,
        "ToPort":80,
        "IpRanges":[{"CidrIp":"0.0.0.0/0"}]
    }]
)

# Allow backend from frontend
ec2.authorize_security_group_ingress(
    GroupId=back,
    IpPermissions=[{
        "IpProtocol":"tcp",
        "FromPort":5000,
        "ToPort":5000,
        "UserIdGroupPairs":[{"GroupId":front}]
    }]
)

# Allow MySQL from backend
ec2.authorize_security_group_ingress(
    GroupId=db,
    IpPermissions=[{
        "IpProtocol":"tcp",
        "FromPort":3306,
        "ToPort":3306,
        "UserIdGroupPairs":[{"GroupId":back}]
    }]
)

print("FrontendSG:", front)
print("BackendSG :", back)
print("DBSG      :", db)