from typing import Any
from Dtos.field_dto import FieldDto

class CatalogueDto:
    def __init__(self,
                 version: int,
                 last_updated: str,
                 etag: str,
                 total_tasks: int,
                 size: int,
                 fields: list[FieldDto]):
        self.version = version
        self.last_updated = last_updated
        self.etag = etag
        self.total_tasks = total_tasks
        self.size = size
        self.fields = fields

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "CatalogueDto":
        fields: list[Any] | dict[str, Any] = data.get('data', [])

        if not isinstance(fields, list):
            fields = [fields]

        return CatalogueDto(
            version=data.get("version", 0),
            last_updated=data.get("lastUpdated", ""),
            etag=data.get("etag", ""),
            total_tasks=data.get("totalAufgaben", 0),
            size=data.get("size", 0),
            fields=[FieldDto.from_dict(i)
                  for i in fields]
                  if fields
                  else []
        )
    
    @staticmethod
    def create_empty():
        return CatalogueDto(
            version=0,
            last_updated="",
            etag="",
            total_tasks=0,
            size=0,
            fields=[]
        )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "lastUpdated": self.last_updated,
            "etag": self.etag,
            "totalAufgaben": self.total_tasks,
            "size": self.size,
            "data": [i.to_dict()
                     for i in self.fields]
                     if self.fields
                     else None
        }