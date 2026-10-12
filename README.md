# My API — Multi-Backend Engineering Project

A backend engineering project integrating Python, FastAPI, Node.js, Express, PostgreSQL, automated testing, CI/CD, Docker, and Linux server deployment.

This project demonstrates the development and operation of independent backend services that share a PostgreSQL database, supported by automated quality checks and containerized infrastructure.

## Project Overview

My API is an ongoing backend software engineering project built as part of a structured learning roadmap.

The project brings together two backend applications:

- **Python:** FastAPI with SQLAlchemy and Alembic.
- **JavaScript:** Node.js with Express and the PostgreSQL `pg` client.

Both applications connect to a shared PostgreSQL database. The project also includes automated testing, code linting, GitHub Actions, Docker, Docker Compose, Nginx, and HTTPS deployment.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming languages | Python, JavaScript |
| Python backend | FastAPI, SQLAlchemy |
| JavaScript backend | Node.js, Express |
| Database | PostgreSQL |
| Database migrations | Alembic |
| Testing | pytest, Node.js tests |
| Code quality | Ruff, ESLint |
| Version control | Git, GitHub |
| CI/CD | GitHub Actions |
| Containerization | Docker, Docker Compose |
| Reverse proxy | Nginx |
| Server environment | Linux / Ubuntu |
| Remote development | Visual Studio Code Remote - SSH |
| Transport security | HTTPS / TLS |

## Project Structure

```text
my-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── backend-node/
│   ├── app.js
│   ├── index.js
│   ├── Dockerfile
│   ├── package.json
│   └── tests/
├── backend-python/
│   ├── app/
│   ├── alembic/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── database/
├── docs/
│   └── ci-workflow.md
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

This tree is a high-level overview; additional configuration and supporting files are omitted for readability.

## Key Engineering Milestones

- Developed independent FastAPI and Express backend applications.
- Integrated both backends with a shared PostgreSQL database.
- Added database migration management using Alembic.
- Created automated tests for application behavior and API functionality.
- Added Python and JavaScript linting to the quality workflow.
- Built a GitHub Actions CI pipeline for automated validation.
- Containerized backend services using Docker.
- Orchestrated application services and PostgreSQL using Docker Compose.
- Configured Nginx reverse-proxy routing.
- Deployed services on a Linux server and configured HTTPS.
- Practiced failure detection and post-deployment verification.

## Automated Testing and CI/CD

GitHub Actions automates validation and delivery tasks for changes to the `main` branch.

The workflow can run on pushes, pull requests targeting `main`, and manual dispatches.

The pipeline includes:

- Automated Python tests using pytest.
- Automated Node.js tests using npm.
- Python linting using Ruff.
- JavaScript linting using ESLint.
- Python and Node.js Docker image builds.
- Docker image verification.
- Publishing container images to GitHub Container Registry (GHCR).
- A manually triggered production deployment workflow for the `main` branch.

The Python CI job also verifies that its required test secret is available before running the test suite.

The workflow has been developed and tested incrementally, including an intentional failure to verify that unsuccessful checks are detected.

These practices provide experience with automated quality checks, container publishing, and controlled deployment workflows.

## Containerization and Deployment

Docker and Docker Compose coordinate the backend applications, database, and supporting infrastructure.

Nginx provides reverse-proxy routing. The deployment work includes Linux server administration, HTTPS/TLS configuration, service health checks, and database persistence verification.

## Security Practices

The project uses `.gitignore` to exclude appropriate local and generated files, separates local configuration from application code, and incorporates security checks into the development workflow.

Sensitive credentials should never be committed to the public repository. Ignoring a file does not remove it if it was previously tracked.

## Learning Objectives

This project develops practical experience in:

- REST API development with Python and JavaScript.
- Relational database integration and schema migrations.
- Automated testing and code quality.
- Git and GitHub workflows.
- Continuous integration and delivery.
- Docker containerization and service networking.
- Linux administration and remote development.
- Reverse-proxy configuration and HTTPS deployment.

## Project Status

This is an ongoing backend engineering project. Its milestones document the progression from API development and database integration to automated quality checks, containerization, and server deployment.

**Author:** Chris Edwards

**GitHub:** [chrisedwards551](https://github.com/chrisedwards551)

**Repository:** [my-api](https://github.com/chrisedwards551/my-api)
