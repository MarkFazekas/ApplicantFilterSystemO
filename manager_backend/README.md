[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)


```shell
python -m ruff check --select I,TC --fix
python -m ruff format
python -m ruff check .
python -m flake8 .
python -m mypy .
```

# Chalice

Setup:
```shell
chalice new-project manager_backend
mv manager_backend/* ./*
ln -s requirements/base.txt requirements.txt
```

Dev Deployment:
```shell
chalice deploy --profile afsd1 --stage dev
```

Prod Deployment:
```shell
chalice deploy --profile afsd1 --stage prod
```