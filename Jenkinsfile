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
            docker build --no-cache -t ${IMAGE_NAME}:${BUILD_NUMBER} .
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
            scp deployment.yaml root@${K8S_MASTER}:/root/
            scp service.yaml root@${K8S_MASTER}:/root/

            ssh root@${K8S_MASTER} '
            kubectl apply -f /root/deployment.yaml
            kubectl apply -f /root/service.yaml
            kubectl rollout status deployment/${DEPLOYMENT}
            '
            """
        }
    }
}

post {
    success {
        echo 'Deployment completed successfully'
    }

    failure {
        echo 'Pipeline failed'
    }
}

}

