# Basis Image: Schlankes Python Image
FROM python:3.12-slim

# Setzt das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiert die benötigten Dateien in den Container
COPY requirements.txt ./
COPY .env ./
COPY LindBot.py ./
COPY cogs/ ./cogs/
COPY events.json ./
COPY README.md ./

# Installiert die nötigen Python Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Installiert deutsche Locale
RUN apt-get update && apt-get install -y locales && \
    echo "de_DE.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen de_DE.UTF-8 && \
    update-locale LANG=de_DE.UTF-8

# Setzt Umgebungsvariablen für die Locale
ENV LANG=de_DE.UTF-8
ENV LANGUAGE=de_DE:de
ENV LC_ALL=de_DE.UTF-8

# Startet den Bot
CMD ["python", "LindBot.py"]
