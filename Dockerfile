# usa uma imagem leve baseada no Debian Slim
FROM python:3.11-slim

# evita que o python gere arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# define o diretório de trabalho
WORKDIR /app

# instala dependências do sistema para o PostgreSQL e compilação básica
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# instala as dependências do Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# copia o projeto
COPY . /app

# expõe a porta do Django
EXPOSE 8000