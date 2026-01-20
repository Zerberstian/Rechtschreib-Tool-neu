#logic for Rechtschreib-Tool
import json

aufgabenListe = [] #Create an empty list for questions
bereichListe = [] #Create an empty list for topics

#Function to load aufgaben.json
def jsonladen():
    with open ("aufgaben.json","r",encoding= "utf-8" ) as f:
        global aufgabenListe
        aufgabenListe = json.load(f)

#Function to list all "uebungsbereich"
def uebungsbereich_auflisten():
    uebungsbereich_liste = []
    for uebungsbereich in aufgabenListe:
        if uebungsbereich['Uebungsbereich'] not in uebungsbereich_liste:
            uebungsbereich_liste.append(uebungsbereich['Uebungsbereich'])
    return uebungsbereich_liste

#Function to list all titels of a bereich
def list_titels(bereich):
    titels = []
    for titel in aufgabenListe:
        if bereich == titel['Uebungsbereich']:
            titels.append(titel['Titel'])
    return titels

#Function to list all topics with their respective titels and adds a IsChecked Status to the list
def dict_questiontitel():
    bereichdict = {}
    for bereich in uebungsbereich_auflisten():
        titeldict = {}
        for titel in aufgabenListe:
            if bereich == titel['Uebungsbereich']:
                titel2 = {}
                titel2["IsChecked"] = False
                #titel2["Questionlist"] = Questiondict
                titeldict[f"{titel["Titel"]}"] = titel2
        bereich2 = {}
        bereich2["IsChecked"] = False
        bereich2["Titellist"] = titeldict
        bereichdict[f"{bereich}"] = bereich2
    for stuff in bereichdict:
        print(stuff, "\n", bereichdict[stuff])
    return bereichdict


#Ich brauche mehr Plan denn ich habe kein Plan mehr

if __name__ == '__main__':
    jsonladen()
    #dict_questiontitel()
    print(list_titels(uebungsbereich_auflisten()))