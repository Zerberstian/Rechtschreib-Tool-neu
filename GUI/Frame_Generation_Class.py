from tkinter import *
import json

from Programmlogik.logic_der_zweite import geladeneAufgaben

def jsonladen():
    with open( "json.json", "r", encoding="utf-8") as f:
        global geladeneAufgaben
        geladeneAufgaben = json.load(f)
#os.path.join(os.path.dirname(__file__),)
window = Tk()

MotherFrame = Frame(window)
MotherFrame.pack()

frames = []
current_index = 0
def show_frame(index):
    for frame in frames:
        frame.pack_forget()
    frames[index].pack(fill="x", pady=5)

def button_click(frage, antwort):
    global current_index
    print(f"Frage: {frage} | Gewählte Antwort: {antwort}")

    if current_index < len(frames) - 1:
        current_index += 1
        show_frame(current_index)
    else:
        print("Ende erreicht")

for bereich in geladeneAufgaben["data"]:
    for teil in bereich["Teilgebiet"]:

        frame = Frame(MotherFrame, bd=2, relief="groove", padx=10, pady=10)
        frame.pack(fill="x", pady=5)

        frage_label = Label(
            frame,
            text=teil["Titel"],
            font=("Arial", 12, "bold")
        )
        frage_label.pack(anchor="w")

        for uebung in teil["UebungenListe"]:

            uebung = teil["UebungenListe"][0]

            for antwort in uebung["Moeglichkeiten"]:
                btn = Button(
                    frame,
                    text=antwort,
                    command=lambda f=teil["Titel"], a=antwort: button_click(f, a)
                )
                btn.pack(side="left", padx=5, pady=5)

    frames.append(frame)

# Show only the first frame
show_frame(0)

if __name__ == "__main__":
    window.mainloop()
    print("b")
