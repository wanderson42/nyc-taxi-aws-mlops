FROM prefecthq/prefect:3.2.11-python3.12

# Instala dependências básicas do sistema e o AWS CLI
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl unzip less groff ca-certificates \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Definindo o diretório de trabalho
WORKDIR /opt/prefect

# Copiar as dependências e instalar
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copiar os fluxos para o diretório correto
COPY train.py .

# Não configure as credenciais diretamente aqui.
