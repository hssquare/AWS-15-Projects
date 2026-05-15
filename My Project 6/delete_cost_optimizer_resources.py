import boto3

REGION = "ap-south-1"
FUNCTION_NAME = "automated-cost-optimizer"
RULE_NAME = "cost-optimizer-schedule"
ROLE_NAME = "lambda-cost-optimizer-role"
POLICY_NAME = "lambda-cost-optimizer-policy"

events = boto3.client("events", region_name=REGION)
lambda_client = boto3.client("lambda", region_name=REGION)
iam = boto3.client("iam", region_name=REGION)


def delete_eventbridge():
    try:
        events.remove_targets(Rule=RULE_NAME, Ids=["1"])
        print("EventBridge target removed")
    except Exception as e:
        print("Error removing target:", str(e))

    try:
        events.delete_rule(Name=RULE_NAME)
        print("EventBridge rule deleted")
    except Exception as e:
        print("Error deleting rule:", str(e))


def delete_lambda():
    try:
        lambda_client.delete_function(FunctionName=FUNCTION_NAME)
        print("Lambda function deleted")
    except Exception as e:
        print("Error deleting Lambda:", str(e))


def delete_iam_role():
    try:
        iam.delete_role_policy(
            RoleName=ROLE_NAME,
            PolicyName=POLICY_NAME
        )
        print("Inline role policy deleted")
    except Exception as e:
        print("Error deleting inline policy:", str(e))

    try:
        iam.delete_role(RoleName=ROLE_NAME)
        print("IAM role deleted")
    except Exception as e:
        print("Error deleting role:", str(e))


if __name__ == "__main__":
    delete_eventbridge()
    delete_lambda()
    delete_iam_role()