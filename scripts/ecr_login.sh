#!/bin/bash

set -euo pipefail

# Log in to ECR registry
aws ecr-public get-login-password \
  --region us-east-1 \
| docker login \
  --username AWS \
  --password-stdin public.ecr.aws/voquis
