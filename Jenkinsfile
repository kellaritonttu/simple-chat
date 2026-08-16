@Library('shared') _

pipeline {
    agent any

    environment {
        OWNER               = 'kellaritonttu'
        GIT_SHA             = "${GIT_COMMIT[0..7]}"
        DOCKERHUB_NAMESPACE = 'harhatilatonttu'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    sh 'echo $DOCKERHUB_TOKEN | docker login -u $DOCKERHUB_USER --password-stdin'
                }
            }
        }

        stage('Build and Push Images') {
            parallel {
                stage('backend') {
                    steps {
                        sh """
                            docker build \
                                -t ${DOCKERHUB_NAMESPACE}/simple-chat-backend:${GIT_SHA} \
                                -t ${DOCKERHUB_NAMESPACE}/simple-chat-backend:latest \
                                -f backend/Dockerfile . --no-cache
                            docker push ${DOCKERHUB_NAMESPACE}/simple-chat-backend:${GIT_SHA}
                            docker push ${DOCKERHUB_NAMESPACE}/simple-chat-backend:latest
                        """
                    }
                }
                stage('frontend') {
                    steps {
                        sh """
                            cd ./frontend
                            docker build \
                                -t ${DOCKERHUB_NAMESPACE}/simple-chat-frontend:${GIT_SHA} \
                                -t ${DOCKERHUB_NAMESPACE}/simple-chat-frontend:latest \
                                -f Dockerfile . --no-cache
                            docker push ${DOCKERHUB_NAMESPACE}/simple-chat-frontend:${GIT_SHA}
                            docker push ${DOCKERHUB_NAMESPACE}/simple-chat-frontend:latest
                        """
                    }
                }
            }
        }

        stage('Update Terraform') {
            steps {
                script {
                    // Define variables
                    def repoUrl = 'github.com/kellaritonttu/simple-chat.git'
                    def tfVarsFile = 'terraform/terraform.image.auto.tfvars'
                    def branchName = env.GIT_BRANCH.replace('origin/', '')

                    // Clone github repo
                    cloneTerraformRepo(
                        repo:   repoUrl,
                        branch: branchName,
                        dir:    'terraform-infra'
                    )

                    // Update the Terraform file
                    dir('terraform-infra') {
                        updateImageTag(
                            file: tfVarsFile,
                            key:  'image_tag',
                            tag:  GIT_SHA
                        )
                    }

                    // Commit changes and push changes
                    pushTerraformRepo(
                        repo:    'https://github.com/kellaritonttu/simple-chat.git',
                        branch:  branchName,
                        file:    tfVarsFile,
                        message: "ci: update image tag to ${GIT_SHA}",
                        dir:     'terraform-infra'
                    )
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
            cleanWs()
        }
    }
}