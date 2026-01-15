#logic for Rechtschreib-Tool
import json

aufgabenListe = [] #Create an empty list for questions
bereichListe = [] #Create an empty list for topics

#Function to load aufgaben.json
def jsonladen():
    with open ("aufgaben.json","r",encoding= "utf-8" ) as f:
        global aufgabenListe
        aufgabenListe = json.load(f)

#Function to list all titel
def aufgaben_titel_auflisten():
    for aufgaben in aufgabenListe:
        print(f"Aufgabe:{aufgaben["Titel"]}")

#Function to list all titel with description
def aufgaben_auflisten():
    for aufgaben in aufgabenListe:
        print(f"Aufgabe: {aufgaben['Titel']} \nAufgabenbeschreibung: {aufgaben['_aufgabenbeschreibung']} \nAufgabenbeschreibung: {aufgaben['Aufgabenbeschreibung']} ")

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

#Function to choose Übungsbereich
def uebungsbereich_auswahl():
    while True:
        uebungsbereichListe = uebungsbereich_auflisten()
        auswahl =int(input("1, 2, 3, 4, 5 oder 6?"))
        auswahl-=1
        if auswahl < 6 and auswahl >= 0:
            uebungsbereich = uebungsbereichListe[auswahl]
            print(uebungsbereich)
            if uebungsbereich not in bereichListe:
                bereichListe.append(uebungsbereich)
            else:
                print("Bereits ausgewählt")
            break
        else:
            print("Ungültiger Bereich")
    while True:
        nochmal = input("Noch ein Übungsbereich auswählen? Y/N\n")
        if nochmal.lower() == "y" :
            uebungsbereich_auswahl()
        elif nochmal.lower() == "n":
            break
        else:
            print('You Stupid')
    print(f"Die Ausgewählten Übungsbereiche sind {bereichListe}")

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
    return(uebungsbereichListe)

#Function to list all Questiontitel based on chosen Übungsbereichen
def list_questiontitel():
    for bereich in uebungsbereich_auflisten():
        print(bereich)
        for aufgaben in aufgabenListe:
            if bereich == aufgaben['Uebungsbereich']:
                print(aufgaben['Titel'])



if __name__ == '__main__':

    jsonladen()
    #aufgaben_titel_auflisten()
    #aufgaben_auflisten()
    #aufgabe_open()
    #spezial_aufgaben()
    #uebungsbereich_auflisten()
    #uebungsbereich_auswahl()
    list_questiontitel()