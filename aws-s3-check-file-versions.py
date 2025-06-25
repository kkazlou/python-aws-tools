import boto3

file_list = ['009702f0-6b58-4751-b2ca-6fd36a7301b9.txt',
            '008370ea-1d30-41d3-98ee-c56eabd8157c.txt',
            '002d473b-ccf3-4539-854c-bb6995d27d08.txt',
            '0000c869-abd2-47e8-aebb-c3467e3c6779.txt']

# Create a client for the S3 service
s3 = boto3.client('s3')

# Set the bucket name
bucket_name = 'cyberark-sr-sre-candidate-bucket'

# Check the versions of the files
for file_name in file_list:
    print()
    print("Checking file: ", file_name)
    
    try:
        response = s3.list_object_versions(Bucket=bucket_name, Prefix=file_name)
        
        if 'Versions' in response and len(response['Versions']) > 1:
            # Get the latest version (first in the list)
            latest_version = response['Versions'][0]
            # Get the previous version (second in the list)
            previous_version = response['Versions'][1]
            
            print("Latest version ID: ", latest_version['VersionId'])
            print("Previous version ID: ", previous_version['VersionId'])
            print("Latest version ETag: ", latest_version['ETag'])
            print("Previous version ETag: ", previous_version['ETag'])
            
            # Compare ETags to check if content is different
            if latest_version['ETag'] != previous_version['ETag']:
                print("Content is DIFFERENT between latest and previous versions")
            else:
                print("Content is IDENTICAL between latest and previous versions")
                # delete the previous version
                # s3.delete_object(Bucket=bucket_name, Key=file_name, VersionId=previous_version['VersionId'])
                # print("Previous version deleted")

        elif 'Versions' in response and len(response['Versions']) == 1:
            print("Only one version exists: ", response['Versions'][0]['VersionId'])
            print("Cannot compare with previous version")
            
        else:
            print("No versions found for this file")
            
    except Exception as e:
        print("Error checking versions: ", e)
