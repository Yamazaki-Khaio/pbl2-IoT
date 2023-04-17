# imagem base
FROM python:3.8-slim-buster

# atualiza o sistema e instala as dependências necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libssl-dev \
    libffi-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# copia o código para dentro do container
COPY . /app

# define o diretório de trabalho
WORKDIR /app

# instala as dependências Python
RUN pip3 install -r requirements.txt

# expõe a porta do MQTT broker
EXPOSE 1883

# define o comando que será executado ao iniciar o container
CMD ["python3", "posto.py"]
