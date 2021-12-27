# Terraform destroy git branch builds
Utility script to destroy branch builds of infrastructure. The following assumptions are made:
* AWS S3 backend is used
* Each branch has its own Terraform deployment, separated by using a different backend key
* Once a CI/CD pipeline has merged a branch, the branch is deleted and the infrastructure ready to be destroyed
* tfenv is used to manage multiple versions of terraform and a `.terraform-version` file is used to pin the version of terraform

## Usage
### Docker
Assuming the current directory is at the root of the repository to process:
```shell
docker run --rm \
  -e AWS_PROFILE="role-dev" \
  -e TF_BACKEND_S3_BUCKET="my-terraform-dev" \
  -e TF_WORKSPACE_PATH="terraform/environments/dev" \
  -e TF_KEY_EXCLUSIONS="website-main" \
  -e TF_KEY_PREFIX="website-" \
  -v $(pwd):/app \
  -v $HOME/.aws:/home/app/.aws \
  -w /app \
  voquis/terraform-destroy-git-branch-builds:latest
```
