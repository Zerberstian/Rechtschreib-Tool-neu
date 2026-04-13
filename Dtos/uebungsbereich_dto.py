from typing import Any
from Dtos.teilgebiet_dto import TeilgebietDto

class UebungsbereichDto:
    def __init__(self,
                 uebungsbereich: str,
                 teilgebiete: list[TeilgebietDto] | None,
                 uebungsbereich_id: int):
        self.uebungsbereich: str = uebungsbereich
        self.teilgebiete: list[TeilgebietDto] | None = teilgebiete
        self.uebungsbereich_id: int = uebungsbereich_id

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "UebungsbereichDto":
        teilgebiet: list[Any] | dict[str, Any] = data.get("Teilgebiet", [])

        if not isinstance(teilgebiet, list):
            teilgebiet = [teilgebiet]

        return UebungsbereichDto(
            uebungsbereich=data["Uebungsbereich"],
            uebungsbereich_id=data["Uebungsbereich_id"],
            teilgebiete=[TeilgebietDto.from_dict(i)
                         for i in teilgebiet]
                         if teilgebiet
                         else None,
        )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "Uebungsbereich": self.uebungsbereich,
            "Uebungsbereich_id": self.uebungsbereich_id,
            "Teilgebiet": [i.to_dict()
                           for i in self.teilgebiete]
                           if self.teilgebiete
                           else None
        }