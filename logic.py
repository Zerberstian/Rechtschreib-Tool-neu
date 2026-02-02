#logic for Rechtschreib-Tool (aufgaben.json)
import json

geladeneAufgaben = [] #Create an empty list for questions
bereichListe = [] #Create an empty list for topics

#Function to load aufgaben.json
def jsonladen():
    with open ("aufgaben.json","r",encoding= "utf-8" ) as f:
        global geladeneAufgaben
        geladeneAufgaben = json.load(f)

#Function to list all "uebungsbereich"
def uebungsbereich_auflisten():
    uebungsbereich_liste = []
    for uebungsbereich in geladeneAufgaben:
        if uebungsbereich['Uebungsbereich'] not in uebungsbereich_liste:
            uebungsbereich_liste.append(uebungsbereich['Uebungsbereich'])
    return uebungsbereich_liste

#Function to list all titels of a bereich
def list_titels(bereiche):
    titels = []
    if not type(bereiche) == list:
        for titel in geladeneAufgaben:
            if bereiche == titel['Uebungsbereich']:
                titels.append(titel['Titel'])
    else:
        for bereich in bereiche:
            for titel in geladeneAufgaben:
                if bereich == titel['Uebungsbereich']:
                    titels.append(titel['Titel'])
    return titels

#Function to list all "Übungen" of a titel
def list_uebungen(titels):
    aufgaben_liste = []
    if not type(titels) == list:
        for aufgabe in geladeneAufgaben:
            if titels == aufgabe['Titel']:
                for uebung in aufgabe['UebungenListe']:
                    aufgaben_liste.append(uebung)
    else:
        for titel in titels:
            for aufgabe in geladeneAufgaben:
                if titel == aufgabe['Titel']:
                    for uebung in aufgabe['UebungenListe']:
                        aufgaben_liste.append(uebung)
    print(len(aufgaben_liste))
    return aufgaben_liste

if __name__ == '__main__':
    jsonladen()
    print(list_uebungen(list_titels('Andere Probleme')))