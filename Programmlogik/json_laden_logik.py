import json
import os
from Dtos import *

aufgabenkatalog: CatalogueDto

# Function to load aufgaben.json
def jsonladen() -> None:
    with open(os.path.join(os.path.dirname(__file__), "json_cache.json"), "r", encoding="utf-8") as f:
        global aufgabenkatalog
        raw = json.load(f)
        aufgabenkatalog = CatalogueDto.from_dict(raw)

# Function to list every "Uebungsbereich"
def list_uebungsbereiche() -> list[str]:
    uebungsbereich_liste: list[str] = []
    for uebungsbereich in aufgabenkatalog.fields if aufgabenkatalog.fields else []:
        if uebungsbereich.title not in uebungsbereich_liste:
            uebungsbereich_liste.append(uebungsbereich.title)
    return uebungsbereich_liste

# Function to list every "Teilgebiet" of an "Uebungsbereich"
def list_teilgebiet_titels(bereich_input: str | list[str]) -> list[str]:
    titels: list[str] = []
    bereiche = bereich_input if isinstance(bereich_input, list) else [bereich_input]

    if not aufgabenkatalog.fields:
        return titels
    
    for bereich in bereiche:
        for uebungsbereiche in aufgabenkatalog.fields:
            if bereich == uebungsbereiche.title:
                if uebungsbereiche.subfields:
                    titels.extend(tg.title for tg in uebungsbereiche.subfields)
    return titels

# Function to list "UebungenListe" of a "Teilgebiet"
def list_uebungen(teilgebiet_titels: str | list[str]) -> list[str]:
    aufgaben_liste: list[str] = []
    titels = teilgebiet_titels if isinstance(teilgebiet_titels, list) else [teilgebiet_titels]

    if not aufgabenkatalog.fields:
        return aufgaben_liste

    for titel in titels:
        for bereich in aufgabenkatalog.fields:
            if not bereich.subfields:
                continue
            for teilgebiet in bereich.subfields:
                if titel == teilgebiet.title:
                    if not teilgebiet.tasks:
                        continue
                    aufgaben_liste.extend(u.task_id for u in teilgebiet.tasks)

    print(len(aufgaben_liste), "= len(aufgaben_liste)")
    return aufgaben_liste

def aufgabe_lesen(uebung_id: str) -> TaskDto | None:
    if not aufgabenkatalog.fields:
        return None
    for bereich in aufgabenkatalog.fields:
        if not bereich.subfields:
            continue
        for teilgebiet in bereich.subfields:
            if not teilgebiet.tasks:
                continue
            for aufgabe in teilgebiet.tasks:
                if uebung_id == aufgabe.task_id:
                    return aufgabe
    return None

def get_spezial_status(teilgebiet_id: str) -> bool:
    if not aufgabenkatalog.fields:
        return False
    for bereich in aufgabenkatalog.fields:
        if not bereich.subfields:
            continue
        for teilgebiet in bereich.subfields:
            if teilgebiet_id == teilgebiet.subfield_id:
                return teilgebiet.is_special
    return False


def get_aufgabenbeschreibung(teilgebiet_id: str) -> str:
    if not aufgabenkatalog.fields:
        return ""
    for bereich in aufgabenkatalog.fields:
        if not bereich.subfields:
            continue
        for teilgebiet in bereich.subfields:
            if teilgebiet_id == teilgebiet.subfield_id:
                return teilgebiet.task_description
    return ""
