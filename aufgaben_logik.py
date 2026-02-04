from logic2 import *

aufgaben_dict = {}

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

        aufgaben_dict[self.uebung_id] = self

    def aufgabenbeschreibung(self):
        gekuerzte_uebung_id = self.uebung_id.rsplit(".", 1)[0]
        return get_aufgaben_beschreibung(gekuerzte_uebung_id)

    def spezial_check(self):
        gekuerzte_uebung_id = self.uebung_id.rsplit(".", 1)[0]
        x = get_spezial_status(gekuerzte_uebung_id)
        print(x)
        if not x:
            return x
        if len(self.moeglichkeiten[0].split()) == 1:
            print("Das ist ein Wort")
        else:
            print("Das ist ein Satz")
        return x

def aufgabe_aufgabieren(aufgabe):
    print(aufgabe.aufgabenbeschreibung, '\n')
    print(aufgabe.uebungs_beschreibung, "\n")
    aufgabe_stellen(aufgabe)
    if aufgabe_beantworten(int(input("Schreiben Sie die Zahl der richtigen Antwort")), aufgabe):
        print("Richtig")
    else:
        print("Falsch")

def aufgabe_stellen(aufgabe):
    for index, entry in enumerate(aufgabe.moeglichkeiten):
        print(entry)

def aufgabe_beantworten(antwort, aufgabe):
    if antwort == aufgabe.korrekt:
        return True
    else:
        return False


if __name__ == "__main__":
    Aufgabe("5.5.69")
    aufgabe_aufgabieren(aufgaben_dict["5.5.69"])
    Aufgabe("5.3.99")
    aufgabe_aufgabieren(aufgaben_dict["5.3.99"])
    Aufgabe("1.1.1")
    aufgabe_aufgabieren(aufgaben_dict["1.1.1"])