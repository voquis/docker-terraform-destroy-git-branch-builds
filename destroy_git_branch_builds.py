"""
Script to destroy terraform infrastructure for non-existent git branches.
It is assumed a copy of infrastructure exists for each branch.
Once a branch is merged and the branch is deleted, this script should be run
to clean up the infrastructure for the deleted branch.
It is assumed Terraform and git are already installed.
"""

import os
import subprocess
from itertools import chain
import boto3
from git import Repo

def get_keys_to_destroy(bucket_name, prefix='', key_exclusions=None):
    """
    Function to get the list of keys from a bucket containing
    multiple terraform state file keys.
    """

    # Fetch state file keys from backend S3 bucket
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    # Use list comprehension to collapse list of dicts into a list
    bucket_keys = [content['Key'] for content in response['Contents']]

    print('Retrieved the following keys from bucket:')
    print(bucket_keys)

    # Iterate through matching bucket keys and drop any explicit exclusions
    for bucket_key in bucket_keys:
        if bucket_key.startswith(prefix) and bucket_key not in key_exclusions:
            yield bucket_key
        else:
            print(f'Skipping bucket key {bucket_key}')


def get_git_branches():
    """
    Get the list of branches from the current repo.
    """

    # Initialise repo using default or supplied path
    path_to_repo = os.environ.get('REPO_PATH', '.')
    repo = Repo(path_to_repo)

    # Get the list of active branches from repo
    for repo_branch in repo.branches:
        yield repo_branch.name


def tf_destroy(bucket_name, bucket_key):
    """
    Execute Terraform destroy command on a specific state file key name
    """
    print(f'Destroying {bucket_key}')

    # Get AWS profile for terraform
    aws_profile = os.environ.get('AWS_PROFILE', 'default')

    # Change to specified path containing terraform workspace files
    current_dir = os.getcwd()
    new_dir = os.path.join(current_dir, os.environ.get('TF_WORKSPACE_PATH', ''))
    os.chdir(new_dir)

    # Initialise backend
    subprocess.run(
        [
            'terraform',
            'init',
            '-reconfigure',
            f"-backend-config=profile={aws_profile}",
            f"-backend-config=key={bucket_key}"
        ],
        check=True
    )

    # Destroy infrastructure and change back to original directory
    subprocess.run(["terraform", "apply", "-destroy", "-auto-approve"], check=True)
    os.chdir(current_dir)

    s3_client = boto3.client('s3')
    s3_client.delete_object(Bucket=bucket_name, Key=bucket_key)


# Fetch environment variables
BUCKET = os.environ.get('TF_BACKEND_S3_BUCKET', None)
KEY_PREFIX = os.environ.get('TF_KEY_PREFIX', '')
KEY_EXCLUSIONS = os.environ.get('TF_KEY_EXCLUSIONS', '').split(',')

# Check provided environment variable values
if not BUCKET:
    raise ValueError('TF_BACKEND_S3_BUCKET not set.')

print(f'Using backend bucket {BUCKET}')
print(f'Using key prefix {KEY_PREFIX}')
print(f'Using key exclusions {KEY_EXCLUSIONS}')

print('Skipping the following active branches:')
BRANCHES = get_git_branches()
for branch in BRANCHES:
    print(branch)

# Use itertools' chain to combine list and generator
EXCLUSIONS = chain(BRANCHES, KEY_EXCLUSIONS)

print('Destroying the following branches:')
KEYS = get_keys_to_destroy(BUCKET, KEY_PREFIX, EXCLUSIONS)

for key in KEYS:
    tf_destroy(BUCKET, key)
