import boto3

size_criteria1 = 5000 # 5KB
size_criteria2 = 15000 # 15KB
files_count = 0
unassigned_files_list = []
assigned_files_list = []
other_files_list = []
size_criteria1_files_list = []
size_criteria2_files_list = []

# Create a client for the S3 service
s3 = boto3.client('s3')

# Set the bucket name
bucket_name = 'cyberark-sr-sre-candidate-bucket'

# by default 'list_objects_v2' returns 1000 objects, so we need to paginate
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket_name)

for page in pages:
    for obj in page['Contents']:
        print(obj['Key'])
        files_count += 1

        # categorize files by name
        if obj['Key'].startswith('unassigned_') and obj['Key'].endswith('.txt'):
            unassigned_files_list.append(obj['Key'])
        elif obj['Key'].startswith('assigned_') and obj['Key'].endswith('.txt'):
            assigned_files_list.append(obj['Key'])
        elif obj['Key'].endswith('.txt'):
            other_files_list.append(obj['Key'])
        else:
            pass

        # categorize files by size
        if obj['Size'] > size_criteria1:
            size_criteria1_files_list.append(obj['Key'])

        if obj['Size'] > size_criteria2:
            size_criteria2_files_list.append(obj['Key'])

print("total files in the bucket", files_count)
print("unassigned files", len(unassigned_files_list))
print("assigned files", len(assigned_files_list))
print("other files", len(other_files_list))
print("files over 5KB", len(size_criteria1_files_list))
print("files over 15KB", len(size_criteria2_files_list))
