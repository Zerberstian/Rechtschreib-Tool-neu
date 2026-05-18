from typing import Any
from Dtos.subfield_dto import SubfieldDto

class FieldDto:
    def __init__(self,
                 title: str,
                 subfields: list[SubfieldDto],
                 field_id: int):
        self.title = title
        self.subfields = subfields
        self.field_id = field_id

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "FieldDto":
        subfield: list[Any] | dict[str, Any] = data.get("Teilgebiet", [])

        if not isinstance(subfield, list):
            subfield = [subfield]

        return FieldDto(
            title=data.get("Uebungsbereich", ""),
            field_id=data.get("Uebungsbereich_id", 0),
            subfields=[SubfieldDto.from_dict(i)
                         for i in subfield]
                         if subfield
                         else [],
        )
    
    @staticmethod
    def create_empty():
        return FieldDto(
            title="",
            subfields=[],
            field_id=0
        )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "Uebungsbereich": self.title,
            "Uebungsbereich_id": self.field_id,
            "Teilgebiet": [i.to_dict()
                           for i in self.subfields]
                           if self.subfields
                           else []
        }