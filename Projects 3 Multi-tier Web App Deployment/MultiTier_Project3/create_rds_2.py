import boto3

rds = boto3.client("rds")

rds.create_db_instance(
    DBInstanceIdentifier="multitierdb",
    AllocatedStorage=20,
    DBName="appdb",
    Engine="mysql",
    MasterUsername="admin",
    MasterUserPassword="Password123!",
    DBInstanceClass="db.t3.micro",
    PubliclyAccessible=True
)

print("RDS Creation Started")