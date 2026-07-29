[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)
[![gitlint](https://img.shields.io/badge/commit_lint-gitlint-blue)](https://github.com/jorisroovers/gitlint)

## Pyenv

How to install: https://github.com/pyenv/pyenv/wiki#suggested-build-environment

cd ~/.pyenv/plugins/python-build/../.. && git pull && cd -
pyenv install --list

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

## AWS Setup

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
export PATH="$JAVA_HOME/bin:$PATH"
```

```shell
wget -O dynamodb_local/dynamodb.tar.gz  https://d1ni2b6xgvw0s0.cloudfront.net/v2.x/dynamodb_local_2026-01-18.tar.gz
tar -C dynamodb_local -xzvf dynamodb_local/dynamodb.tar.gz
java -Djava.library.path=dynamodb_local/DynamoDBLocal_lib -jar dynamodb_local/DynamoDBLocal.jar -dbPath dynamodb_local/databases -optimizeDbBeforeStartup -delayTransientStatuses -disableTelemetry -port 8000
```

Update the tar file from: https://s3-us-west-2.amazonaws.com/dynamodb-local

```shell
aws configure --profile afsd1_dev
```

AWS Access Key ID: DEVELOPERDATABASE  
AWS Secret Access Key: FAKEKEY 
Default region name: eu-demo-1  

Test DynamoDB
```shell
aws dynamodb list-tables --endpoint-url http://localhost:8000 --profile afsd1_dev
```
