import boto3
from datetime import datetime, timedelta, timezone

# Change region if needed
REGION = "ap-south-1"

ec2 = boto3.client("ec2", region_name=REGION)
cloudwatch = boto3.client("cloudwatch", region_name=REGION)

CPU_THRESHOLD = 5.0          # Stop if average CPU is below this
LOOKBACK_MINUTES = 30        # Check CPU for last 30 minutes
PERIOD = 300                 # 5 minutes


def get_average_cpu(instance_id):
    """
    Get average CPU utilization for an EC2 instance.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=LOOKBACK_MINUTES)

    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": instance_id
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=PERIOD,
        Statistics=["Average"]
    )

    datapoints = response.get("Datapoints", [])

    if not datapoints:
        return None

    avg_cpu = sum(point["Average"] for point in datapoints) / len(datapoints)
    return avg_cpu


def get_running_instances():
    """
    Get only running EC2 instances with AutoStop=true tag.
    """
    response = ec2.describe_instances(
        Filters=[
            {"Name": "instance-state-name", "Values": ["running"]}
        ]
    )

    instance_ids = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]

            tags = {tag["Key"]: tag["Value"] for tag in instance.get("Tags", [])}

            # Safety: stop only instances tagged with AutoStop=true
            if tags.get("AutoStop", "false").lower() == "true":
                instance_ids.append(instance_id)

    return instance_ids


def stop_instance(instance_id):
    """
    Stop EC2 instance.
    """
    response = ec2.stop_instances(InstanceIds=[instance_id])
    return response


def lambda_handler(event, context):
    print("Starting Automated Cost Optimizer...")

    running_instances = get_running_instances()

    if not running_instances:
        print("No running instances found with AutoStop=true")
        return {
            "statusCode": 200,
            "body": "No matching running instances found."
        }

    stopped_instances = []
    skipped_instances = []

    for instance_id in running_instances:
        avg_cpu = get_average_cpu(instance_id)

        if avg_cpu is None:
            print(f"{instance_id}: No CPU data found. Skipping.")
            skipped_instances.append({
                "instance_id": instance_id,
                "reason": "No CPU data"
            })
            continue

        print(f"{instance_id}: Average CPU = {avg_cpu:.2f}%")

        if avg_cpu < CPU_THRESHOLD:
            stop_instance(instance_id)
            print(f"{instance_id}: Stopped because CPU < {CPU_THRESHOLD}%")
            stopped_instances.append({
                "instance_id": instance_id,
                "avg_cpu": round(avg_cpu, 2)
            })
        else:
            print(f"{instance_id}: Kept running")
            skipped_instances.append({
                "instance_id": instance_id,
                "avg_cpu": round(avg_cpu, 2),
                "reason": "CPU above threshold"
            })

    return {
        "statusCode": 200,
        "body": {
            "stopped_instances": stopped_instances,
            "skipped_instances": skipped_instances
        }
    }