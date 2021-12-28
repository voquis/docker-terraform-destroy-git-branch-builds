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
  -e TF_RELATIVE_PATH="terraform/environments/dev" \
  -e TF_KEY_EXCLUSIONS="website-main,website-develop" \
  -e TF_KEY_INCLUSIONS="other-key-1,other-key-2" \
  -e TF_KEY_PREFIX="website-" \
  -v $(pwd):/app \
  -v $HOME/.aws:/home/app/.aws \
  -w /app \
  voquis/terraform-destroy-git-branch-builds:latest
```

## Development
### Docker
To run the script inside a development container, from the root of this repo run:
```shell
docker run --rm -it \
  -w /app \
  -v $(pwd):/app \
  -v $HOME/.aws:/root/.aws \
  -v $HOME/path/to/project:/project \
  python:3 \
  bash
```
where `$HOME/path/to/project` is the local path to the terraform project.


### Running
Install dependencies (app and test) with:
```shell
pip install \
  -r requirements.txt \
  -r requirements-test.txt
```

Install terraform version manager ([tfenv](https://github.com/tfutils/tfenv)):
```shell
git clone https://github.com/tfutils/tfenv.git ~/.tfenv
echo 'export PATH="$HOME/.tfenv/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

Run the script with:
```shell
AWS_PROFILE="role-dev" \
TF_BACKEND_S3_BUCKET="my-terraform-dev" \
TF_ABSOLUTE_PATH="/project/path/to/terraform/files" \
TF_KEY_EXCLUSIONS="website-main" \
TF_KEY_PREFIX="website-" \
python destroy_git_branch_builds.py
```

### Testing
Run pylint with:
```shell
pylint destroy_git_branch_builds.py
```
