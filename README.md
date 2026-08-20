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
- Triggering Terraform Cloud to apply changes to GCP.

## Pipeline

### Manually run the Deploy Jenkins Job

It would:

1. Create docker images
2. Push them into Dockerhub repositories
3. Update Terraform image tags in `terraform.image.auto.tfvars` file
4. Send terraform apply command to the Terraform Cloud.  
5. Terraform Cloud Updates the GCP project.

## Application Features

| Feature | Description |
| -- | -- |
| **Authentication** | User login via Google OAuth. |
| **User Account** | Update display name in the app. |
| **Messaging** | Real-time chat functionality. |

## Prerequisites

### Tools

- Docker and Docker Compose
- Google Cloud Platform (GCP) Account
- Terraform Cloud Organization with GCP credentials

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
| TF_CLOUD_TOKEN | Terraform Cloud access token |


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

- Log in using your Google account.
- Update your display name in the app settings.
- Start chatting in real-time with other users.