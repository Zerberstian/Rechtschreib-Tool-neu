from typing import Any
from Dtos.uebung_dto import UebungDto

class TeilgebietDto:
    def __init__(self,
                 titel: str,
                 aufgabenbeschreibung: str,
                 uebungsliste: list[UebungDto] | None,
                 ist_speziell: bool,
                 is_checked: bool,
                 expanded: bool,
                 teilgebiet_id: str):
        self.titel: str = titel
        self.aufgabenbeschreibung: str = aufgabenbeschreibung
        self.uebungsliste: list[UebungDto] | None = uebungsliste
        self.ist_speziell: bool = ist_speziell
        self.is_checked: bool = is_checked
        self.expanded: bool = expanded
        self.teilgebiet_id: str = teilgebiet_id

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "TeilgebietDto":
        uebungsliste: list[Any] | dict[str, Any] = data.get("UebungenListe", [])

        if not isinstance(uebungsliste, list):
            uebungsliste = [uebungsliste]

        return TeilgebietDto(
            titel=data["Titel"],
            aufgabenbeschreibung=data["Aufgabenbeschreibung"],
            ist_speziell=data["IstSpeziell"],
            is_checked=data["IsChecked"],
            expanded=data["Expanded"],
            teilgebiet_id=data["Teilgebiet_id"],
            uebungsliste=[UebungDto.from_dict(i)
                          for i in uebungsliste]
                          if uebungsliste
                          else None,
            
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