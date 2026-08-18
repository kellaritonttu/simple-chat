@Library('shared') _

pipeline {
    agent any

    environment {
        OWNER               = 'kellaritonttu'
        GIT_SHA             = "${GIT_COMMIT?.substring(0, 7) ?: 'manual-trigger'}"
        DOCKERHUB_NAMESPACE = 'harhatilatonttu'
    }

    stages {

        stage('Checkout') {
            steps {
                gitCheckout()
            }
        }

        stage('Login to Docker Hub') {
            steps {
                dockerLogin()
            }
        }

        stage('Build and Push Images') {
            parallel {
                stage('migrate') {
                    steps {
                        dockerBuildPush(
                            image:      "${env.DOCKERHUB_NAMESPACE}/simple-chat-migrate", 
                            tag:        env.GIT_SHA, 
                            dockerfile: "backend/Dockerfile.migrate",
                            context:    "."
                        )
                    }
                }
                stage('backend') {
                    steps {
                        dockerBuildPush(
                            image:      "${env.DOCKERHUB_NAMESPACE}/simple-chat-backend", 
                            tag:        env.GIT_SHA, 
                            dockerfile: "backend/Dockerfile",
                            context:    "backend"
                        )
                    }
                }
                stage('frontend') {
                    steps {
                        dockerBuildPush(
                            image:      "${env.DOCKERHUB_NAMESPACE}/simple-chat-frontend", 
                            tag:        env.GIT_SHA, 
                            dockerfile: "frontend/Dockerfile",
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
                    def branchName = (env.GIT_BRANCH ?: 'main').replace('origin/', '')

                    gitConfig()

                    updateImageTag(
                        file: tfVarsFile,
                        key:  'image_tag',
                        tag:  env.GIT_SHA
                    )

                    gitAdd(file: tfVarsFile)
                    gitCommit(message: "ci: update image tag to ${env.GIT_SHA}")
                    gitPush(branch: branchName)
                }
            }
        }

        stage('Deploy') {
            steps {
                terraformDeploy(terraformDir: 'terraform')
            }
        }
    }

    post {
        always {
            dockerClean(images: [
                "${env.DOCKERHUB_NAMESPACE}/simple-chat-backend:${env.GIT_SHA}", 
                "${env.DOCKERHUB_NAMESPACE}/simple-chat-frontend:${env.GIT_SHA}",
                "${env.DOCKERHUB_NAMESPACE}/simple-chat-migrate:${env.GIT_SHA}"
            ])
            dockerLogout()
            cleanWs()
        }
    }
}