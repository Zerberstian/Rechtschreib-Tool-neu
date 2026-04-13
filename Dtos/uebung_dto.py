from typing import Any

class UebungDto:
    def __init__(self,
                 moeglichkeiten: list[str],
                 korrekte_antwort: int,
                 infotext: str | None,
                 uebungs_beschreibung: str,
                 uebung_id: str):
        self.moeglichkeiten: list[str] = moeglichkeiten
        self.korrekte_antwort: int = korrekte_antwort
        self.infotext: str | None = infotext
        self.uebungs_beschreibung: str = uebungs_beschreibung
        self.uebung_id: str = uebung_id

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "UebungDto":
        return UebungDto(
            moeglichkeiten=data["moeglichkeiten"],
            korrekte_antwort=data["korrekte_antwort"],
            infotext=data.get("infotext"),
            uebungs_beschreibung=data["uebungs_beschreibung"],
            uebung_id=data["uebung_id"]
        )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "moeglichkeiten": self.moeglichkeiten,
            "korrekte_antwort": self.korrekte_antwort,
            "infotext": self.infotext,
            "uebungs_beschreibung": self.uebungs_beschreibung,
            "uebung_id": self.uebung_id
        }