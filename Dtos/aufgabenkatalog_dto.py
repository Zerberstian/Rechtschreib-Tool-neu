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
        uebungsbereiche: list[Any] | dict[str, Any] = data.get('data', [])

        if not isinstance(uebungsbereiche, list):
            uebungsbereiche = [uebungsbereiche]

        return AufgabenkatalogDto(
            version=data.get("version", 0),
            last_updated=data.get("lastUpdated", ""),
            etag=data.get("etag", ""),
            total_aufgaben=data.get("totalAufgaben", 0),
            size=data.get("size", 0),
            data=[UebungsbereichDto.from_dict(i)
                  for i in uebungsbereiche]
                  if uebungsbereiche
                  else None
        )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "lastUpdated": self.last_updated,
            "etag": self.etag,
            "totalAufgaben": self.total_aufgaben,
            "size": self.size,
            "data": [i.to_dict()
                     for i in self.data]
                     if self.data
                     else None
        }