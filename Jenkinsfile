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
                dockerLogin()
            }
        }

        stage('Build and Push Images') {
            parallel {
                stage('backend') {
                    steps {
                        dockerBuildPush(
                            image:      "${env.DOCKERHUB_NAMESPACE}/simple-chat-backend", 
                            tag:        env.GIT_SHA, 
                            dockerfile: "backend/Dockerfile"
                            context:    "backend"
                        )
                    }
                }
                stage('frontend') {
                    steps {
                        dockerBuildPush(
                            image:      "${env.DOCKERHUB_NAMESPACE}/simple-chat-frontend", 
                            tag:        env.GIT_SHA, 
                            dockerfile: "frontend/Dockerfile"
                            context:    "frontend"
                        )
                    }
                }
            }
        }

        stage('Update Terraform') {
            steps {
                script {
                    def tfVarsFile = 'terraform/terraform.image.auto.tfvars'
                    def branchName = env.GIT_BRANCH.replace('origin/', '')

                    // Config Jenkins email in git
                    gitConfig()

                    // Update the Terraform file
                    updateImageTag(
                        file: tfVarsFile,
                        key:  'image_tag',
                        tag:  env.GIT_SHA
                    )

                    // Add file to git 
                    gitAdd(file: tfVarsFile)

                    // Commit Terraform image_tag variable change
                    gitCommit(message: "ci: update image tag to ${env.GIT_SHA}")

                    // Push changes
                    gitPush(
                        repo:   env.GIT_URL,
                        branch: env.GIT_BRANCH.replace('origin/', '')
                    )
                }
            }
        }
    }

    post {
        always {
            dockerClean(image: "${env.DOCKERHUB_NAMESPACE}/simple-chat-backend:${env.GIT_SHA}")
            dockerClean(image: "${env.DOCKERHUB_NAMESPACE}/simple-chat-frontend:${env.GIT_SHA}")
            dockerLogout()
            cleanWs()
        }
    }
}