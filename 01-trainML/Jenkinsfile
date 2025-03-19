#!/usr/bin/env groovy

pipeline {
  agent {
    kubernetes {
      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: kaniko
      image: wlf42/kaniko-git:latest
      imagePullPolicy: Always
      command: ["sleep"]
      args: ["99d"]
      env:
        - name: DOCKER_CONFIG
          value: /kaniko/.docker
      volumeMounts:
        - name: jenkins-docker-cfg
          mountPath: /kaniko/.docker
      resources:
        limits:
          memory: "6Gi"
          cpu: "3000m"
        requests:
          memory: "2Gi"
          cpu: "2000m"
  volumes:
    - name: jenkins-docker-cfg
      projected:
        sources:
          - secret:
              name: regcred
              items:
                - key: .dockerconfigjson
                  path: config.json
"""
    }
  }

  environment {
    TAG = "latest"
    IMAGE_NAME = "wanderson/nyc-taxi-flow"
    DOCKER_DEST = "wlf42/nyc-taxi-flow:latest"
    PREFECT_API_URL = "http://prefect-server.default.svc.cluster.local:4200/api"
  }

  triggers {
    githubPush()
  }

  stages {
    stage('Build Docker Image with Kaniko') {
      steps {
        container(name: 'kaniko') {
          sh '''
            echo "Clonando o repositório..."
            git clone https://github.com/wanderson42/nyc-taxi-aws-mlops.git /workspace/repo

            echo "Verificando conteúdo clonado..."
            ls -la /workspace/repo/01-trainML

            echo "Iniciando build com Kaniko..."
            /kaniko/executor \
              --context=/workspace/repo/01-trainML \
              --dockerfile=/workspace/repo/01-trainML/Dockerfile \
              --destination=${DOCKER_DEST} \
              --cache=true \
              --compressed-caching=false \
              --cache-copy-layers \
              --verbosity=debug \
              --force
          '''
        }
      }
    }

    stage('Deploy to Prefect') {
      steps {
        container(name: 'kaniko') {
          withEnv(["PREFECT_API_URL=${PREFECT_API_URL}"]) {
            sh '''
              echo "Verificando conexão com Prefect em: $PREFECT_API_URL"
              cd /workspace/repo/01-trainML
              prefect config validate
              echo "Iniciando deploy para Prefect Server..."
              make deploy-months YEAR=2024
            '''
          }
        }
      }
    }
  }
}


