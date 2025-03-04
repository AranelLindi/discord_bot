# Basis Image: Schlankes Python Image
FROM python:3.12-slim

# Setzt das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiert die benötigten Dateien in den Container
COPY requirements.txt ./
COPY .env ./
COPY LindBot.py ./
COPY VotingClass.py ./
COPY VoteOption.py ./
COPY README.md ./

# Installiert die nötigen Python Abhängigkeiten
RUN pip install --no-chache-dir -r requirements.txt

# Startet den Bot
CMD ["python", "LindBot.py"]
