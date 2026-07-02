import json
from Dtos import *
from program_logic.path import Path

class JsonLoader:
    def __init__(self) -> None:
        self.catalogue: CatalogueDto = CatalogueDto.create_empty()

    # Loads aufgaben.json from the local cache into memory
    def load_json(self) -> None:
        with open(Path().cache_path(), "r", encoding="utf-8") as f:
            self.catalogue = CatalogueDto.from_dict(json.load(f))

    def _subfields(self) -> list[SubfieldDto]:
        return [subfield
                for field in self.catalogue.fields
                for subfield in field.subfields]

    def _find_subfield(self, subfield_id: str) -> SubfieldDto | None:
        for subfield in self._subfields():
            if subfield.subfield_id == subfield_id:
                return subfield
        return None

    # Lists the title of every "Uebungsbereich"
    def list_fields(self) -> list[str]:
        return list(dict.fromkeys(field.title for field in self.catalogue.fields))

    # Lists (title, id) of every "Teilgebiet" of the given "Uebungsbereiche".
    # Titles are not guaranteed unique across different Uebungsbereiche.
    def list_subfields(self, field_titles: str | list[str]) -> list[tuple[str, str]]:
        titles = field_titles if isinstance(field_titles, list) else [field_titles]
        return [(subfield.title, subfield.subfield_id)
                for field in self.catalogue.fields if field.title in titles
                for subfield in field.subfields]

    # Lists the task ids of the "Teilgebiete" matched by their unique ids
    def list_tasks_by_subfield(self, subfield_ids: str | list[str]) -> list[str]:
        ids = set(subfield_ids if isinstance(subfield_ids, list) else [subfield_ids])
        return [task.task_id
                for subfield in self._subfields() if subfield.subfield_id in ids
                for task in subfield.tasks]

    # Lists the task ids of the whole catalogue
    def list_all_tasks(self) -> list[str]:
        return [task.task_id
                for subfield in self._subfields()
                for task in subfield.tasks]

    def get_task_by_id(self, task_id: str) -> TaskDto | None:
        for subfield in self._subfields():
            for task in subfield.tasks:
                if task.task_id == task_id:
                    return task
        return None

    def get_special_status(self, subfield_id: str) -> bool:
        subfield = self._find_subfield(subfield_id)
        return subfield.is_special if subfield else False

    def get_task_description(self, subfield_id: str) -> str:
        subfield = self._find_subfield(subfield_id)
        return subfield.task_description if subfield else ""


# Shared instance: load_json() runs once at startup, all modules read from it
json_loader = JsonLoader()
