from logic_der_zweite import *
from GUI.BereichCheckbox import *
import random

aufgaben_dict = {} # Objekte der Klasse Aufgabe werden hier gemerkt und die Uebung_id ist key
zu_loesende_aufgaben_list = []
falsche_antwort_dict = {}
boese_liste = []
gute_liste = []

class FalscheAntwort:
    def __init__(self, uebung_id, antwort, korrekte_antwort):
        self.uebung_id = uebung_id
        self.antwort = antwort
        self.korrekte_antwort = korrekte_antwort

        falsche_antwort_dict[self.uebung_id] = self

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
        return get_aufgabenbeschreibung(gekuerzte_uebung_id)

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
    antwort = int_input()
    aufgabe_beantworten(antwort, aufgabe, index)

def aufgabe_stellen(aufgabe):
    for index, entry in enumerate(aufgabe.moeglichkeiten):
        print(entry)

def aufgabe_beantworten(antwort, aufgabe, index):
    if antwort == aufgabe.korrekt:
        print("Die Antwort ist Richtig")
        richtige_merken(aufgabe)
    else:
        print("Die Antwort ist Falsch")
        falsche_merken(index, aufgabe, antwort)

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
    if aufgaben_picken(10):
        return
    for index, aufgabe in enumerate(zu_loesende_aufgaben_list):
        print(aufgabe)
        aufgabe_loesen(index, aufgaben_dict[aufgabe])
    print(len(gute_liste), " Richtige Antworten")
    for x in gute_liste:
        print(x)
    print(len(boese_liste), " Falschen Antworten")
    for antwort in falsche_antwort_dict:
        print("\nDie richtige Antwort ist: ", falsche_antwort_dict[antwort].korrekte_antwort)
        print("Du hast: ", falsche_antwort_dict[antwort].antwort , " ausgewählt")
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

def do_something_function_that_needs_a_better_name(aufgabe, antwort):
    try:
        return aufgabe.moeglichkeiten[antwort-1]
    except IndexError:
        return "Antwort außerhalb des gültigen Mengenbereiches"

def falsche_merken(index, aufgabe, antwort):
    FalscheAntwort(aufgabe.uebung_id,
                   do_something_function_that_needs_a_better_name(aufgabe,antwort),
                   aufgabe.moeglichkeiten[aufgabe.korrekt-1])
    if aufgabe.uebung_id not in boese_liste:
        boese_liste.append(aufgabe.uebung_id)
        falsche_antwort_rein_shuffeln(index, aufgabe.uebung_id)

def falsche_antwort_rein_shuffeln(index, aufgabe):
    try:
        random_index = random.randint(index + 3, len(zu_loesende_aufgaben_list))
        zu_loesende_aufgaben_list.insert(random_index, aufgabe)
    except ValueError:
        print("Der Index ist nicht gefund!")

if __name__ == "__main__":
    root = Tk()
    BereichCheckbox(root).create("#ffffff")
    start = Button(root, text="Start", command=button_start)
    start.pack()
    root.mainloop()