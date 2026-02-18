import tkinter as tk
import json
from tkinter.constants import DISABLED

# JSON-Daten laden
with open("json.json", "r", encoding="utf-8") as f:
    daten = json.load(f)

root = tk.Tk()
root.title("Dynamische Frames")

main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

frames = []
current_index = 0

def show_frame(index):
    for frame in frames:
        frame.pack_forget()
    frames[index].pack(fill="x", pady=5)

def next_frame():
    global current_index
    current_index += 1
    if current_index < len(frames):
        show_frame(current_index)
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

# Erste Frage anzeigen
show_frame(0)

root.mainloop()