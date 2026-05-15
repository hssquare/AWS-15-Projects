import boto3
import zipfile
import time
import os

REGION = "ap-south-1"
FUNCTION_NAME = "automated-cost-optimizer"
ROLE_NAME = "lambda-cost-optimizer-role"
ZIP_FILE_NAME = "lambda_function.zip"

iam = boto3.client("iam", region_name=REGION)
lambda_client = boto3.client("lambda", region_name=REGION)


def get_role_arn():
    try:
        response = iam.get_role(RoleName=ROLE_NAME)
        return response["Role"]["Arn"]
    except Exception as e:
        print("Error getting role ARN:", str(e))
        return None


def zip_lambda_code():
    try:
        with zipfile.ZipFile(ZIP_FILE_NAME, "w", zipfile.ZIP_DEFLATED) as z:
            z.write("lambda_function.py")
        print("Lambda code zipped successfully")
        return ZIP_FILE_NAME
    except Exception as e:
        print("Error zipping Lambda code:", str(e))
        return None


def create_lambda(role_arn, zip_file_name):
    try:
        with open(zip_file_name, "rb") as f:
            zipped_code = f.read()

        response = lambda_client.create_function(
            FunctionName=FUNCTION_NAME,
            Runtime="python3.11",
            Role=role_arn,
            Handler="lambda_function.lambda_handler",
            Code={"ZipFile": zipped_code},
            Timeout=60,
            MemorySize=128,
            Publish=True,
            Description="Automated Cost Optimizer for EC2 idle instances"
        )

        print("Lambda created successfully")
        print("Lambda ARN:", response["FunctionArn"])

    except lambda_client.exceptions.ResourceConflictException:
        print("Lambda function already exists")

    except Exception as e:
        print("Error creating Lambda:", str(e))


if __name__ == "__main__":
    role_arn = get_role_arn()

    if not role_arn:
        print("Role ARN not found. Please create IAM role first.")
        exit()

    print("Waiting 10 seconds for IAM role propagation...")
    time.sleep(10)

    zip_file_name = zip_lambda_code()

    if zip_file_name:
        create_lambda(role_arn, zip_file_name)