import boto3

ec2 = boto3.client("ec2", region_name="ap-south-1")

INSTANCE_ID = "i-0c60a571fbf881dac"   # replace with your real instance id

response = ec2.stop_instances(
    InstanceIds=[INSTANCE_ID]
)

print("Stopping instance...")
print(response)