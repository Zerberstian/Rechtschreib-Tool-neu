import sys
import os
from logic_der_zweite import *
import random
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from GUI.BereichCheckbox import *
from GUI.GUI_new import spinbox


aufgaben_dict = {} # Contains "Uebung_id"s to load exercises
zu_loesende_aufgaben_list = []
falsche_antwort_dict = {}
falsch_beantwortet = []
richtig_beantwortet = []
korrigiert_beantwortet = []

class Aufgabe:
    def __init__(self, uebung_id):
        self.__wiederholt = False
        self.uebung_id = uebung_id
        aufgabe = aufgabe_lesen(uebung_id)
        self.moeglichkeiten = aufgabe["Moeglichkeiten"]
        self.korrekt = aufgabe["KorrekteAntwort"]
        self.infotext = aufgabe["Infotext"]
        self.uebungs_beschreibung = aufgabe["UebungsBeschreibung"]
        self.speziell = self.speziell_check()
        self.aufgabenbeschreibung = self.aufgabenbeschreibung()
        if self.speziell == "Speziell Satz":
            self.moeglichkeiten = self.moeglichkeiten.copy()[0].split()
        elif self.speziell == "Speziell Wort":
            self.moeglichkeiten = list(self.moeglichkeiten.copy()[0])
        aufgaben_dict[self.uebung_id] = self

    def aufgabenbeschreibung(self):
        gekuerzte_uebung_id = self.uebung_id.rsplit(".", 1)[0]
        return get_aufgabenbeschreibung(gekuerzte_uebung_id)

    def speziell_check(self):
        gekuerzte_uebung_id = self.uebung_id.rsplit(".", 1)[0]
        speziell = get_spezial_status(gekuerzte_uebung_id)
        if not speziell:
            return "Nicht Speziell"
        if len(self.moeglichkeiten[0].split()) == 1:
            return "Speziell Wort"
        else:
            return "Speziell Satz"

# Skulldunno warum ich das Privat gemacht habe
    def set_wiederholt(self):
        self.__wiederholt = True

    def get_wiederholt(self):
        return self.__wiederholt

class FalscheAntwort:
    def __init__(self, uebung_id, antwort, korrekte_antwort, wiederholt):
        self.__wiederholt = wiederholt
        if not self.__wiederholt:
            self.uebung_id = uebung_id
        else:
            self.uebung_id = uebung_id + "+"
        self.antwort = antwort
        self.korrekte_antwort = korrekte_antwort

        falsche_antwort_dict[self.uebung_id] = self

    def get_wiederholt(self):
        return self.__wiederholt
# Randomly picks exercises from chosen "Teilgebiet" until limit is reached
def aufgaben_picken(limit):
    if aufgaben_dict == {}:
        return False, print("Das Dict ist Leer. Haben Sie nichts ausgewählt?")
    x = 0
    while x < limit:
        uebung_id = random.choice(list(aufgaben_dict.keys()))
        if uebung_id not in zu_loesende_aufgaben_list:
            zu_loesende_aufgaben_list.append(uebung_id)
            print(zu_loesende_aufgaben_list[-1])
            x += 1
        elif len(zu_loesende_aufgaben_list) == len(list(aufgaben_dict.keys())):
            print("Alle Verfügbaren Aufgaben geladen")
            break
    return None

def moeglichkeiten_listen(aufgabe):
    for index, entry in enumerate(aufgabe.moeglichkeiten):
        print(entry)

def int_input():
    while True:
        try :
            antwort = input("Schreiben Sie die Zahl der richtigen Antwort")
            return int(antwort)
        except ValueError:
            print("Die Antwort ist nicht gültig!")

def antwort_check(antwort, aufgabe, index):
    if aufgabe.get_wiederholt():
        if antwort == aufgabe.korrekt:
            print("\nDie Antwort wurde korrigiert")
            korrigierte_merken(aufgabe)
        else:
            print("\nDie Antwort ist falsch.")
            falsch_merken(index, aufgabe, antwort)
    else:
        if antwort == aufgabe.korrekt:
            print("\nDie Antwort ist richtig.")
            richtig_merken(aufgabe)
        else:
            print("\nDie Antwort ist falsch.")
            falsch_merken(index, aufgabe, antwort)

