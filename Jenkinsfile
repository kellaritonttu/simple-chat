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
                                -f backend/Dockerfile .
                            docker push ${DOCKERHUB_NAMESPACE}/simple-chat-backend:${GIT_SHA}
                            docker push ${DOCKERHUB_NAMESPACE}/simple-chat-backend:latest
                        """
                    }
                }
                stage('frontend') {
                    steps {
                        sh """
                            cd ./frontend
                            docker build --no-cache \
                                -t ${DOCKERHUB_NAMESPACE}/simple-chat-frontend:${GIT_SHA} \
                                -t ${DOCKERHUB_NAMESPACE}/simple-chat-frontend:latest \
                                -f Dockerfile .
                            docker push ${DOCKERHUB_NAMESPACE}/simple-chat-frontend:${GIT_SHA}
                            docker push ${DOCKERHUB_NAMESPACE}/simple-chat-frontend:latest
                        """
                    }
                }
            }
        }

        stage('Update Terraform') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-credentials',
                    usernameVariable: 'GITHUB_USER',
                    passwordVariable: 'GITHUB_TOKEN'
                )]) {
                    sh """
                        sed -i 's/image_tag = .*/image_tag = "${GIT_SHA}"/' terraform/terraform.tfvars
                        git config user.email "jenkins@ci"
                        git config user.name "Jenkins"
                        git add terraform/terraform.tfvars
                        git diff --staged --quiet || git commit -m "ci: update image tag to ${GIT_SHA}"
                        git push https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/your-username/chat.git HEAD:${env.BRANCH_NAME}
                    """
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