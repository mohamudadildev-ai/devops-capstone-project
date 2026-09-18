# Customer Accounts Microservice

[![CI Build](https://github.com/mohamudadildev-ai/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/mohamudadildev-ai/devops-capstone-project/actions/workflows/ci-build.yaml)

A RESTful microservice for managing Customer Accounts, built as the
capstone project for the DevOps course. It covers the full lifecycle of
a microservice: agile planning with user stories and a Kanban board,
a Flask REST API with full CRUD support, automated testing, continuous
integration with GitHub Actions, security headers/CORS, containerization
with Docker, and deployment to Kubernetes with a Tekton CD pipeline.

## Contents

- [service/](service) - the Flask application (models, routes, security config)
- [tests/](tests) - unit tests for the models and the REST API
- [setup.cfg](setup.cfg) - nosetests, coverage, flake8 and pylint configuration
- [Dockerfile](Dockerfile) - container image definition
- [k8s/](k8s) - Kubernetes Deployment and Service manifests
- [tekton/](tekton) - Tekton Tasks, Pipeline and PipelineRun for CD
- [.github/workflows/ci-build.yaml](.github/workflows/ci-build.yaml) - CI: lint then test on every push/PR
- [docs/user-story.md](docs/user-story.md) - user story template used for planning

## API

| Endpoint                 | Method | Description               |
|---------------------------|--------|----------------------------|
| `/`                       | GET    | Service metadata          |
| `/health`                 | GET    | Health check               |
| `/accounts`               | POST   | Create an Account          |
| `/accounts`               | GET    | List all Accounts          |
| `/accounts/<id>`          | GET    | Read an Account             |
| `/accounts/<id>`          | PUT    | Update an Account           |
| `/accounts/<id>`          | DELETE | Delete an Account           |

## Running locally

```bash
pip install -r requirements.txt
flask run
```

## Running the tests

```bash
nosetests
flake8 service tests
pylint service tests
```

## Building and running with Docker

```bash
docker build -t accounts:1.0 .
docker run --rm -p 8080:8080 accounts:1.0
```

## Deploying to Kubernetes

```bash
kubectl apply -k k8s/
kubectl get deployments,pods,rs,svc
```
