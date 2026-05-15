import boto3
import json

REGION = "ap-south-1"
ROLE_NAME = "lambda-cost-optimizer-role"
POLICY_NAME = "lambda-cost-optimizer-policy"

iam = boto3.client("iam", region_name=REGION)


def create_role():
    with open("trust_policy.json", "r") as f:
        trust_policy = json.load(f)

    try:
        response = iam.create_role(
            RoleName=ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description="Role for Automated Cost Optimizer Lambda"
        )
        print("Role created successfully")
        print("Role ARN:", response["Role"]["Arn"])
        return response["Role"]["Arn"]

    except iam.exceptions.EntityAlreadyExistsException:
        print("Role already exists")
        response = iam.get_role(RoleName=ROLE_NAME)
        print("Existing Role ARN:", response["Role"]["Arn"])
        return response["Role"]["Arn"]

    except Exception as e:
        print("Error creating role:", str(e))
        return None


def attach_inline_policy():
    with open("permission_policy.json", "r") as f:
        permission_policy = json.load(f)

    try:
        iam.put_role_policy(
            RoleName=ROLE_NAME,
            PolicyName=POLICY_NAME,
            PolicyDocument=json.dumps(permission_policy)
        )
        print("Inline policy attached successfully")

    except Exception as e:
        print("Error attaching policy:", str(e))


if __name__ == "__main__":
    role_arn = create_role()
    if role_arn:
        attach_inline_policy()