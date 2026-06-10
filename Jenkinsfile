pipeline {
    agent any

    environment {
        IMAGE_NAME = "vineethpv1997/python"
        K8S_MASTER = "192.168.232.135"
        DEPLOYMENT = "python-demo"
        CONTAINER = "python-demo"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                """
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh """
                    echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin

                    docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                    docker push ${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh """
                ssh root@${K8S_MASTER} '
                kubectl set image deployment/${DEPLOYMENT} \
                ${CONTAINER}=${IMAGE_NAME}:${BUILD_NUMBER}

                kubectl rollout status deployment/${DEPLOYMENT}
                '
                """
            }
        }

    }

    post {
        success {
            echo "Deployment completed successfully"
        }

        failure {
            echo "Pipeline failed"
        }
    }
}
