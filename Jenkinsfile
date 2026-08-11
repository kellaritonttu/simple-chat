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
                            docker build \
                                -t ${DOCKERHUB_NAMESPACE}/simple-chat-frontend:${GIT_SHA} \
                                -t ${DOCKERHUB_NAMESPACE}/simple-chat-frontend:latest \
                                -f frontend/Dockerfile .
                            docker push ${DOCKERHUB_NAMESPACE}/simple-chat-frontend:${GIT_SHA}
                            docker push ${DOCKERHUB_NAMESPACE}/simple-chat-frontend:latest
                        """
                    }
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