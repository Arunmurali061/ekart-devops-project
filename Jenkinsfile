

pipeline {
    agent any

    environment {
        IMAGE_NAME = 'quay.io/arunmdevops/ekart'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Downloading eKart source code'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building eKart Docker image'

                sh '''
                    docker build \
                      -t ${IMAGE_NAME}:${BUILD_NUMBER} \
                      -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Verify Image') {
            steps {
                echo 'Verifying Docker image'

                sh 'docker image inspect ${IMAGE_NAME}:${BUILD_NUMBER}'
                sh 'docker images ${IMAGE_NAME}'
            }
        }

        stage('Push to Quay') {
            steps {
                echo 'Pushing eKart image to Quay'

                withCredentials([usernamePassword(
                    credentialsId: 'quay-robot-creds',
                    usernameVariable: 'QUAY_USER',
                    passwordVariable: 'QUAY_TOKEN'
                )]) {
                    sh '''
                        set +x
                        trap 'docker logout quay.io >/dev/null 2>&1 || true' EXIT

                        echo "$QUAY_TOKEN" | docker login quay.io \
                          --username "$QUAY_USER" \
                          --password-stdin

                        docker push "${IMAGE_NAME}:${BUILD_NUMBER}"
                        docker push "${IMAGE_NAME}:latest"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'eKart CI pipeline completed successfully!'
        }

        failure {
            echo 'eKart CI pipeline failed. Check the console output.'
        }
    }
}

