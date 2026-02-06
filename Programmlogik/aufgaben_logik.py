from logic2 import *
from GUI.BereichCheckbox import *
import random

aufgaben_dict_ausgewahlt = {} # Objekte der Klasse Aufgabe werden hier gemerkt und können mit der Uebung_id ist key
zuloesende_aufgaben_dict = {} # ^ diese sind aber die, welche noch beantwortet werden müssen
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
        self.fremdwort = aufgabe["Fremdwort"]
        self.uebungs_beschreibung = aufgabe["UebungsBeschreibung"]
        self.spezial_type = self.spezial_check()
        self.aufgabenbeschreibung = self.aufgabenbeschreibung()

        aufgaben_dict_ausgewahlt[self.uebung_id] = self

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
        aufgaben_dict_ausgewahlt.pop(self.uebung_id)

def aufgabe_loesen(aufgabe):
    print(aufgabe.aufgabenbeschreibung, '\n')
    print(aufgabe.uebungs_beschreibung, "\n")
    aufgabe_stellen(aufgabe)
    if aufgabe_beantworten(int_input(), aufgabe):
        print("Die Antwort ist Richtig")
        richtige_merken(aufgabe)
    else:
        print("Die Antwort ist Falsch")
        falsche_merken(aufgabe)

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


def do_stuff():
    akitve_aufgaben_objekte_erstellen()
    aufgaben_picken(5)
    for aufgabe in zuloesende_aufgaben_dict:
        print(aufgabe)
        aufgabe_loesen(zuloesende_aufgaben_dict[aufgabe])
    print(len(gute_liste), " Richtige Antworten")
    print(len(boese_liste), " Falschen Antworten")

def temp_do_stuff():
    for aufgabe in aufgaben_dict_ausgewahlt.copy():
        print(aufgabe)
        aufgaben_dict_ausgewahlt[aufgabe].release_me()

def aufgaben_picken(limit):
    if aufgaben_dict_ausgewahlt == {}:
        return print("Das Dict ist Leer. Haben Sie nichts ausgewählt?")
    x = 0
    list_test = []
    while x < limit:
        test = random.choice(list(aufgaben_dict_ausgewahlt.keys()))
        if test not in list_test:
            list_test.append(test)
            zuloesende_aufgaben_dict[test] = aufgaben_dict_ausgewahlt[test]
            print(zuloesende_aufgaben_dict[test].uebung_id)
        elif len(list_test) == len(list(aufgaben_dict_ausgewahlt.keys())):
            print("Alle Verfügbaren Aufgaben geloaden")
            break
        x += 1
    return None

def neu_aufgabe_random_wieder_ins_dictionary(neue_aufgabe):
    pass

def richtige_merken(aufgabe):
    gute_liste.append(aufgabe.uebung_id)

def falsche_merken(aufgabe):
    boese_liste.append(aufgabe.uebung_id)

if __name__ == "__main__":
    root = Tk()
    BereichCheckbox(root).create("#ffffff")
    start = Button(root, text="Start", command=do_stuff)
    start.pack()
    reset = Button(root, text="Reset", command=temp_do_stuff)
    reset.pack()
    root.mainloop()

'''
Es fehlt noch das die "Auswahl" entfernt wird falls man noch mal Übungen machen will.
Zur Zeit muss man neustarten um eine neue Auswahl in der Checkbox zu machen.
eg wenn man zurück geht sollen alle Aufgaben Objekte vergessen werden. 
'''