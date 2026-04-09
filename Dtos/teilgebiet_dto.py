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
        self.titel: str = titel
        self.aufgabenbeschreibung: str = aufgabenbeschreibung
        self.uebungsliste: list[UebungDto] = uebungsliste
        self.ist_speziell: bool = ist_speziell
        self.is_checked: bool = is_checked
        self.expanded: bool = expanded
        self.teilgebiet_id: str = teilgebiet_id

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "TeilgebietDto":
        return TeilgebietDto(
            titel=data["Titel"],
            aufgabenbeschreibung=data["Aufgabenbeschreibung"],
            uebungsliste=[UebungDto.from_dict(i) for i in data["UebungenListe"]],
            ist_speziell=data["IstSpeziell"],
            is_checked=data["IsChecked"],
            expanded=data["Expanded"],
            teilgebiet_id=data["Teilgebiet_id"]
        )