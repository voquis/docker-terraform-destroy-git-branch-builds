#!/bin/bash

set -euo pipefail

# Log in to ECR registry
aws ecr-public get-login-password \
  --region us-east-1 \
| docker login \
  --username AWS \
  --password-stdin public.ecr.aws/voquis

# Build image with multiple tags
docker build \
  -t public.ecr.aws/voquis/terraform-destroy-git-branch-builds:${GITHUB_REF_NAME} \
  -t public.ecr.aws/voquis/terraform-destroy-git-branch-builds:latest

# Push images
docker push public.ecr.aws/voquis/terraform-destroy-git-branch-builds:${GITHUB_REF_NAME}
docker push public.ecr.aws/voquis/terraform-destroy-git-branch-builds:latest
