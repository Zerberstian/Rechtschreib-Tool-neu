from logic2 import *
from BereichCheckbox import *
import random

aufgaben_dict_ausgewahlt = {} # Objekte der Klasse Aufgabe werden hier gemerkt und können mit der Uebung_id ist key
zuloesende_aufgaben_dict = {} # ^ diese sind aber die, welche noch beantwortet werden müssen


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
            return x
        print("Diese Aufgabe ist \"Speziell\"")
        if len(self.moeglichkeiten[0].split()) == 1:
            print("Das ist ein Wort")
        else:
            print("Das ist ein Satz")
        return x

def aufgabe_aufgabieren(aufgabe):
    print(aufgabe.aufgabenbeschreibung, '\n')
    print(aufgabe.uebungs_beschreibung, "\n")
    aufgabe_stellen(aufgabe)
    if aufgabe_beantworten(int_input(), aufgabe):
        print("Die Antwort ist Richtig")
    else:
        print("Die Antwort ist Falsch")

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

def alle_aufgaben_objekte():
    for index, aufgabe in enumerate(aufgaben_dict_ausgewahlt):
        print(aufgaben_dict_ausgewahlt[aufgabe].moeglichkeiten)

def do_stuff():
    akitve_aufgaben_objekte_erstellen()
    aufgaben_picken(20)
    #alle_aufgaben_objekte()

def aufgaben_picken(limit):
    x = 0
    while x < limit:
        x += 1
        test = random.choice(list(aufgaben_dict_ausgewahlt.keys()))
        print(test)
        pass

if __name__ == "__main__":
    root = Tk()
    BereichCheckbox(root).create("#ffffff")
    asdasdasd = Button(root, text="Test", command=do_stuff)
    asdasdasd.pack()
    root.mainloop()