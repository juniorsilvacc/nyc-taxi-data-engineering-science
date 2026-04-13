FROM python:3.12-slim

WORKDIR /app

# 1. Instalando dependências e o OpenJDK 21 (versão disponível no Debian Trixie)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    openjdk-21-jre-headless \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. Atualizando o caminho do JAVA_HOME para a versão 21
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]