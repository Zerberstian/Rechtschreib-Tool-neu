import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from GUI.BereichCheckbox import *
from Programmlogik.json_laden_logik import *

aufgaben_dict: dict[str, "Aufgabe"] = {} # Contains "Uebung_id"s to load exercises
ausgewaehlte_aufgaben: list[str] = []
zu_loesende_aufgaben_list: list[str] = []
falsche_antwort_dict: dict[str, "FalscheAntwort"] = {}
falsch_beantwortet: list[str] = []
richtig_beantwortet: list[str] = []
korrigiert_beantwortet: list[str] = []

class Aufgabe:
    def __init__(self, uebung_id: str):
        self.__wiederholt = False
        self.uebung_id = uebung_id
        aufgabe = aufgabe_lesen(uebung_id)
        if aufgabe is None:
            raise ValueError(f"Aufgabe mit ID '{uebung_id}' nicht gefunden.")
        self.moeglichkeiten = aufgabe.moeglichkeiten
        self.korrekt = aufgabe.korrekte_antwort
        self.infotext = aufgabe.infotext
        self.uebungs_beschreibung = aufgabe.uebungs_beschreibung
        self.speziell = self.speziell_check()
        self.aufgabenbeschreibung = self.beschreibung()
        if self.speziell == "Speziell Satz":
            self.moeglichkeiten = self.moeglichkeiten.copy()[0].split()
        elif self.speziell == "Speziell Wort":
            self.moeglichkeiten = list(self.moeglichkeiten.copy()[0])
        aufgaben_dict[self.uebung_id] = self

    def beschreibung(self) -> str:
        gekuerzte_uebung_id: str = self.uebung_id.rsplit(".", 1)[0]
        return get_aufgabenbeschreibung(gekuerzte_uebung_id)

    def speziell_check(self) -> str:
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
        if not self.__wiederholt:
            self.__wiederholt = True
        else:
            self.__wiederholt = False

    def get_wiederholt(self):
        return self.__wiederholt

class FalscheAntwort:
    def __init__(self, uebung_id: str, antwort: str, korrekte_antwort: str, wiederholt: bool):
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
def aufgaben_picken(limit: int) -> bool:
    if not ausgewaehlte_aufgaben:
        print("Sie haben nichts ausgewählt!")
        return False
    x = 0
    while x < limit:
        uebung_id = random.choice(ausgewaehlte_aufgaben)
        if uebung_id not in zu_loesende_aufgaben_list:
            zu_loesende_aufgaben_list.append(uebung_id)
            print(zu_loesende_aufgaben_list[-1])
            x += 1
        elif len(zu_loesende_aufgaben_list) == len(list(aufgaben_dict.keys())):
            print("Alle Verfügbaren Aufgaben geladen.")
            break
    return True

def moeglichkeiten_listen(aufgabe: Aufgabe):
    for _, entry in enumerate(aufgabe.moeglichkeiten):
        print(entry)

def int_input() -> int:
    while True:
        try :
            antwort = input("Schreiben Sie die Zahl der richtigen Antwort.")
            return int(antwort)
        except ValueError:
            print("Die Antwort ist nicht gültig!")

def antwort_check(antwort: int, aufgabe: Aufgabe, index: int) -> bool:
    if aufgabe.get_wiederholt():
        if antwort == aufgabe.korrekt:
            print("\nDie Antwort wurde korrigiert.")
            korrigierte_merken(aufgabe)
            return True
        else:
            print("\nDie Antwort ist falsch.")
            falsch_merken(index, aufgabe, antwort)
            return False
    else:
        if antwort == aufgabe.korrekt:
            print("\nDie Antwort ist richtig.")
            richtig_merken(aufgabe)
            return True
        else:
            print("\nDie Antwort ist falsch.")
            falsch_merken(index, aufgabe, antwort)
            return False

def korrigierte_merken(aufgabe: Aufgabe):
    korrigiert_beantwortet.append(aufgabe.uebung_id)

def richtig_merken(aufgabe: Aufgabe):
    richtig_beantwortet.append(aufgabe.uebung_id)

def antwort_finden(aufgabe: Aufgabe, antwort: int) -> str:
    try:
        return aufgabe.moeglichkeiten[antwort-1]
    except IndexError:
        return "Antwort außerhalb des gültigen Mengenbereiches."

def falsch_merken(index: int, aufgabe: Aufgabe, antwort: int):
    FalscheAntwort(aufgabe.uebung_id,
                   antwort_finden(aufgabe,antwort),
                   aufgabe.moeglichkeiten[(aufgabe.korrekt-1)],
                   aufgabe.get_wiederholt())
    if aufgabe.uebung_id not in falsch_beantwortet:
        aufgabe.set_wiederholt()
        falsch_beantwortet.append(aufgabe.uebung_id)
        falsch_beantwortet_einfuegen(index, aufgabe.uebung_id)