def korrigierte_merken(aufgabe):
    korrigiert_beantwortet.append(aufgabe.uebung_id)

def richtig_merken(aufgabe):
    richtig_beantwortet.append(aufgabe.uebung_id)

def antwort_finden(aufgabe, antwort):
    try:
        return aufgabe.moeglichkeiten[antwort-1]
    except IndexError:
        return "Antwort außerhalb des gültigen Mengenbereiches"

def falsch_merken(index, aufgabe, antwort):
    FalscheAntwort(aufgabe.uebung_id,
                   antwort_finden(aufgabe,antwort),
                   aufgabe.moeglichkeiten[(aufgabe.korrekt-1)],
                   aufgabe.get_wiederholt())
    if aufgabe.uebung_id not in falsch_beantwortet:
        aufgabe.set_wiederholt()
        falsch_beantwortet.append(aufgabe.uebung_id)
        falsch_beantwortet_einfuegen(index, aufgabe.uebung_id)

# Inserts exercises that were  answered wrong at a random spot in "aufgaben_liste"
def falsch_beantwortet_einfuegen(index, aufgabe):
    try:
        random_index = random.randint(index + 3, len(zu_loesende_aufgaben_list))
        zu_loesende_aufgaben_list.insert(random_index, aufgabe)
    except ValueError:
        print("Der Index ist nicht gefunden!")

def aufgabe_bearbeiten(index, aufgabe):
    if aufgabe.get_wiederholt():
        print("WIEDERHOLUNG_________!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! deutlich genug?")
    print(aufgabe.aufgabenbeschreibung, '\n')
    print(aufgabe.uebungs_beschreibung, "\n")
    moeglichkeiten_listen(aufgabe)
    antwort = int_input()
    antwort_check(antwort, aufgabe, index)

def akitve_aufgaben_objekte_erstellen():
    aktiv = get_active()
    for eintrag in list_uebungen(aktiv):
        Aufgabe(eintrag)

def aufgaben_initialisieren():
    akitve_aufgaben_objekte_erstellen()
    if aufgaben_picken(int(spinbox.get())):
        return
    for index, aufgabe in enumerate(zu_loesende_aufgaben_list):
        print(aufgabe)
        aufgabe_bearbeiten(index, aufgaben_dict[aufgabe])

def statistik_ausgeben():
    stats_der_richtigen()
    stats_der_falschen()
    stats_der_korrigierten()
    print(f"Aus {len(zu_loesende_aufgaben_list)} Aufgaben hast du "
          f"{len(richtig_beantwortet)} Richtig, "
          f"{len(falsch_beantwortet) + (len(zu_loesende_aufgaben_list) - len(richtig_beantwortet) - len(falsch_beantwortet) - len(korrigiert_beantwortet))} Falsch und "
          f"{len(korrigiert_beantwortet)} Korrigiert")
    resetting()

def stats_der_richtigen():
    print(len(richtig_beantwortet), " Richtige Antworten")
    for x in richtig_beantwortet:
        print(x)

def stats_der_falschen():
    print(len(falsch_beantwortet), " Falsche Antworten")
    for antwort in falsche_antwort_dict:
        antwort = antwort.strip("+")
        print(antwort, '\n')
        print(aufgaben_dict[antwort].aufgabenbeschreibung, '\n')
        print(aufgaben_dict[antwort].uebungs_beschreibung, "\n")
        print("Die richtige Antwort ist: ", falsche_antwort_dict[antwort].korrekte_antwort)
        print("Du hast: ", falsche_antwort_dict[antwort].antwort , " ausgewählt")

def stats_der_korrigierten():
    print(len(korrigiert_beantwortet), "Korrigiert")
    for x in korrigiert_beantwortet:
        print(x)

def button_start():
    aufgaben_initialisieren()
    statistik_ausgeben()

# Clears all dictionaries
def resetting():
    aufgaben_dict.clear()
    zu_loesende_aufgaben_list.clear()
    falsch_beantwortet.clear()
    richtig_beantwortet.clear()
    korrigiert_beantwortet.clear()
    falsche_antwort_dict.clear()

if __name__ == "__main__":
    root = Tk()
    #BereichCheckbox(root).create("#ffffff")
    start = Button(root, text="Start", command=button_start)
    start.pack()
    root.mainloop()