from typing import Any
from Dtos.uebung_dto import UebungDto

class TeilgebietDto:
    def __init__(self,
                 titel: str,
                 aufgabenbeschreibung: str,
                 uebungsliste: list[UebungDto],
                 ist_speziell: bool,
                 is_checked: bool,
                 expanded: bool,
                 teilgebiet_id: str):
        self.titel = titel
        self.aufgabenbeschreibung = aufgabenbeschreibung
        self.uebungsliste = uebungsliste
        self.ist_speziell = ist_speziell
        self.is_checked = is_checked
        self.expanded = expanded
        self.teilgebiet_id = teilgebiet_id

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "TeilgebietDto":
        uebungsliste: list[Any] | dict[str, Any] = data.get("UebungenListe", [])

        if not isinstance(uebungsliste, list):
            uebungsliste = [uebungsliste]

        return TeilgebietDto(
            titel=data.get("Titel", ""),
            aufgabenbeschreibung=data.get("Aufgabenbeschreibung", ""),
            ist_speziell=data.get("IstSpeziell", False),
            is_checked=data.get("IsChecked", False),
            expanded=data.get("Expanded", False),
            teilgebiet_id=data.get("Teilgebiet_id", ""),
            uebungsliste=[UebungDto.from_dict(i)
                          for i in uebungsliste]
                          if uebungsliste
                          else []
        )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "Titel": self.titel,
            "Aufgabenbeschreibung": self.aufgabenbeschreibung,
            "IstSpeziell": self.ist_speziell,
            "IsChecked": self.is_checked,
            "Expanded": self.expanded,
            "Teilgebiet_id": self.teilgebiet_id,
            "UebungenListe": [i.to_dict()
                              for i in self.uebungsliste]
                              if self.uebungsliste
                              else None
        }
    
    @staticmethod
    def create_empty():
        return TeilgebietDto(
            titel="",
            aufgabenbeschreibung="",
            uebungsliste=[],
            ist_speziell=False,
            is_checked=False,
            expanded=False,
            teilgebiet_id=""
        )