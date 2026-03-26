FROM python:3.10-slim

WORKDIR /scraper

# Instalar dependencias del sistema para compilar psycopg2
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /scraper/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /scraper/requirements.txt

COPY . /scraper

# Por ahora, usamos este comando para mantener el contenedor "vivo" y despierto
# así podremos entrar a él y crear nuestro proyecto Scrapy manualmente.
CMD ["tail", "-f", "/dev/null"]