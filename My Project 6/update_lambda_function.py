import boto3
import zipfile

REGION = "ap-south-1"
FUNCTION_NAME = "automated-cost-optimizer"
ZIP_FILE_NAME = "lambda_function.zip"

lambda_client = boto3.client("lambda", region_name=REGION)


def zip_lambda_code():
    try:
        with zipfile.ZipFile(ZIP_FILE_NAME, "w", zipfile.ZIP_DEFLATED) as z:
            z.write("lambda_function.py")
        print("Lambda code zipped successfully")
        return ZIP_FILE_NAME
    except Exception as e:
        print("Error zipping Lambda code:", str(e))
        return None


def update_lambda(zip_file_name):
    try:
        with open(zip_file_name, "rb") as f:
            zipped_code = f.read()

        response = lambda_client.update_function_code(
            FunctionName=FUNCTION_NAME,
            ZipFile=zipped_code,
            Publish=True
        )

        print("Lambda updated successfully")
        print("Updated Lambda ARN:", response["FunctionArn"])

    except Exception as e:
        print("Error updating Lambda:", str(e))


if __name__ == "__main__":
    zip_file_name = zip_lambda_code()
    if zip_file_name:
        update_lambda(zip_file_name)