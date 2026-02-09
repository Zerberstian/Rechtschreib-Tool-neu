from logic_der_zweite import *
from GUI.BereichCheckbox import *
import random

aufgaben_dict = {} # Objekte der Klasse Aufgabe werden hier gemerkt und können mit der Uebung_id ist key
zu_loesende_aufgaben_list = []
boese_liste = []
gute_liste = []

'''
Hier sind eine paar Funktionen, welche ihren Sinn im laufe der Programmierung wieder verlieren.
'''

class Aufgabe:
    def __init__(self, uebung_id):
        self.uebung_id = uebung_id
        aufgabe = aufgabe_lesen(uebung_id)
        self.moeglichkeiten = aufgabe["Moeglichkeiten"]
        self.korrekt = aufgabe["KorrekteAntwort"]
        self.infotext = aufgabe["Infotext"]
        self.uebungs_beschreibung = aufgabe["UebungsBeschreibung"]
        self.spezial_type = self.spezial_check()
        self.aufgabenbeschreibung = self.aufgabenbeschreibung()

        aufgaben_dict[self.uebung_id] = self

    def aufgabenbeschreibung(self):
        gekuerzte_uebung_id = self.uebung_id.rsplit(".", 1)[0]
        return get_aufgaben_beschreibung(gekuerzte_uebung_id)

    def spezial_check(self):
        gekuerzte_uebung_id = self.uebung_id.rsplit(".", 1)[0]
        x = get_spezial_status(gekuerzte_uebung_id)
        if not x:
            return "Nicht Speziell"
        if len(self.moeglichkeiten[0].split()) == 1:
            return "Speziell Wort"
        else:
            return "Speziell Satz"
    def release_me(self):
        aufgaben_dict.pop(self.uebung_id)

def aufgabe_loesen(index, aufgabe):
    print(aufgabe.aufgabenbeschreibung, '\n')
    print(aufgabe.uebungs_beschreibung, "\n")
    aufgabe_stellen(aufgabe)
    if aufgabe_beantworten(int_input(), aufgabe):
        print("Die Antwort ist Richtig")
        richtige_merken(aufgabe)
    else:
        print("Die Antwort ist Falsch")
        falsche_merken(index, aufgabe)

def aufgabe_stellen(aufgabe):
    for index, entry in enumerate(aufgabe.moeglichkeiten):
        print(entry)

def aufgabe_beantworten(antwort, aufgabe):
    if antwort == aufgabe.korrekt:
        return True
    else:
        return False

def int_input():
    while True:
        try :
            ant = input("Schreiben Sie die Zahl der richtigen Antwort")
            return int(ant)
        except ValueError:
            print("Der Antwort ist nicht gefund!")

def akitve_aufgaben_objekte_erstellen():
    aktiv = get_active()
    for eintrag in list_uebungen(aktiv):
        Aufgabe(eintrag)

def button_start():
    aufgaben_initialisieren()

def aufgaben_initialisieren():
    akitve_aufgaben_objekte_erstellen()
    if aufgaben_picken(8):
        return
    for index, aufgabe in enumerate(zu_loesende_aufgaben_list):
        print(aufgabe)
        aufgabe_loesen(index, aufgaben_dict[aufgabe])
    print(len(gute_liste), " Richtige Antworten")
    print(len(boese_liste), " Falschen Antworten")
    resetting()

def resetting():
    aufgaben_dict.clear()
    zu_loesende_aufgaben_list.clear()
    boese_liste.clear()
    gute_liste.clear()

def aufgaben_picken(limit):
    if aufgaben_dict == {}:
        return False, print("Das Dict ist Leer. Haben Sie nichts ausgewählt?")
    x = 0
    while x < limit:
        uebung_id = random.choice(list(aufgaben_dict.keys()))
        if uebung_id not in zu_loesende_aufgaben_list:
            zu_loesende_aufgaben_list.append(uebung_id)
            print(zu_loesende_aufgaben_list[-1])
        elif len(zu_loesende_aufgaben_list) == len(list(aufgaben_dict.keys())):
            print("Alle Verfügbaren Aufgaben geloaden")
            break
        x += 1
    return None

def richtige_merken(aufgabe):
    gute_liste.append(aufgabe.uebung_id)

def falsche_merken(index, aufgabe):
    boese_liste.append(aufgabe.uebung_id)
    if aufgabe.uebung_id in boese_liste:
        falsche_antwort_rein_shuffeln(index, aufgabe.uebung_id)

def falsche_antwort_rein_shuffeln(index, aufgabe):
    try:
        random_index = random.randint(index + 3, len(zu_loesende_aufgaben_list) - index)
        zu_loesende_aufgaben_list.insert(random_index, aufgabe)
    except ValueError:
        print("Der Index ist nicht gefund!")

if __name__ == "__main__":
    root = Tk()
    BereichCheckbox(root).create("#ffffff")
    start = Button(root, text="Start", command=button_start)
    start.pack()
    #reset = Button(root, text="Reset", command=resetting )
    #reset.pack()
    root.mainloop()

'''
Es fehlt noch das die "Auswahl" entfernt wird falls man noch mal Übungen machen will.
Zur Zeit muss man neustarten um eine neue Auswahl in der Checkbox zu machen.
eg wenn man zurück geht sollen alle Aufgaben Objekte vergessen werden. 
'''