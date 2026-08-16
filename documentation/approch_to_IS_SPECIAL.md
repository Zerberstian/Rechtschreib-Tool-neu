# Is special 
## Some exercises have "is_special": TRUE for wxample where you have to place a Comma
### here we show step by step how we approched this kind of exrcises

1. We had the Idea to dynamicly create Buttons for each Word
````python
import tkinter as tk
root = tk.Tk()

tk.Button(root,
       text="Hi",
       command=lambda: print("Hi")).pack(side=LEFT)
tk.Button(root,
       text="im",
       command=lambda: print("im")).pack(side=LEFT)
tk.Button(root,
       text="Josh",
       command=lambda: print("Josh")).pack(side=LEFT)

if __name__ == "__main__": 
    root.mainloop()
````
### Note: _In this example, there is no dynamic creation yet_ !

---
2. By giving the buttons a  "call back" we can check if the pressed Button matches the value that is correct.

The JSON we use in this Example:
````json
{
  "Satz": "Hi im Josh",
  "richtig": 1
}
````
The Python Code:
````python
import tkinter as tk
import json

# JSON laden
def jsonload():
    with open("example.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Button-Klick Funktion
def button_click(position):
    if position == richtig:
        print("✅ Richtig!")
    else:
        print("❌ Falsch!")

# Daten laden
geladeneAufgaben = jsonload()
satz = geladeneAufgaben["Satz"]
richtig = geladeneAufgaben["richtig"]  # z.B. 1

woerter = satz.split()

# GUI
root = tk.Tk()
frame = tk.Frame(root)
frame.pack(pady=10)

for index, wort in enumerate(woerter, start=1):  # start=1 → first position = 1
    btn = tk.Button(
        frame,
        text=wort,
        command=lambda pos=index: button_click(pos)
    )
    btn.pack(side="left", padx=5)

root.mainloop()
````
### Now you will see three buttons, and you have to choose the button after which the comma should be placed.
This structure should appear:
````
+----------------------------------------+
|              "My Window"               |
| -------------------------------------- |
| [ Button 1 ] [ Button 2 ] [ Button 3 ] |
|                                        |
+----------------------------------------+
````
The Buttons will be called:
[Hi] [Im] [Josh]
The correct one for where the Comma should be 1:
>Hi, im Josh

If you now press [Button 1] the Program will print "✅ Richtig!" to your Console.<br/>
Now its your part to be creative and use this Example to your advantage.