#logic for Rechtschreib-Tool
import json

aufgabenListe = [] #leere Aufgabenliste wird erstellt

#die aufgaben.json datei wird geladen und alle Inhalte in die Aufgabenliste gesteckt
def jsonladen():
    with open ("aufgaben.json","r",encoding= "utf-8" ) as f:
        global aufgabenListe
        aufgabenListe = json.load(f)

#listet alle Titel der Aufgaben auf
def aufgaben_titel_auflisten():
    for aufgaben in aufgabenListe:
        print(f"Aufgabe:{aufgaben["Titel"]}")

def aufgaben_auflisten():
    for aufgaben in aufgabenListe:
        print(f"Aufgabe: {aufgaben['Titel']} \nAufgabenbeschreibung: {aufgaben['_aufgabenbeschreibung']} \nAufgabenbeschreibung2: {aufgaben['Aufgabenbeschreibung']} ")

jsonladen()
#aufgaben_titel_auflisten()
aufgaben_auflisten()