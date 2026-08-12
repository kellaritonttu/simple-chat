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
                script {
                    // Define variables
                    def repoUrl = 'github.com/kellaritonttu/simple-chat.git'
                    def tfVarsFile = 'terraform/terraform.image.auto.tfvars'
                    def branchName = env.GIT_BRANCH.replace('origin/', '')

                    // Update the Terraform file
                    sh """
                        sed -i 's/image_tag = .*/image_tag = \"${GIT_SHA}\"/' ${tfVarsFile}
                        cat ${tfVarsFile}
                    """

                    // Configure Git
                    sh """
                        git config user.email "jenkins@ci"
                        git config user.name "Jenkins"
                    """

                    // Stage and commit changes
                    sh """
                        git add ${tfVarsFile}
                        if ! git diff --staged --quiet; then
                            git commit -m "ci: update image tag to ${GIT_SHA}"
                        fi
                    """

                    // Push changes
                    withCredentials([usernamePassword(
                        credentialsId: 'github-credentials',
                        usernameVariable: 'GITHUB_USER',
                        passwordVariable: 'GITHUB_TOKEN'
                    )]) {
                        sh """
                            git push https://\${GITHUB_USER}:\${GITHUB_TOKEN}@${repoUrl} HEAD:${branchName}
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