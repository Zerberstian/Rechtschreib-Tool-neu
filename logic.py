#logic for Rechtschreib-Tool
import json

aufgabenListe = [] #Create an empty list for questions
bereichListe = [] #Create an empty list for topics

#Function to load aufgaben.json
def jsonladen():
    with open ("aufgaben.json","r",encoding= "utf-8" ) as f:
        global aufgabenListe
        aufgabenListe = json.load(f)

#Function to show a question inside the console , answer wrong and the programm will close
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

#Function to show Questions with status "IstSpeziell" True
def spezial_aufgaben():
    for aufgaben in aufgabenListe:
        if aufgaben['IstSpeziell']:
            for uebung in aufgaben['UebungenListe']:
                print(uebung)

#Function to list all "uebungsbereich"
def uebungsbereich_auflisten():
    uebungsbereichListe = []
    for uebungsbereich in aufgabenListe:
        if uebungsbereich['Uebungsbereich'] in uebungsbereichListe:
            pass
        else:
            uebungsbereichListe.append(uebungsbereich['Uebungsbereich'])
    x = 0
    for i in uebungsbereichListe:
        x+=1
        #print(f"{x}. {i}")
    return uebungsbereichListe

#Function to list all topics with their respective titels
def dict_questiontitel():
    bereichdict = {}
    for bereich in uebungsbereich_auflisten():
        Uebungsliste = []
        liste = []
        for aufgaben in aufgabenListe:
            if bereich == aufgaben['Uebungsbereich']:
                liste.append(aufgaben['Titel'])
        bereich2 = bereich
        bereich2 = {}
        bereich2[f"Titellist"] = liste
        bereichdict[f"{bereich}"] = bereich2
    for stuff in bereichdict:
        print(stuff, "\n", bereichdict[stuff])
    return bereichdict

def choose_topics():
    pass

#Ich brauche mehr Plan denn ich habe kein Plan mehr

if __name__ == '__main__':
    jsonladen()
    choose_topics()
    dict_questiontitel()