# syntax=docker/dockerfile:1

# Usa uma imagem Python base
FROM python:3.12.7-slim

# Instala dependências básicas do sistema e o AWS CLI
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl unzip less groff ca-certificates \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Define o diretório de trabalho
WORKDIR /app

# Copia as dependências e instala
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copia o código da aplicação
COPY app.py .

# Expõe a porta do serviço
EXPOSE 9696

# Configura a entrada do serviço
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "app:app", "--timeout", "120"]


#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=9696"]
