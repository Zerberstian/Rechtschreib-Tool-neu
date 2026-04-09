from typing import Any
from Dtos.teilgebiet_dto import TeilgebietDto

class UebungsbereichDto:
    def __init__(self,
                 uebungsbereich: str,
                 teilgebiete: list[TeilgebietDto],
                 uebungsbereich_id: int):
        self.uebungsbereich: str = uebungsbereich
        self.teilgebiete: list[TeilgebietDto] = teilgebiete
        self.uebungsbereich_id: int = uebungsbereich_id

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "UebungsbereichDto":
        return UebungsbereichDto(
            uebungsbereich=data["Uebungsbereich"],
            teilgebiete=[TeilgebietDto.from_dict(i) for i in data["Teilgebiet"]],
            uebungsbereich_id=data["Uebungsbereich_id"]
        )