import tkinter as tk
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Programmlogik import aufgaben_logik

aufgaben_frame_dict = {}

class AufgabenFrame:
    def __init__(self, uebung_id, master, font):
        self.frame_id = len(aufgaben_frame_dict)
        self.uebung_id = uebung_id
        self.master = master
        self.font = font

        aufgaben_frame_dict[self.frame_id] = self

        self.frame = tk.Frame(self.master)
        self.frame2 = tk.Frame(self.frame)
        self.frame2.pack(fill="both", expand=True)
        self.aufgabenbeschreibung_label = tk.Label(self.frame2,
                              text=aufgaben_logik.aufgaben_dict[self.uebung_id].aufgabenbeschreibung,
                              font=(self.font, 20))
        self.aufgabenbeschreibung_label.pack()
        self.uebungs_beschreibung_label = tk.Label(self.frame2,
                                                   text=aufgaben_logik.aufgaben_dict[uebung_id].uebungs_beschreibung,
                                                   font=(self.font, 20))
        self.uebungs_beschreibung_label.pack()
        self.buttonframe = tk.Frame(self.frame2)
        self.buttonframe.pack()
        for index, antwort_moeglichkeit in enumerate(aufgaben_logik.aufgaben_dict[self.uebung_id].moeglichkeiten):
            btn = tk.Button(
                self.buttonframe,
                text=antwort_moeglichkeit,
                font=(self.font, 15),
                command=lambda f= self.buttonframe,
                               antwort=index+1,
                               korrekte_antwort = aufgaben_logik.aufgaben_dict[self.uebung_id].moeglichkeiten[aufgaben_logik.aufgaben_dict[self.uebung_id].korrekt - 1],
                               aufgabe= aufgaben_logik.aufgaben_dict[self.uebung_id],
                               frame_id = self.frame_id: AufgabenFrame.button_click(self, f, antwort, aufgabe, frame_id, korrekte_antwort),
            )
            btn.grid(row=0, column=index, padx=1, pady=1)
    def show(self):
        self.frame.grid(row = 1, column = 1)

    def hide(self):
        self.frame.grid_forget()

    def warten(self):
        print("Fertig warten")
        self.hide()
        frame_generation(self.master, self.font)

    def button_click(self, frame, x, aufgabe, frame_id, korrekte_antwort):
        aufgaben_logik.antwort_check(x, aufgabe, frame_id)
        # Buttons einfärben
        for widget in frame.winfo_children():
            print(widget)
            if isinstance(widget, tk.Button):
                print("Ist Button")
                if widget["text"] == korrekte_antwort:
                    widget.config(bg="#12a505", fg="#ffffff") # richtige Antwort grün
                    print("Button Grun")
                elif widget["text"] != korrekte_antwort:
                    widget.config(bg="#ff0000", fg="#ffffff")  # falsche Antwort rot
                    print("Button Rot")
                widget.config(state="disabled", disabledforeground="#ffffff")
                print("Button disabled")
        frame.update()
        return self.master.after(1000, self.warten())

def frame_generation(master, font):
    try:
        aufgabe = aufgaben_logik.zu_loesende_aufgaben_list[len(aufgaben_frame_dict)]
    except IndexError:
        return print("Fertig mit allen Aufgaben"), reset(), aufgaben_logik.statistik_ausgeben()
    AufgabenFrame(aufgabe, master, font)
    aufgaben_frame_dict[len(aufgaben_frame_dict)-1].show()
    return print("Deine Aufgabe wurde geladen")
def reset():
    aufgaben_frame_dict.clear()

if __name__ == "__main__":
    print("deutsche pass")