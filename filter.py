from tkinter import *
import json

GEWUENSCHTE_ANZAHL = 3

with open("blob2.json", "r", encoding="utf-8") as f:
    data = json.load(f)

gefilterte_uebungen = []


for teilgebiet in data["Teilgebiet"]:
    for uebung in teilgebiet["UebungenListe"]:
        if len(uebung["Moeglichkeiten"]) == GEWUENSCHTE_ANZAHL:
            gefilterte_uebungen.append({
                "Titel": teilgebiet["Titel"],
                "Aufgabenbeschreibung": teilgebiet["Aufgabenbeschreibung"],
                "Moeglichkeiten": uebung["Moeglichkeiten"],
                "KorrekteAntwort": uebung["KorrekteAntwort"],
                "Infotext": uebung["Infotext"]
            })

#print(gefilterte_uebungen)

class ButtonCreator:
    def __init__(self, parent, quantity):
        self.parent = parent
        self.quantity = quantity
        self.buttons = []
        
        self.create_buttons()
        

    def create_buttons(self):
        for index, i in enumerate(self.quantity):
            btn = Button(
                self.parent,
                text=f"{i}",
                command=lambda index=index, i=i: self.on_click(index, i))
            
            btn.pack(pady=5)
            self.buttons.append(btn)


    def on_click(self, index, i):      
        print(f"Button {i} wurde geklickt")
        print(str(index))

        if (index)+1 == uebung["KorrekteAntwort"]:
            print("R")
        else:
            print("FF 15")


if __name__ == "__main__":

    window = Tk()
    window.geometry("300x300")

    s = gefilterte_uebungen[0]
    p1 = ButtonCreator(parent=window, quantity=s["Moeglichkeiten"], GEWUENSCHTE_ANZAHL = 3)
    p2 = ButtonCreator(parent=Frame, quantity=s["Moeglichkeiten"], GEWUENSCHTE_ANZAHL = 2)
    print(len(p1.quantity))
    window.mainloop()