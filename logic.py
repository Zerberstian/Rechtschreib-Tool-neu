#logic for Rechtschreib-Tool
import json

aufgabenListe = [] #Create an empty list for questions
bereichListe = [] #Create an empty list for topics

#Function to load aufgaben.json
def jsonladen():
    with open ("aufgaben_mit_ids.json","r",encoding= "utf-8" ) as f:
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
    if not type(bereich) == list:
        for titel in aufgabenListe:
            if bereich == titel['Uebungsbereich']:
                titels.append(titel['Titel'])
    else:
        for b in bereich:
            for titel in aufgabenListe:
                if b == titel['Uebungsbereich']:
                    titels.append(titel['Titel'])
    return titels

#Function to list all "Übungen" of a titel
def list_uebungen(titels):
    uebungen = []
    if not type(titels) == list:
        for uebung in aufgabenListe:
            if titels ==uebung['Titel']:
                uebungen.append(uebung['Uebungsbereich'])
    else:
        for titel in titels:
            for uebung in aufgabenListe:
                if titel == uebung['Titel']:
                    uebungen.append(uebung['UebungenListe'])
    return uebungen

if __name__ == '__main__':
    jsonladen()
    #dict_questiontitel()
    for a in list_uebungen(list_titels('Fremdworte')):
        print(list_uebungen(list_titels('Fremdworte')))
    '''
    for a in list_uebungen(list_titels(uebungsbereich_auflisten())):
        print(a)
        #for uid in a: print(uid['uid'])
    '''