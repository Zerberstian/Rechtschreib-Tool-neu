import json
import os

geladeneAufgaben = [] #Create an empty list for questions

# Function to load aufgaben.json
def jsonladen():
    with open(os.path.join(os.path.dirname(__file__), "aufgaben_mit_ids.json"), "r", encoding="utf-8") as f:
        global geladeneAufgaben
        geladeneAufgaben = json.load(f)

# Function to list every "Uebungsbereich"
def list_uebungsbereiche():
    uebungsbereich_liste = []
    for uebungsbereich in geladeneAufgaben['data']:
        if uebungsbereich['Uebungsbereich'] not in uebungsbereich_liste:
            uebungsbereich_liste.append(uebungsbereich['Uebungsbereich'])
    return uebungsbereich_liste

# Function to list every "Teilgebiet" of an "Uebungsbereich"
def list_titels(bereich):
    titels = []
    if not type(bereich) == list:
        for alle_bereiche in geladeneAufgaben['data']:
            if bereich == alle_bereiche['Uebungsbereich']:
                for titel in alle_bereiche['Teilgebiet']:
                    titels.append(titel['Titel'])
    else:
        for alle_bereiche in bereich:
            for uebungsbereiche in geladeneAufgaben['data']:
                if alle_bereiche == uebungsbereiche['Uebungsbereich']:
                    for titel in uebungsbereiche['Teilgebiet']:
                        titels.append(titel['Titel'])
    return titels

# Function to list "UebungenListe" of a "Teilgebiet"
def list_uebungen(titels):
    aufgaben_liste = []
    if not type(titels) == list:
        for bereich in geladeneAufgaben['data']:
            for teilgebiet in bereich['Teilgebiet']:
                if titels == teilgebiet['Titel']:
                    for uebung in teilgebiet['UebungenListe']:
                        aufgaben_liste.append(uebung["Uebung_id"])
    else:
        for titel in titels:
            for bereich in geladeneAufgaben['data']:
                for teilgebiet in bereich['Teilgebiet']:
                    if titel == teilgebiet['Titel']:
                        for uebung in teilgebiet['UebungenListe']:
                            aufgaben_liste.append(uebung["Uebung_id"])
    print(len(aufgaben_liste), "= len(aufgaben_liste)")
    return aufgaben_liste

def aufgabe_lesen(aufgaben_id):
    for bereich in geladeneAufgaben['data']:
        for teilgebiet in bereich['Teilgebiet']:
            for aufgabe in teilgebiet['UebungenListe']:
                if aufgaben_id == aufgabe["Uebung_id"]:
                    return aufgabe

def get_spezial_status(teilgebiet_id):
    for bereich in geladeneAufgaben['data']:
        for teilgebiet in bereich['Teilgebiet']:
            if teilgebiet_id == teilgebiet['Teilgebiet_id']:
                return teilgebiet['IstSpeziell']

def get_aufgabenbeschreibung(teilgebiet_id):
    for bereich in geladeneAufgaben['data']:
        for teilgebiet in bereich['Teilgebiet']:
            if teilgebiet_id == teilgebiet['Teilgebiet_id']:
                return teilgebiet['Aufgabenbeschreibung']

jsonladen()
