import tkinter as tk
import json #will become useless
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Programmlogik import aufgaben_logik

# JSON-Daten laden
with open("json.json", "r", encoding="utf-8") as f:
    daten = json.load(f)

frames = []
aufgaben_frame_dict = {}
current_index = 0

class AufgabenFrame:
    def __init__(self, uebung_id, master, font):
        self.frame_id = len(aufgaben_frame_dict)
        self.uebung_id = uebung_id
        self.master = master
        self.font = font

        aufgaben_frame_dict[self.frame_id] = self

        self.frame = tk.Frame(self.master)
        self.label = tk.Label(self.frame, text=aufgaben_logik.aufgaben_dict[self.uebung_id].aufgabenbeschreibung, font=(self.font, 20))
        self.label.pack(side="left")
        self.buttonframe = tk.Frame(self.frame)
        self.buttonframe.pack()
        for index, antwort_moeglichkeit in enumerate(aufgaben_logik.aufgaben_dict[self.uebung_id].moeglichkeiten):
            btn = tk.Button(
                self.buttonframe,
                text=antwort_moeglichkeit,
                font=(self.font, 15),
                command=lambda x=antwort_moeglichkeit: x(x),
            )
    def show(self):
        self.frame.grid(row = 1, column = 1)

    def hide(self):
        self.frame.pack_forget()

def show_frame(index):
    for frame in frames:
        frame.pack_forget()
    frames[index].pack(fill="x", pady=5)

def next_frame():
    global current_index
    current_index += 1
    if current_index < len(frames):
        pass#show_frame(current_index)
    else:
        print("Ende erreicht")

def button_click(frame, richtige_antwort, gewaehlte_antwort):
    print(f"Gewählte Antwort: {gewaehlte_antwort}")

    # Buttons einfärben
    for widget in frame.winfo_children():
        if isinstance(widget, tk.Button):
            if widget["text"] == richtige_antwort:
                widget.config(bg="#12a505", fg="#ffffff")  # richtige Antwort grün
            elif widget["text"] == gewaehlte_antwort:
                widget.config(bg="#ff0000", fg="#ffffff")  # falsche Antwort rot
            widget.config(state="disabled")
    # Nach 1 Sekunde nächste Frage
    root.after(1000, next_frame)

def start_frame_generation(master, font):
    aufgabe = aufgaben_logik.zu_loesende_aufgaben_list[current_index]
    AufgabenFrame(aufgabe, master, font)
    aufgaben_frame_dict[current_index].show()
    pass

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dynamische Frames")

    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10)

    # Frames generieren
    for eintrag in daten:
        frame = tk.Frame(main_frame, bd=2, relief="groove", padx=10, pady=10)

        frage_label = tk.Label(frame, text=eintrag["frage"], font=("Arial", 25, "bold"))
        frage_label.pack(anchor="w")

        for antwort in eintrag["antworten"]:
            btn = tk.Button(
                frame,
                text=antwort,
                font=("Arial", 20, "bold"),
                command=lambda f=frame,
                               r=eintrag["richtig"],
                               a=antwort: button_click(f, r, a)
            )
            btn.pack(side="left", padx=5, pady=5)

        frames.append(frame)

    show_frame(0)

    root.mainloop()