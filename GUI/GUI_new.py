from tkinter import *
from tkinter import messagebox
import os
import sys
import Programmlogik.logic2
from GUI import BereichCheckbox


#logic2.jsonladen()  # json must be in directory

def on_value_change():
    try:
        print(f"{spinbox.get()} = Wert in Spinbox")  # Print zur Kontrolle beim Debugging
        if int(spinbox.get()) > 100:
            spinbox.delete(0, END)
            spinbox.insert(0, 100)

        elif int(spinbox.get()) < 1:
            spinbox.delete(0, END)
            spinbox.insert(0, 1)

    except ValueError:
        messagebox.showerror("Ungültige Eingabe",
                             "Start mit Standardwert für Aufgabenmenge (10).")
        spinbox.delete(0, END)
        spinbox.insert(0, 10)
        print(spinbox.get(), "bei ungültiger spinbox.get()")

# max Aufgaben 10 als quickselct (Logic)
def callback_value_10():
    spinbox.delete(0, END)
    spinbox.insert(0, 10)

# max Aufgaben 100 als quickselct (Logic)
def callback_value_100():
    spinbox.delete(0, END)
    spinbox.insert(0, 100)

def start_logic():
    print("Start der logik")
    print(spinbox.get(), "= value check 2")
    show_start_frame()

def combined_command():
        on_value_change()
        print(spinbox.get(), "= value check 1")
        #start_logic()

        aktiv = BereichCheckbox.get_active()
        if not aktiv  == []:
            start_logic()
            for a in logic2.list_uebungen(aktiv): print(a)
        else:
            messagebox.showerror("Fehlende Auswahl",
                                 "Es wurde kein Aufgabenbereich ausgewählt.")

def to_start():
    combined_command()

# Konstanten für Größen und Farben
BG_Farbe = "#E0470A"
Btn_BG_Farbe = "#ffffff"
BtnFontArt = "Arial"
BtnFontGroesse = 30

# Fenster wird definiert
window = Tk()
window.update_idletasks()

# Ausrichtung im Fenster
window.grid_rowconfigure(0, weight=2)
window.grid_columnconfigure(0, weight=2)
window.grid_rowconfigure(1, weight=3)
window.grid_columnconfigure(1, weight=3)

# generiere Fenster über ganzen Bildschirm
x_pos = -9
y_pos = 0
window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}+{x_pos}+{y_pos}")

# Eigenschaften für Fenster
window.minsize(1100, 650)
window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False))              # Escape = exit fullscreen
window.bind("<F12>", lambda e: window.attributes("-fullscreen", True))                  # F12 = enter fullscreen
window.title("Rechtschreibtool")                                                        # changing Title from tk to Rechtschreibtool
window.configure(bg=BG_Farbe)                                                           # backround Color to SRH Color
icon = PhotoImage(file="srhIcon.png")                                                   # changing the tk icon to srh icon
window.iconphoto(True, icon)

# zwischen Frames wechseln
def show_start_frame():
    logicFrame.grid(row=0, column=0, sticky=NW)
    SelectFrame.place_forget()

def show_select_frame():
    MenuFrame.grid_forget()
    headline.grid_forget()
    SelectFrame.place(x=0, y=0, relwidth=1, relheight=1)
    MenuText.grid_forget()

def back_to_main_frame():
    MenuFrame.grid(row=0, column=0, rowspan=2, sticky=NW)
    SelectFrame.place_forget()
    headline.grid(row=0,column=1, sticky=N)
    MenuText.grid(row=1,column=1, sticky=NW)
    logicFrame.grid_forget()

def open_instruction_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), "A.pdf")

    if sys.platform.startswith("win"):
        os.startfile(pdf_path)

# Frames
##############################################################################
# Frame für das Mainmenu
MenuFrame = Frame(window, bg=BG_Farbe)
MenuFrame.grid(row=0, column=0, rowspan=2, sticky=NW, ipadx=5)

# Frame für die Aufgabenauswahl
SelectFrame = Frame(window, bg=BG_Farbe)

# Frame for managing grid
CheckBoxFrameS = Frame(SelectFrame, bg=BG_Farbe)
CheckBoxFrameS.grid(row=1, column=1, sticky=N)

# Frame for managing grid
ButtonFrameSB = Frame(SelectFrame, bg=BG_Farbe)
ButtonFrameSB.grid(row=0, column=0, sticky=NW)

# Frame für Spinbox und Buttons
SpinBoxFrame = Frame(SelectFrame, bg=BG_Farbe)
SpinBoxFrame.grid(row=1, column=2, rowspan=1, sticky=NW)

