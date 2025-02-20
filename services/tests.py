import boto3

session = boto3.session.Session()
s3 = session.client(
    service_name="s3",
    region_name="nyc3",
    endpoint_url="https://nyc3.digitaloceanspaces.com",
    aws_access_key_id="DO002RGDJ947DJHJ9WDT",
    aws_secret_access_key="e5+/pko6Ojar51Hb8ojUKfq2HtXy+tnGKOfs3rIcEfo",
)

# Try to list files
response = s3.list_objects_v2(Bucket="smtech-space")
print(response)


# AWS_S3_ENDPOINT_URL="https://nyc3.digitaloceanspaces.com"
# AWS_ACCESS_KEY_ID="DO002RGDJ947DJHJ9WDT"
# AWS_SECRET_ACCESS_KEY="e5+/pko6Ojar51Hb8ojUKfq2HtXy+tnGKOfs3rIcEfo"
# AWS_STORAGE_BUCKET_NAME="smtech-space"


with open("test.txt", "w") as f:
    f.write("Hello Spaces!")

s3.upload_file("test.txt", "smtech-space", "test.txt")
print(f"File uploaded: https://smtech-space.nyc3.cdn.digitaloceanspaces.com/test.txt")
