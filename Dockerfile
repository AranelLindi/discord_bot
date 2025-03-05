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
# Startet den Bot
CMD ["python", "LindBot.py"]
