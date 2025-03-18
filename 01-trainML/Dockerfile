# Dockerfile final
FROM wlf42/prefect-aws:3.2.11

WORKDIR /opt/prefect

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY train.py .

CMD ["prefect", "version"]
