pipeline {
agent any

```
environment {
    IMAGE_NAME = "vineethpv1997/python"
    K8S_MASTER = "192.168.232.135"
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

    stage('Push Docker Image') {
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
            sed 's|vineethpv1997/python:latest|${IMAGE_NAME}:${BUILD_NUMBER}|g' deployment.yaml > deployment-final.yaml

            scp deployment-final.yaml root@${K8S_MASTER}:/root/deployment.yaml
            scp service.yaml root@${K8S_MASTER}:/root/service.yaml

            ssh root@${K8S_MASTER} '
                kubectl apply -f /root/deployment.yaml
                kubectl apply -f /root/service.yaml

                kubectl rollout status deployment/python-demo
            '
            """
        }
    }
}

post {
    success {
        echo "Deployment Successful"
    }

    failure {
        echo "Pipeline Failed"
    }
}
```

}

