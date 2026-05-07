pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        DOCKER_IMAGE   = "zuriyat/ml-metrics-api"
        CONTAINER_NAME = "ml-metrics-container"
        APP_PORT       = "8000"
    }

    stages {

        stage('Fetch Data from GitHub') {
            steps {
                echo 'Fetching latest code and dataset...'
                checkout scm
            }
        }

        stage('Train Model') {
            steps {
                echo 'Training model...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt -q
                    python3 train.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t ${DOCKER_IMAGE}:latest .'
            }
        }

        stage('Run Docker Container') {
            steps {
                echo 'Starting container...'
                sh '''
                    docker stop ${CONTAINER_NAME} || true
                    docker rm   ${CONTAINER_NAME} || true
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p ${APP_PORT}:8000 \
                        ${DOCKER_IMAGE}:latest
                '''
            }
        }

        stage('Verify API') {
            steps {
                sh '''
                    sleep 8
                    curl -f http://localhost:8000/metrics
                '''
            }
        }
    }

    post {
        success { echo 'Pipeline SUCCESS - API is live!' }
        failure { echo 'Pipeline FAILED - check logs above' }
    }
}
