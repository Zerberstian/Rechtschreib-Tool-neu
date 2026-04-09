import json
import os
from Dtos.aufgabenkatalog_dto import AufgabenkatalogDto
from Dtos.uebung_dto import UebungDto

aufgabenkatalog: AufgabenkatalogDto

# Function to load aufgaben.json
def jsonladen() -> None:
    with open(os.path.join(os.path.dirname(__file__), "json_cache.json"), "r", encoding="utf-8") as f:
        global aufgabenkatalog
        raw = json.load(f)
        aufgabenkatalog = AufgabenkatalogDto.from_dict(raw)

# Function to list every "Uebungsbereich"
def list_uebungsbereiche() -> list[str]:
    uebungsbereich_liste: list[str] = []
    for uebungsbereich in aufgabenkatalog.data:
        if uebungsbereich.uebungsbereich not in uebungsbereich_liste:
            uebungsbereich_liste.append(uebungsbereich.uebungsbereich)
    return uebungsbereich_liste

# Function to list every "Teilgebiet" of an "Uebungsbereich"
def list_teilgebiet_titels(bereich_input: str | list[str]) -> list[str]:
    titels: list[str] = []
    bereiche = bereich_input if type(bereich_input) == list else [bereich_input]

    for bereich in bereiche:
        for uebungsbereiche in aufgabenkatalog.data:
            if bereich == uebungsbereiche.uebungsbereich:
                titels.extend(tg.titel for tg in uebungsbereiche.teilgebiete)
    return titels

# Function to list "UebungenListe" of a "Teilgebiet"
def list_uebungen(teilgebiet_titels: str | list[str]) -> list[str]:
    aufgaben_liste: list[str] = []
    titels = teilgebiet_titels if type(teilgebiet_titels) == list else [teilgebiet_titels]

    for titel in titels:
        for bereich in aufgabenkatalog.data:
            for teilgebiet in bereich.teilgebiete:
                if titel == teilgebiet.titel:
                    aufgaben_liste.extend(u.uebung_id for u in teilgebiet.uebungsliste)

    print(len(aufgaben_liste), "= len(aufgaben_liste)")
    return aufgaben_liste

def aufgabe_lesen(uebung_id: str) -> UebungDto | None:
    for bereich in aufgabenkatalog.data:
        for teilgebiet in bereich.teilgebiete:
            for aufgabe in teilgebiet.uebungsliste:
                if uebung_id == aufgabe.uebung_id:
                    return aufgabe
    return None

def get_spezial_status(teilgebiet_id: str) -> bool:
    for bereich in aufgabenkatalog.data:
        for teilgebiet in bereich.teilgebiete:
            if teilgebiet_id == teilgebiet.teilgebiet_id:
                return teilgebiet.ist_speziell
    return False


def get_aufgabenbeschreibung(teilgebiet_id: str) -> str:
    for bereich in aufgabenkatalog.data:
        for teilgebiet in bereich.teilgebiete:
            if teilgebiet_id == teilgebiet.teilgebiet_id:
                return teilgebiet.aufgabenbeschreibung
    return ""

jsonladen()
