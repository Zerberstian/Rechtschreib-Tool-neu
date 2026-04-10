from typing import Any
from Dtos.uebungsbereich_dto import UebungsbereichDto

class AufgabenkatalogDto:
    def __init__(self,
                 version: int,
                 last_updated: str,
                 etag: str,
                 total_aufgaben: int,
                 size: int,
                 data: list[UebungsbereichDto] | None):
        self.version: int = version
        self.last_updated: str = last_updated
        self.etag: str = etag
        self.total_aufgaben: int = total_aufgaben
        self.size: int = size
        self.data: list[UebungsbereichDto] | None = data

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "AufgabenkatalogDto":
        return AufgabenkatalogDto(
            version=data["version"],
            last_updated=data["lastUpdated"],
            etag=data["etag"],
            total_aufgaben=data["totalAufgaben"],
            size=data["size"],
            data=[UebungsbereichDto.from_dict(i)
                  for i in data["data"]]
                  if ("data" in data and data["data"] != [])
                  else None
        )