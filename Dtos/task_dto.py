from typing import Any

class TaskDto:
    def __init__(self,
                 answer_options: list[str],
                 correct_answer: int,
                 information_text: str | None,
                 task_description: str,
                 task_id: str):
        self.answer_options = answer_options
        self.correct_answer = correct_answer
        self.information_text = information_text
        self.task_description = task_description
        self.task_id = task_id

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "TaskDto":
            return TaskDto(
            answer_options=data.get("Moeglichkeiten", []),
            correct_answer=data.get("KorrekteAntwort", 0),
            information_text=data.get("Infotext", None),
            task_description=data.get("UebungsBeschreibung", ""),
            task_id=data.get("Uebung_id", "")
        )
    
    @staticmethod
    def create_empty():
        return TaskDto(
            answer_options=[],
            correct_answer=0,
            information_text=None,
            task_description="",
            task_id=""
        )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "Moeglichkeiten": self.answer_options,
            "Korrekte_antwort": self.correct_answer,
            "Infotext": self.information_text,
            "UebungsBeschreibung": self.task_description,
            "Uebung_id": self.task_id
        }