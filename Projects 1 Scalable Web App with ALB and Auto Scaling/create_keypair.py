import boto3

ec2 = boto3.client('ec2')

response = ec2.create_key_pair(KeyName='WebAppKey')

with open("WebAppKey.pem", "w") as file:
    file.write(response['KeyMaterial'])

print("Key Pair Created")