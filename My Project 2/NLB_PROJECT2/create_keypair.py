import boto3

ec2 = boto3.client('ec2')

response = ec2.create_key_pair(KeyName='NLBKey')

with open("NLBKey1.pem", "w") as f:
    f.write(response['KeyMaterial'])

print("Key Pair Created")