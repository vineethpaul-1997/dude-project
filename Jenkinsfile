pipeline {
    agent any

    environment {
        FRONTEND_IMAGE = "vineethpv1997/devops-frontend"
        BACKEND_IMAGE  = "vineethpv1997/devops-backend"

        K8S_MASTER = "192.168.232.135"

        GIT_REPO = "https://github.com/vineethpaul-1997/YOUR_REPO.git"
        GIT_BRANCH = "main"
    }

    stages {

        stage('Checkout') {
            steps {
                git(
                    url: "${GIT_REPO}",
                    branch: "${GIT_BRANCH}",
                    credentialsId: "github-creds"
                )
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh """
                docker build --no-cache \
                -t ${FRONTEND_IMAGE}:${BUILD_NUMBER} \
                -t ${FRONTEND_IMAGE}:latest \
                ./frontend
                """
            }
        }

        stage('Build Backend Image') {
            steps {
                sh """
                docker build --no-cache \
                -t ${BACKEND_IMAGE}:${BUILD_NUMBER} \
                -t ${BACKEND_IMAGE}:latest \
                ./backend
                """
            }
        }

        stage('Push Images') {
            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {

                    sh """

                    echo \$DOCKER_PASS | docker login \
                    -u \$DOCKER_USER \
                    --password-stdin

                    docker push ${FRONTEND_IMAGE}:${BUILD_NUMBER}
                    docker push ${FRONTEND_IMAGE}:latest

                    docker push ${BACKEND_IMAGE}:${BUILD_NUMBER}
                    docker push ${BACKEND_IMAGE}:latest

                    """

                }

            }
        }

        stage('Deploy Frontend') {
            steps {

                sh """

                scp -o StrictHostKeyChecking=no \
                frontend/deployment.yaml \
                root@${K8S_MASTER}:/root/frontend-deployment.yaml

                scp -o StrictHostKeyChecking=no \
                frontend/service.yaml \
                root@${K8S_MASTER}:/root/frontend-service.yaml

                ssh -o StrictHostKeyChecking=no \
                root@${K8S_MASTER} '

                kubectl apply -f /root/frontend-deployment.yaml

                kubectl apply -f /root/frontend-service.yaml

                kubectl rollout restart deployment/frontend

                kubectl rollout status deployment/frontend

                '

                """

            }
        }

        stage('Deploy Backend') {
            steps {

                sh """

                scp -o StrictHostKeyChecking=no \
                backend/deployment.yaml \
                root@${K8S_MASTER}:/root/backend-deployment.yaml

                scp -o StrictHostKeyChecking=no \
                backend/service.yaml \
                root@${K8S_MASTER}:/root/backend-service.yaml

                ssh -o StrictHostKeyChecking=no \
                root@${K8S_MASTER} '

                kubectl apply -f /root/backend-deployment.yaml

                kubectl apply -f /root/backend-service.yaml

                kubectl rollout restart deployment/backend

                kubectl rollout status deployment/backend

                '

                """

            }
        }

        stage('Verify Deployment') {
            steps {

                sh """

                ssh -o StrictHostKeyChecking=no \
                root@${K8S_MASTER} "

                kubectl get pods -o wide

                kubectl get svc

                "

                """

            }
        }

    }

    post {

        success {
            echo "✅ Frontend and Backend deployed successfully"
        }

        failure {
            echo "❌ Pipeline failed"
        }

    }
}
