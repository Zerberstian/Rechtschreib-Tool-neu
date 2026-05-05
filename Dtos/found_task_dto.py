from Dtos.uebung_dto import UebungDto

class FoundTaskDto:
    def __init__(self, bereich_idx: int, teil_idx: int, aufgabe_idx: int, aufgabe: UebungDto):
        self.bereich_idx = bereich_idx
        self.teil_idx = teil_idx
        self.aufgabe_idx = aufgabe_idx
        self.aufgabe = aufgabe