# Inserts exercises that were  answered wrong at a random spot in "aufgaben_liste"
def falsch_beantwortet_einfuegen(index: int, aufgabe: str):
    try:
        random_index = random.randint(index + 3, len(zu_loesende_aufgaben_list))
        zu_loesende_aufgaben_list.insert(random_index, aufgabe)
    except ValueError:
        print("Der Index ist nicht gefunden!")

def aufgabe_bearbeiten_konsole(index: int, aufgabe: Aufgabe):
    if aufgabe.get_wiederholt():
        print("WIEDERHOLUNG_________!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! deutlich genug?")
    print(aufgabe.aufgabenbeschreibung, '\n')
    print(aufgabe.uebungs_beschreibung, "\n")
    moeglichkeiten_listen(aufgabe)
    antwort = int_input()
    antwort_check(antwort, aufgabe, index)

def aufgaben_obejekte_erstellen():
    for eintrag in list_uebungen(list_teilgebiet_titels(list_uebungsbereiche())):
        Aufgabe(eintrag)

def list_aktive_aufgaben():
    for eintrag in list_uebungen(get_active()):
        ausgewaehlte_aufgaben.append(eintrag)

def aufgaben_initialisieren(aufgaben_limit: int):
    list_aktive_aufgaben()
    if aufgaben_picken(aufgaben_limit):
        return

def aufgaben_anfangen_konsole():
    for index, aufgabe in enumerate(zu_loesende_aufgaben_list):
        print(aufgabe)
        aufgabe_bearbeiten_konsole(index, aufgaben_dict[aufgabe])

def statistik_ausgeben():
    """
    stats_der_richtigen()
    stats_der_falschen()
    stats_der_korrigierten()
    stats_gesamt()
    resetting()
    """
    return (stats_der_richtigen(),
            stats_der_falschen(),
            stats_der_korrigierten(),
            stats_gesamt())
            #,resetting())

def stats_gesamt() -> str:
    return(f"Aus {len(zu_loesende_aufgaben_list)} Aufgaben hast du "
           f"{len(richtig_beantwortet)} Richtig, "
           f"{len(falsch_beantwortet)
              + (len(zu_loesende_aufgaben_list)
                - len(richtig_beantwortet)
                - len(falsch_beantwortet)
                - len(korrigiert_beantwortet))}"
            f" Falsch und {len(korrigiert_beantwortet)} Korrigiert")

def stats_der_richtigen() -> list[str]:
    antworten_liste: list[str] = []
    print(len(richtig_beantwortet), " Richtige Antworten")
    for antwort in richtig_beantwortet:
        antworten_liste.append(antwort)
    return antworten_liste

def stats_der_falschen() -> list[str]:
    antworten_liste: list[str] = []
    print(len(falsch_beantwortet), " Falsche Antworten")
    for antwort in falsche_antwort_dict:
        antwort_stripped = antwort.strip("+")
        print(antwort_stripped)
        string_antwort = (f"{antwort_stripped}\n"
                          f"{aufgaben_dict[antwort_stripped].aufgabenbeschreibung}\n"
                          f"{aufgaben_dict[antwort_stripped].uebungs_beschreibung}\n"
                          f"Die richtige Antwort ist: "
                          f"{falsche_antwort_dict[antwort].korrekte_antwort}\n"
                          f"Du hast: {falsche_antwort_dict[antwort].antwort} ausgewählt\n\n")
        #print(string_antwort)
        antworten_liste.append(string_antwort)
    return antworten_liste

def stats_der_korrigierten() -> list[str]:
    antworten_liste: list[str] = []
    print(len(korrigiert_beantwortet), "Korrigiert")
    for antwort in korrigiert_beantwortet:
        #print(antwort)
        antworten_liste.append(antwort)
    return antworten_liste

def button_start():
    aufgaben_initialisieren(5)
    aufgaben_anfangen_konsole()
    statistik_ausgeben()

# Clears all dictionaries

def resetting():
    for eintrag in aufgaben_dict:
        aufgaben_dict[eintrag].set_wiederholt()
    ausgewaehlte_aufgaben.clear()
    zu_loesende_aufgaben_list.clear()
    falsch_beantwortet.clear()
    richtig_beantwortet.clear()
    korrigiert_beantwortet.clear()
    falsche_antwort_dict.clear()

aufgaben_obejekte_erstellen()

if __name__ == "__main__":
    root = Tk()
    #BereichCheckbox(root).create("#ffffff")
    start = Button(root, text="Start", command=button_start)
    start.pack()
    root.mainloop()