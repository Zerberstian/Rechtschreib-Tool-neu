from Dtos.task_dto import TaskDto

class FoundTaskDto:
    def __init__(self, field_idx: int, subfield_idx: int, task_idx: int, task: TaskDto):
        self.field_idx = field_idx
        self.subfield_idx = subfield_idx
        self.task_idx = task_idx
        self.task = task