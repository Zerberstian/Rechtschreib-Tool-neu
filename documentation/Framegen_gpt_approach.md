# Framegen
## With Python and Tkinter, you can build a dynamic frame generator that reads JSON data and creates frames with buttons (or other widgets) from it. 
### This explains (step by step) how it works and gives you an example.

### 1.  Example-JSON

Assume your JSON file (data.json) looks like this:
````json
[
    {
        "frage": "Was ist deine Lieblingsfarbe?",
        "antworten": ["Rot", "Blau", "Grün"]
    },
    {
        "frage": "Welches Tier magst du am liebsten?",
        "antworten": ["Hund", "Katze", "Vogel"]
    }
]
````
---
### 2. Tkinter Base
We create a window, a main frame, and dynamically generate frames for each question. Each frame gets buttons for the answers.

````python
import tkinter as tk
import json

# JSON-Daten laden
with open("data.json", "r") as f:
    daten = json.load(f)

root = tk.Tk()
root.title("Dynamische Frames")

main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

def button_click(frage, antwort):
    print(f"Frage: {frage} | Gewählte Antwort: {antwort}")

# Frames generieren
for eintrag in daten:
    frame = tk.Frame(main_frame, bd=2, relief="groove", padx=10, pady=10)
    frame.pack(fill="x", pady=5)

    # Frage als Label
    frage_label = tk.Label(frame, text=eintrag["frage"], font=("Arial", 12, "bold"))
    frage_label.pack(anchor="w")

    # Buttons für Antworten
    for antwort in eintrag["antworten"]:
        btn = tk.Button(frame, text=antwort, 
                        command=lambda f=eintrag["frage"], a=antwort: button_click(f, a))
        btn.pack(side="left", padx=5, pady=5)

root.mainloop()
````
---
### 3. Explanation

### Load JSON: 
- Read the questions and answers with json.load().

### Create frame: 
- For each JSON entry, a separate frame is created.

### Buttons dynamic: 
- each button gets the appropriate response.

### Important: 
- With lambda, you have to pass the variables as default arguments (f=..., a=...), 
<br/>otherwise every button will show the last answer.

### Event function: 
- button_click() displays the selected answer or can be used, for example, for navigation.
---
### 4. Frame by Frame 
Problem: 
- All Frames get packed to the Window at the same time

Solution:
1. Store all frames in a list
2. Keep an index of the currently visible frame
3. Hide the current frame and show the next one when a button is clicked

### Key idea (simple mental model)
- frames = [] → holds all generated frames
- current_index = 0 → which frame is visible
- pack_forget() → hide current frame
- pack() → show next frame
- 
````python
import tkinter as tk
import json

# JSON-Daten laden
with open("fg_json.json", "r", encoding="utf-8") as f:
    daten = json.load(f)

root = tk.Tk()                              # <- Root aka Window
root.title("Dynamische Frames")

main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

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

# Frames generieren
for eintrag in daten:
    frame = tk.Frame(main_frame, bd=2, relief="groove", padx=10, pady=10)

    frage_label = tk.Label(frame, text=eintrag["frage"], font=("Arial", 12, "bold"))
    frage_label.pack(anchor="w")

    for antwort in eintrag["antworten"]:
        btn = tk.Button(
            frame,
            text=antwort,
            command=lambda f=eintrag["frage"], a=antwort: button_click(f, a)
        )
        btn.pack(side="left", padx=5, pady=5)

    frames.append(frame)

# Show only the first frame
show_frame(0)

root.mainloop()
````

### Important notes
- frame always refers to the last frame created
  - so you can't just use:

````python
def next_frame():
    frame.pack_forget()
    frame.pack()
````
- it hides and immediately shows **the same** frame 
    - That's why we use list to go through it step by step (index by index)
---
### 5. Ideas
- add a delay and color the Buttons with the right answer
- Disable buttons after one click
