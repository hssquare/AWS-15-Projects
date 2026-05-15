import boto3

REGION = "ap-south-1"
RULE_NAME = "cost-optimizer-schedule"
FUNCTION_NAME = "automated-cost-optimizer"

events = boto3.client("events", region_name=REGION)
lambda_client = boto3.client("lambda", region_name=REGION)
sts = boto3.client("sts", region_name=REGION)


def create_rule():
    try:
        response = events.put_rule(
            Name=RULE_NAME,
            ScheduleExpression="rate(15 minutes)",
            State="ENABLED",
            Description="Trigger automated cost optimizer Lambda every 15 minutes"
        )
        print("Rule created successfully")
        print("Rule ARN:", response["RuleArn"])
        return response["RuleArn"]
    except Exception as e:
        print("Error creating rule:", str(e))
        return None


def add_lambda_permission():
    try:
        account_id = sts.get_caller_identity()["Account"]
        source_arn = f"arn:aws:events:{REGION}:{account_id}:rule/{RULE_NAME}"

        lambda_client.add_permission(
            FunctionName=FUNCTION_NAME,
            StatementId="eventbridge-invoke-lambda",
            Action="lambda:InvokeFunction",
            Principal="events.amazonaws.com",
            SourceArn=source_arn
        )
        print("Permission added successfully")
    except lambda_client.exceptions.ResourceConflictException:
        print("Permission already exists")
    except Exception as e:
        print("Error adding Lambda permission:", str(e))


def add_target(rule_arn):
    try:
        function_arn = lambda_client.get_function(FunctionName=FUNCTION_NAME)["Configuration"]["FunctionArn"]

        response = events.put_targets(
            Rule=RULE_NAME,
            Targets=[
                {
                    "Id": "1",
                    "Arn": function_arn
                }
            ]
        )

        print("Target added successfully")
        print(response)
    except Exception as e:
        print("Error adding target:", str(e))


if __name__ == "__main__":
    rule_arn = create_rule()
    if rule_arn:
        add_lambda_permission()
        add_target(rule_arn)