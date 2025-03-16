import os

# Variáveis do Makefile que podem ser passadas como parâmetros ou definidas no próprio código
YEAR = os.getenv('YEAR', '2024')
TAXI_TYPE = os.getenv('TAXI_TYPE', 'green')
BUCKET = os.getenv('BUCKET', 'mlflow-cloud-artifacts')
DATASET_FOLDER = os.getenv('DATASET_FOLDER', 'nyc-trip-data')
ARTIFACT_FOLDER = os.getenv('ARTIFACT_FOLDER', 'nyc-mlflow-artifacts')
ENTRYPOINT = os.getenv('ENTRYPOINT', 'train.py:main_flow')
DEPLOYMENT_NAME = os.getenv('DEPLOYMENT_NAME', 'train-nyc')
TIMEZONE = os.getenv('TIMEZONE', 'America/Sao_Paulo')
POOL = os.getenv('POOL', 'minikube-workpool')
IMAGE_NAME = os.getenv('IMAGE_NAME', 'wanderson/nyc-taxi-flow')

# Criando o arquivo prefect.yaml
with open('prefect.yaml', 'w') as f:
    f.write(f"""
name: flows
prefect-version: 3.2.11

build:
  - prefect_docker.deployments.steps.build_docker_image:
      id: build-image
      requires: prefect-docker>=0.4.0
      image_name: '{{{{ $PREFECT_IMAGE_NAME }}}}'
      tag: {os.getenv('TAG', 'latest')}
      dockerfile: Dockerfile
      platform: linux/amd64

push:
  - prefect_aws.deployments.steps.push_to_s3:
      id: push_code
      requires: prefect-aws>=0.3.4
      bucket: {BUCKET}
      folder: nyc-deployments
      credentials: '{{{{ prefect.blocks.aws-credentials.aws-s3-creds }}}}'

pull:
  - prefect_aws.deployments.steps.pull_from_s3:
      id: pull_code
      requires: prefect-aws>=0.3.4
      bucket: '{{{{ push_code.bucket }}}}'
      folder: '{{{{ push_code.folder }}}}'
      credentials: '{{{{ prefect.blocks.aws-credentials.aws-s3-creds }}}}'

definitions:
  work_pool:
    name: {POOL}
    job_variables:
      image: '{{{{ build-image.image }}}}'

deployments: []
""")
    print("Arquivo prefect.yaml gerado com sucesso!")
