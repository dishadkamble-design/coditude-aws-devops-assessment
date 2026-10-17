
# Coditude AWS DevOps Assessment

## Overview

This repository demonstrates an AWS DevOps assessment for a full-stack task management application.

**Technology Stack:**
- Frontend: Next.js
- Backend: Python FastAPI
- Database: PostgreSQL
- Infrastructure as Code: AWS CloudFormation
- CI/CD: GitHub Actions

The project includes both containerized and non-containerized AWS deployment approaches.

**Deployment status:** No live AWS deployment has been performed. Infrastructure and deployment configurations are included for assessment purposes.

## 1. Containerized Deployment - Amazon ECS

The containerized approach uses:
- Docker containers for frontend and backend
- Amazon ECS
- Application Load Balancer
- Amazon RDS PostgreSQL
- AWS Secrets Manager
- CloudFormation templates

Infrastructure files:
- `infrastructure/network.yaml`
- `infrastructure/security.yaml`
- `infrastructure/database.yaml`
- `infrastructure/ecs.yaml`

## 2. Non-Containerized Deployment - Amazon EC2

The non-containerized approach uses:
- Amazon EC2
- Auto Scaling Group
- Application Load Balancer
- systemd services
- Amazon RDS PostgreSQL
- AWS Secrets Manager

Infrastructure files:
- `infrastructure/ec2/ec2.yaml`
- `infrastructure/ec2/user-data.sh`

The EC2 bootstrap script installs dependencies, configures the frontend and backend services, and retrieves database credentials from AWS Secrets Manager.

## 3. CI/CD

GitHub Actions workflows are available in `.github/workflows/`.

- `ci.yml` - Application and infrastructure validation
- `deploy-ecs.yml` - ECS deployment workflow configuration

AWS deployment requires appropriate IAM permissions, repository configuration, and AWS infrastructure resources.

## 4. Run Application Locally

### Prerequisites

- Docker Desktop
- Docker Compose

### Start Application

```bash
docker compose up --build -d
```

### Application URLs

- Frontend: http://localhost:3000
- Backend Health: http://localhost:8000/health
- API Documentation: http://localhost:8000/docs
- Tasks API: http://localhost:8000/api/tasks

### Stop Application

```bash
docker compose down
```

Do not use `docker compose down -v` unless you want to remove local database data.

## 5. Security

- AWS Secrets Manager for database credentials
- Security groups for network access control
- HTTPS configuration for AWS Application Load Balancers
- IAM roles for AWS service permissions
- Local development credentials are not intended for production

## 6. Validation

CloudFormation templates were validated locally using `cfn-lint` for the `ap-south-1` AWS region.

GitHub Actions CI completed successfully.

## 7. Assessment Notes

Both containerized and non-containerized AWS infrastructure configurations are included.

No live AWS resources were deployed, as deployment was not required for this assessment.

Runtime deployment verification remains pending.
