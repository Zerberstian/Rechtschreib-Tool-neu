from typing import Any

class UebungDto:
    def __init__(self,
                 moeglichkeiten: list[str],
                 korrekte_antwort: int,
                 infotext: str | None,
                 uebungs_beschreibung: str,
                 uebung_id: str):
        self.moeglichkeiten = moeglichkeiten
        self.korrekte_antwort = korrekte_antwort
        self.infotext = infotext
        self.uebungs_beschreibung = uebungs_beschreibung
        self.uebung_id = uebung_id

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "UebungDto":
        return UebungDto(
            moeglichkeiten=data.get("Moeglichkeiten", []),
            korrekte_antwort=data.get("KorrekteAntwort", 0),
            infotext=data.get("Infotext", None),
            uebungs_beschreibung=data.get("UebungsBeschreibung", ""),
            uebung_id=data.get("Uebung_id", "")
        )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "Moeglichkeiten": self.moeglichkeiten,
            "Korrekte_antwort": self.korrekte_antwort,
            "Infotext": self.infotext,
            "UebungsBeschreibung": self.uebungs_beschreibung,
            "Uebung_id": self.uebung_id
        }
    
    @staticmethod
    def create_empty():
        return UebungDto(
            moeglichkeiten=[],
            korrekte_antwort=0,
            infotext=None,
            uebungs_beschreibung="",
            uebung_id=""
        )