from typing import Any
from Dtos.task_dto import TaskDto

class SubfieldDto:
    def __init__(self,
                 title: str,
                 task_description: str,
                 tasks: list[TaskDto],
                 is_special: bool,
                 is_checked: bool,
                 is_expanded: bool,
                 subfield_id: str):
        self.title = title
        self.task_description = task_description
        self.tasks = tasks
        self.is_special = is_special
        self.is_checked = is_checked
        self.is_expanded = is_expanded
        self.subfield_id = subfield_id

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "SubfieldDto":
        task_list: list[Any] | dict[str, Any] = data.get("UebungenListe", [])

        if not isinstance(task_list, list):
            task_list = [task_list]

        return SubfieldDto(
            title=data.get("Titel", ""),
            task_description=data.get("Aufgabenbeschreibung", ""),
            is_special=data.get("IstSpeziell", False),
            is_checked=data.get("IsChecked", False),
            is_expanded=data.get("Expanded", False),
            subfield_id=data.get("Teilgebiet_id", ""),
            tasks=[TaskDto.from_dict(i)
                          for i in task_list]
                          if task_list
                          else []
        )
    
    @staticmethod
    def create_empty():
        return SubfieldDto(
            title="",
            task_description="",
            tasks=[],
            is_special=False,
            is_checked=False,
            is_expanded=False,
            subfield_id=""
        )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "Titel": self.title,
            "Aufgabenbeschreibung": self.task_description,
            "IstSpeziell": self.is_special,
            "IsChecked": self.is_checked,
            "Expanded": self.is_expanded,
            "Teilgebiet_id": self.subfield_id,
            "UebungenListe": [i.to_dict()
                              for i in self.tasks]
                              if self.tasks
                              else None
        }