""" Diese Datei enthält lediglich den Container für eine Vote-Klasse
    um eine Abstimmungsmöglichkeit (VoteOption) darzustellen
"""

# Hilfscontainer um Abstimmungsoptionen zu speichern und Stimmen anonym zu zählen
# (Die Notwendigkeit der Existen von Wählerregister wird überliegendem Code überlassen)


class VoteOption:
    def __init__(self, name: str):  # Konstruktor
        #print("VoteOption Konstruktor was called!\n")
        self.name = name
        self.votes = 0  # private
