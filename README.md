# Simple Chat

A Simple Chat application with a Terraform-managed CI/CD pipeline for Google Cloud Platform (GCP).

## Project Overview

This project provides a real-time chat application with a fully automated CI/CD pipeline using:

- Google Cloud Run for hosting the `backend` and `frontend` services.
- Terraform to manage GCP resources.
- Jenkins for orchestrating the deployment pipeline.

The pipeline automates:

- Docker image builds for both services.
- Pushing images to DockerHub.
- Updating Terraform configurations in terraform.image.auto.tfvars.
- Triggering Terraform to apply changes to GCP.

## Pipeline

### Manually run Deploy Jenkins Jobs

They are capable of:

1. Creating docker images
2. Pushing them into Dockerhub repositories
3. Updating Terraform image tags in `terraform.image.auto.tfvars` file
4. Applying terraform configuration.  

## Application Features

| Feature | Description |
| -- | -- |
| **Messaging** | Real-time chat functionality. |

## Prerequisites

### Tools

- Docker and Docker Compose
- Google Cloud Platform (GCP) Account

### Secrets Setup

Copy the example jenkins environment file and fill in the credentials:

```sh
cp jenkins/.env.example jenkins/.env
```

### Required credentials

| Credentials | Description |
| -- | -- |
| JENKINS_ADMIN_PASSWORD | Admin password for Jenkins UI login |
| DOCKERHUB_USERNAME | DockerHub repository username |
| DOCKERHUB_TOKEN | DockerHub repository access token |
| GITHUB_USERNAME | GitHub username |
| GITHUB_TOKEN | GitHub fine-grained personal access token |

## Deployment Guide

### Set up Jenkins

1. Navigate to the `jenkins/` directory:

```sh
cd jenkins
```

2. Start Jenkins using Docker Compose:

```sh
docker-compose up --build
```

Jenkins will be available at **`http://localhost:8080`**

### Configure Jenkins Jobs

1. Login in to the Jenkins UI.
2. Run the **seed job** to create all pipeline jobs defined in `jobs/seed.groovy`.

### Deploy the Application

1. In Jenkins UI , navigate to the `simple-chat` folder.
2. Run the `deploy` job.

### Access the Application

1. After deployment, copy the **frontend URL** from Terraform outputs
2. Open the URL in a new tab to start Simple Chat

## Usage

- Start chatting in real-time with other users.