logicFrame  =   Frame(window, bg=BG_Farbe)

AufgabenFrameSeite = Frame(window, bg=BG_Farbe)
##############################################################################

SelectFrame.grid_rowconfigure(0, weight=1)
SelectFrame.grid_columnconfigure(0, weight=1)

SelectFrame.grid_rowconfigure(1, weight=2)
SelectFrame.grid_columnconfigure(1, weight=4)

SelectFrame.grid_rowconfigure(2, weight=1)
SelectFrame.grid_columnconfigure(2, weight=0)

# Label für Ausrichtungszwecke
voidLabel = Label(SelectFrame, bg=BG_Farbe)
voidLabel.grid(row=0, column=1, sticky=NW)

# Label für das Icon
iconLabel = Label(MenuFrame, image=icon)
iconLabel.pack(anchor="w", pady=(5, 15), fill="x")

# adding a big Title
headline = Label(window,
                text="Hallo",
                font=(BtnFontArt, BtnFontGroesse),
                bg=BG_Farbe,
                fg=BG_Farbe)

headline.grid(row=0,column=1, sticky=N)

MenuText = Label(window,
                 text= f"Die offizielle und\n"         # adding a Label with Text in the Center
                       f"verbesserte Version\n"
                       f"des Rechtschreibtools\n"
                       f"der SRH Dresden",
                font=(BtnFontArt, 35),
                bg=BG_Farbe,
                fg="#ffffff")

MenuText.grid(row=1,column=1, sticky=NW)

# Button for starting the select options
Button(MenuFrame,
        text="Start",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=show_select_frame,
        ).pack(anchor="w",fill="x", pady=5)

# Buttons for going back to Main Menu
Button(ButtonFrameSB,
        text="zurück",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=back_to_main_frame,
        ).pack(anchor="w" ,fill="x", pady=5, padx=5)

Button(logicFrame,
       text="zurück",
       font=(BtnFontArt, BtnFontGroesse),
       bg=Btn_BG_Farbe,
       command=back_to_main_frame,
       ).grid(row=3, column=3, padx=5, pady=5)

# max Aufgaben 10 als quickselct (Button)
Button(SpinBoxFrame,
       text="10",
       font=(BtnFontArt, BtnFontGroesse),
       bg=Btn_BG_Farbe,
       command=callback_value_10,
       ).grid(row=3, column=0, padx=5, pady=5, ipadx=15)

# max Aufgaben 100 als quickselct (Button)
Button(SpinBoxFrame,
       text="100",
       font=(BtnFontArt, BtnFontGroesse),
       bg=Btn_BG_Farbe,
       command=callback_value_100,
       ).grid(row=3,
              column=1,
              padx=5,
              pady=5)

# Button for Explaination of the Programm (it opens the PDF in same Folder as the Files)
Button(MenuFrame,
       text="Erklärung",
       font=(BtnFontArt, BtnFontGroesse),
       bg=Btn_BG_Farbe,
       command=open_instruction_pdf,
       ).pack(anchor="w",
              fill="x",
              pady=5)

# sys Exit
Button(MenuFrame,
       text="Beenden",
       font=(BtnFontArt, BtnFontGroesse),
       bg=Btn_BG_Farbe,
       command=sys.exit,).pack(anchor="w",
                               fill="x",
                               pady=5)
Label(SpinBoxFrame,
      bg="#ffffff",
      text=f"Gib die Menge\n "
           f"an Aufgaben an:\n "
           f"(1-100)",
      font=("Arial", 18)).grid(row=0,
                               column=0,
                               columnspan=2,
                               pady=5,
                               ipadx=13)

# Spinbox
spinbox = Spinbox(SpinBoxFrame,
                  from_=1,
                  to=100,
                  increment=1,
                  width=10,
                  font=("Arial", 20),
                  command=on_value_change)

spinbox.delete(0, END)
spinbox.insert(0, 10)  # bei Inizialisierung wird der Standardwert 10 festgelegt

spinbox.grid(row=2,
             column=0,
             columnspan=2,
             pady=5,
             ipadx=23)

# start der logik + extras
Button(SpinBoxFrame,
       bg=Btn_BG_Farbe,
       text="Start",
       font=(BtnFontArt, BtnFontGroesse),
       command=to_start).grid(row=4,
                              column=0,
                              columnspan=2,
                              ipadx=50,
                              padx=5,
                              pady=5)

# creates checkboxes
BereichCheckbox.BereichCheckbox(CheckBoxFrameS).create("#ffffff")

if __name__ == "__main__":
    window.mainloop()
