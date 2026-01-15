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
        print(f"Aufgabe: {aufgaben['Titel']} \nAufgabenbeschreibung: {aufgaben['_aufgabenbeschreibung']} \nAufgabenbeschreibung: {aufgaben['Aufgabenbeschreibung']} ")

def aufgabe_open():
    fehler = 0
    richtig = True
    for aufgaben in aufgabenListe:
        for uebung in aufgaben['UebungenListe']:
            x = 0
            if richtig:
                for i in uebung['Moeglichkeiten']:
                    print(i)
                antwort = int(input('1, 2 oder 3?'))
                if antwort == uebung['KorrekteAntwort']:
                    pass
                else:
                    fehler +=1
                x+=1
                if x == 10:
                    break
    print(f"Fehler {fehler}")

jsonladen()
#aufgaben_titel_auflisten()
#aufgaben_auflisten()
aufgabe_open()