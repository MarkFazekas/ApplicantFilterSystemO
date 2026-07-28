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