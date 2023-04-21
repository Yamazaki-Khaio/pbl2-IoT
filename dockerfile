# Imagem base do Python 3.9
FROM python:3.9

# Diretório de trabalho
WORKDIR /app

# Instalação das dependências
COPY requirements.txt .
RUN pip install -r requirements.txt

# Cópia do código-fonte da aplicação
COPY posto.py .

# Comando padrão para execução do container
CMD ["python", "posto.py"]

# Cópia do código-fonte da aplicação
COPY carro.py .

# Comando padrão para execução do container
CMD ["python", "carro.py"]