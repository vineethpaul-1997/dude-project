pipeline {
    agent any

    environment {

        GIT_REPO = "https://github.com/vineethpaul-1997/dude-project.git"
        GIT_BRANCH = "main"

        FRONTEND_IMAGE = "vineethpv1997/devops-frontend"
        BACKEND_IMAGE  = "vineethpv1997/devops-backend"

        K8S_MASTER = "192.168.232.135"
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

        stage('Build Frontend') {
            steps {
                sh """
                docker build --no-cache \
                -t ${FRONTEND_IMAGE}:${BUILD_NUMBER} \
                -t ${FRONTEND_IMAGE}:latest \
                ./frontend
                """
            }
        }

        stage('Build Backend') {
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

        stage('Deploy Database') {

            steps {

                sh """

                scp -o StrictHostKeyChecking=no \
                database/deployment.yaml \
                root@${K8S_MASTER}:/root/mysql-deployment.yaml

                scp -o StrictHostKeyChecking=no \
                database/service.yaml \
                root@${K8S_MASTER}:/root/mysql-service.yaml

                ssh -o StrictHostKeyChecking=no root@${K8S_MASTER} '

                kubectl apply -f /root/mysql-deployment.yaml

                kubectl apply -f /root/mysql-service.yaml

                kubectl rollout status deployment/mysql

                '

                """

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

                ssh -o StrictHostKeyChecking=no root@${K8S_MASTER} '

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

                ssh -o StrictHostKeyChecking=no root@${K8S_MASTER} '

                kubectl apply -f /root/backend-deployment.yaml

                kubectl apply -f /root/backend-service.yaml

                kubectl rollout restart deployment/backend

                kubectl rollout status deployment/backend

                '

                """

            }

        }

        stage('Verify') {

            steps {

                sh """

                ssh -o StrictHostKeyChecking=no root@${K8S_MASTER} "

                echo '===== PODS ====='

                kubectl get pods -o wide

                echo

                echo '===== SERVICES ====='

                kubectl get svc

                echo

                echo '===== DEPLOYMENTS ====='

                kubectl get deployments

                "

                """

            }

        }

    }

    post {

        success {
            echo "✅ Frontend + Backend + Database deployed successfully"
        }

        failure {
            echo "❌ Pipeline failed"
        }

    }

}
