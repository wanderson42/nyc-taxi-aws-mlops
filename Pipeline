pipeline {
    agent any

    environment {
        TAG = "latest"
        IMAGE_NAME = "wanderson/nyc-taxi-flow"
    }

    triggers {
        githubPush()
    }

    stages {
        stage('Clone repo') {
            steps {
                git credentialsId: 'seu-credencial-id', url: 'https://github.com/wanderson42/nyc-taxi-aws-mlops.git', branch: 'master'
            }
        }

        stage('Build Docker image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$TAG .'
                sh 'docker push $IMAGE_NAME:$TAG'
            }
        }

        stage('Deploy to Prefect') {
            steps {
                sh 'make deploy-months YEAR=2024'
            }
        }
    }
}
