""" Diese Datei enthält lediglich den Container für eine Vote-Klasse
    um eine Abstimmungsmöglichkeit (VoteOption) darzustellen
"""

# Hilfscontainer um Abstimmungsoptionen zu speichern und Stimmen anonym zu zählen
# (Die Notwendigkeit der Existen von Wählerregister wird überliegendem Code überlassen)
class VoteOption:
    def __init__(self, name): # Konstruktor
        self.__name = name
        self.__votes = 0 # private
    
    def addVote(self): # Inkrementiert Stimmenabgabe für diese Wahloption um eins
        self.__votes += 1 

    def removeVote(self): # Inkrementiert Stimmenabgabe für diese Wahloption um eins
        self.__votes -= 1
    
    def getVotes(self): # Gibt Anzahl an Stimmen dieser Option zurück
        return self.__votes

    def getDescription(self): # Gibt die Abstimmungsbeschreibung zurück
        return self.__name