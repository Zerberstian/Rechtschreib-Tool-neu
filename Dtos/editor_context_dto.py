class EditorContextDto:
    def __init__(self,
                 bereich_name: str,
                 teilgebiet_name: str,
                 aufgabe_label: str):
        self.bereich_name = bereich_name
        self.teilgebiet_name = teilgebiet_name
        self.aufgabe_label = aufgabe_label
    
    def clear(self):
        self.bereich_name = ""
        self.teilgebiet_name = ""
        self.aufgabe_label = ""