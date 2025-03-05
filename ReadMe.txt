Discord Bot, der einfache Funktionen sowie Kalendar- und Abstimmungsfähigkeiten besitzt. Ist darauf ausgelegt in einem Docker Container zu laufen.

Der Bot unterstützt folgende Befehle:
!roll X - Liefert Zufallszahl zwischen 1 und X (falls X weg gelassen wird zwischen 1 und 6)
!flip - Wirft eine Münze
!time - Liefert aktuelles Datum mit Uhrzeit
!ping - Berechnet die Round Trip Time des Bots
!uptime - Zeigt an wie lange er schon online ist
!remindme X Y - Erinnert den User nach X Sekunden an Nachricht Y
---
!day X - Gibt den Wochentag zu einem spezifischen Datum aus
!addevent x Y - Fügt ein neues Event am Datum X mit dem Titel Y dem Kalender hinzu
!listevents - Listet alle zukünftigen Events auf
---
!Voting X A B C ... - Erstellt eine Abstimmung zu Frage X mit den Optionen A B C ... 
!Vote A - Gibt eine Stimme für Option A ab
!ShowResults - Zeigt das Abstimmungsergebnis an
!CloseVoting - Schließt die Abstimmung

-----------------BEFEHLE-----------------
Docker-Image bauen:
docker build -t discord-bot .

Docker Container starten:
docker-compose up -d # -d sorgt dafür, dass Container im Hintergrund gestartet wird!

Logs abrufen
docker logs -f discord-bot
