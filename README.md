[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)
[![gitlint](https://img.shields.io/badge/commit_lint-gitlint-blue)](https://github.com/jorisroovers/gitlint)

# Python env

## Pyenv

How to install:   
https://github.com/pyenv/pyenv/wiki#suggested-build-environment

```shell
curl https://pyenv.run | bash
```

How to update:  
```shell
cd ~/.pyenv/plugins/python-build/../.. && git pull && cd -
pyenv install --list
```

Install:

```shell
env PYTHON_CONFIGURE_OPTS='--enable-optimizations --with-lto' PYTHON_CFLAGS='-march=native -mtune=native' pyenv install 3.14.6
pyenv virtualenv 3.14.6 afs3146
pyenv local afs3146
```

## Setup commands

```shell
pip install uv
uv pip install -r manager_backend/requirements/dev.txt
```

# AWS Setup

1. Create root user with email address.  
2. Setup MFA for root user.  
3. Setup Account alias  
4. Create a new iam user.  
   - Create a new iam Group.  
   - Admin group with: AdministratorAccess Policy  
5. Login to new account.  
6. Select the current user in IAM  
7. Create access key  
   - Command Line Interface (CLI)  

```shell
aws configure --profile afsd1
```

Default region: eu-west-1

```shell
chmod 600 ~/.aws/credentials
```

```shell
aws sts get-caller-identity --profile afsd1
```

## Local DynamoDB Setup

```shell
sudo apt install default-jre
```

Put it in your `.profile`/`.bashrc`

```shell
export JAVA_HOME="/usr/lib/jvm/java-21-openjdk-amd64"
export JAVA_HOME="/usr/lib/jvm/java-25-openjdk-amd64"
export PATH="$JAVA_HOME/bin:$PATH"
```

```shell
wget -O dynamodb_local/dynamodb.tar.gz https://d1ni2b6xgvw0s0.cloudfront.net/v2.x/dynamodb_local_2026-01-18.tar.gz
tar -C dynamodb_local -xzvf dynamodb_local/dynamodb.tar.gz
java -Djava.library.path=dynamodb_local/DynamoDBLocal_lib -jar dynamodb_local/DynamoDBLocal.jar -dbPath dynamodb_local/databases -optimizeDbBeforeStartup -delayTransientStatuses -disableTelemetry -port 8000
```

Update the tar file from: https://s3-us-west-2.amazonaws.com/dynamodb-local

```shell
nano ~/.aws/credentials
```

```ini
[afsd1_dev]
aws_access_key_id = DEVELOPERACCESSKEY
aws_secret_access_key = FAKEKEY
```

Then add these:

```shell
nano ~/.aws/config
```

```ini
[profile afsd1_dev]
region = eu-demo-1
services = local-services

[services local-services]
dynamodb =
  endpoint_url = http://localhost:8000
```

Test DynamoDB
```shell
aws dynamodb list-tables --profile afsd1_dev
```

### Create table

```shell
aws dynamodb create-table \
  --table-name ApplicantFilterSystemDev \
  --attribute-definitions \
    AttributeName=pk,AttributeType=S \
    AttributeName=sk,AttributeType=S \
  --key-schema \
    AttributeName=pk,KeyType=HASH \
    AttributeName=sk,KeyType=RANGE \
  --provisioned-throughput \
    ReadCapacityUnits=2,WriteCapacityUnits=2 \
  --profile afsd1_dev
```

## Real AWS DynamoDB

Create DynamoDB:

```shell
aws cloudformation deploy \
  --template-file dynamodb/cf_dev.json \
  --stack-name applicant-filter-system-dev \
  --profile afsd1 \
  --no-fail-on-empty-changeset
```
