# Carnival Compliance Service

carnival compilance service that checks if an optimization result follows the fuel allowances for the route

```bash
git clone https://github.com/AbdelrahmanAbounida/carnival-task
cd carnival-task
```

# Basic Setup

Note: the following venv creation is for unix os (mac/linux)

## 0. Quick start

```
make run
```

## 1. PDM Build

<br />

**installation**

```
pip install pdm
python -m venv venv
source venv/bin/activate
pdm install
```

<br />

**linting and formatting**

```
pdm run pre-commit
```

<br />

**testing**

```
pdm run pytest
```

## 2. Docker

```
docker build -t carnival .
docker run -it -p 7000:7000 carnival
```

# TODO

- [x] Basic Project Setup
- [x] PDM init
- [x] precommit
- [x] linting >> black, ruff, isort
- [x] sample route
- [x] Dockerizing app
- [x] logging
- [x] init TDD
- [x] pytest
- [x] CICD
- [x] Basic Functionality
- [x] Update Task
- [x] auto build and deploy on each pull / push to main
- [ ] setup in README
- [ ] authenticate routes
- [ ] Makefile

- [ ] k6 ,load testing
- [ ] see how to scale the app vertically , horizontally, auto scaling
- [ ] k8s
- [ ] aws deploy (ECS, ELB, cloudfront, Fragate)
- [ ] nginx configuration
- [ ] promotheus , grafana
- [ ] caching
- [ ] profiling
- [ ] Terraform Provisioning
- [ ] Ansible Configuration
- [ ] ratelimit
- [ ] bumping api on push to main
- [ ] pytest cov
