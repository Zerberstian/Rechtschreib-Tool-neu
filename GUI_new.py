from tkinter import *               #import for tkinter
from tkinter import messagebox      #import messagebox
import os                           #import for Operating System
import sys                          #import system
import logic2                        #import logic.py
import BereichCheckbox              #import BereichCheckbox.py

logic2.jsonladen()  #load aufgaben.json (must be in directory)

def on_value_change():
    global value
    global spinbox
    try:
        value = int(spinbox.get())
        print(value)
        if value>100:
            value = 100
            spinbox.delete(0, END)
            spinbox.insert(0, 100)
        elif value<=0:
            value = 1
            spinbox.delete(0, END)
            spinbox.insert(0, 1)

    except ValueError:
        messagebox.showerror("Ungültige Eingabe",
                             "Start mit Standardwert für Aufgabenmenge (10).")

        spinbox.delete(0, END)
        spinbox.insert(0, 10)
        print(spinbox.get())

def start_logic():
    print("Start Logic")
    lokal_var = value
    print(lokal_var)
    show_start_frame()

def combined_command():
        on_value_change()
        print(spinbox.get())
        aktiv = BereichCheckbox.get_active()
        if not aktiv  == []:
            start_logic()
            for a in logic2.list_uebungen(aktiv): print(a)
        else:
            print("Hs")

def to_start():
    combined_command()

# Konstanten für großen und Farben
BG_Farbe = "#E0470A"
Btn_BG_Farbe = "#ffffff"
BtnFontGröße = 30

# def a Window
window = Tk()
window.update_idletasks()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

#ausrichtung im Window
window.grid_rowconfigure(0, weight=2)
window.grid_columnconfigure(0, weight=2)
window.grid_rowconfigure(1, weight=3)
window.grid_columnconfigure(1, weight=3)

#stat point of Window
x_pos = -9
y_pos = 0
window.geometry(f"{screen_width}x{screen_height}+{x_pos}+{y_pos}")                      # Set window size to screen size
window.minsize(1100, 650)

window.attributes("-fullscreen", False)                                                 #fullscreen
window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False))              #Escape fullscreen exit
window.bind("<F12>", lambda e: window.attributes("-fullscreen", True))                  #F12 fullscreen toggle
window.title("Rechtschreibtool")                                                        #changing Title from tk to Rechtschreibtool
window.configure(bg=BG_Farbe)                                                           #backround Color to SRH Color

'''
window.attributes("-alpha", 0.7)
'''

#changing the tk icon to srh icon
icon = PhotoImage(file="srhIcon.png")
window.iconphoto(True, icon)

#zwischen frames wechseln
def show_start_frame():
    logicFrame.grid(row=0, column=0, sticky=NW)
    SelectFrame.place_forget()

#zwischen frames wechseln
def show_select_frame():
    MenuFrame.grid_forget()
    headline.grid_forget()
    SelectFrame.place(x=0, y=0, relwidth=1, relheight=1)
    MenuText.grid_forget()

#zwischen frames wechseln
def back_to_main_frame():
    MenuFrame.grid(row=0, column=0, rowspan=2, sticky=NW)
    SelectFrame.place_forget()
    headline.grid(row=0,column=1, sticky=N)
    MenuText.grid(row=1,column=1, sticky=NW)
    logicFrame.grid_forget()

def open_instruktion_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), "A.pdf")

    if sys.platform.startswith("win"):
        os.startfile(pdf_path)

# Frames
#################################################################################
#
#the Main Menu Frame                                                               #
MenuFrame = Frame(window, bg=BG_Farbe)                                            #
MenuFrame.grid(row=0, column=0, rowspan=2, sticky=NW, ipadx=5)                     #
                                                                                   #
#the Frame to select your                                                          #
SelectFrame = Frame(window, bg=BG_Farbe)                                          #
                                                                                   #
#Frame for manageing grid                                                          #
CheckBoxFrameS = Frame(SelectFrame, bg=BG_Farbe)                                  #
CheckBoxFrameS.grid(row=1, column=1, sticky=N)                                     #
                                                                                   #
#Frame for manageing grid                                                          #
ButtonFrameSB = Frame(SelectFrame, bg=BG_Farbe)                                   #
ButtonFrameSB.grid(row=0, column=0, sticky=NW)                                     #
#Frame für Spinbox und Btn
SBBFrame = Frame(SelectFrame, bg=BG_Farbe)                                        #
SBBFrame.grid(row=1, column=2, rowspan=1, sticky=NW)                               #
                                                                                   #
logicFrame  =   Frame(window, bg=BG_Farbe)                                        #

AufgabenFrameSeite = Frame(window, bg=BG_Farbe)
                                                                                   #
#####################################################################################

SelectFrame.grid_rowconfigure(0, weight=1)
SelectFrame.grid_columnconfigure(0, weight=1)

SelectFrame.grid_rowconfigure(1, weight=2)
SelectFrame.grid_columnconfigure(1, weight=4)

SelectFrame.grid_rowconfigure(2, weight=1)
SelectFrame.grid_columnconfigure(2, weight=0)

#Ein Label was nur aus Ausrichtungszwecken existiert
voidLabel = Label(SelectFrame, bg=BG_Farbe)
voidLabel.grid(row=0, column=1, sticky=NW)

#the Label for the Icon
iconLabel = Label(MenuFrame, image=icon)
iconLabel.pack(anchor="w", pady=(5, 15), fill="x")




#adding a big Title
headline = Label(window,
                text="Hallo",
                font=("Ariel", BtnFontGröße),
                bg=BG_Farbe,
                fg=BG_Farbe)

headline.grid(row=0,column=1, sticky=N)

MenuText = Label(window,
                 text= f"Die offizielle und\n"         #adding a Label with Text in the Center
                       f"verbesserte Version\n"
                       f"des Rechtschreibtools\n"
                       f"der SRH Dresden",
                font=("Ariel", 35),
                bg=BG_Farbe,
                fg="#ffffff")

MenuText.grid(row=1,column=1, sticky=NW)

# Button for starting the select options
Button(MenuFrame,
        text="Start",
        font=("Ariel", BtnFontGröße),
        bg=Btn_BG_Farbe,
        command=show_select_frame,
        ).pack(anchor="w",fill="x", pady=5)

#Button for going back to Main Menu
Button(ButtonFrameSB,
        text="zurück",
        font=("Ariel", BtnFontGröße),
        bg=Btn_BG_Farbe,
        command=back_to_main_frame,
        ).pack(anchor="w" ,fill="x", pady=5, padx=5)

#Button for going back to Main Menu
Button(logicFrame,
       text="zurück",
       font=("Ariel", BtnFontGröße),
       bg=Btn_BG_Farbe,
       command=back_to_main_frame,
       ).grid(row=3, column=3, padx=5, pady=5)

#max Aufgaben 10 als quickselct (Logic)
def callback_value_10():
    global value
    value = 10
    print("Button", value, "pressed")
    spinbox.delete(0, END)
    spinbox.insert(0, 10)

#max Aufgaben 100 als quickselct (Logic)
def callback_value_100():
    global value
    value = 100
    print("Button", value, "pressed")
    spinbox.delete(0, END)
    spinbox.insert(0, 100)

#max Aufgaben 10 als quickselct (Button)
Button(SBBFrame,
       text="10",
       font=("Ariel", BtnFontGröße),
       bg=Btn_BG_Farbe,
       command=callback_value_10,
       ).grid(row=3, column=0, padx=5, pady=5, ipadx=15)

#max Aufgaben 100 als quickselct (Button)
Button(SBBFrame,
       text="100",
       font=("Ariel", BtnFontGröße),
       bg=Btn_BG_Farbe,
       command=callback_value_100,
       ).grid(row=3,
              column=1,
              padx=5,
              pady=5)

# Button for Explaination of the Programm (it opens the PDF in same Folder as the Files)
Button(MenuFrame,
       text="Erklärung",
       font=("Ariel", BtnFontGröße),
       bg=Btn_BG_Farbe,
       command=open_instruktion_pdf,
       ).pack(anchor="w",
              fill="x",
              pady=5)

# sys Exit
Button(MenuFrame,
       text="Beenden",
       font=("Ariel", BtnFontGröße),
       bg=Btn_BG_Farbe,
       command=sys.exit,).pack(anchor="w",
                               fill="x",
                               pady=5)
#Siehe Text
Label(SBBFrame,
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
spinbox = Spinbox(SBBFrame,
                  from_=1,
                  to=100,
                  increment=1,
                  width=10,
                  font=("Ariel", 20),
                  command=on_value_change)

#bei inizialisierung wird der Standardwert 10 festgelegt
spinbox.delete(0, END)
spinbox.insert(0, 10)

spinbox.grid(row=2,
             column=0,
             columnspan=2,
             pady=5,
             ipadx=23)

#start der logik + extras
Button(SBBFrame,
       bg=Btn_BG_Farbe,
       text="Start",
       font=("Ariel", BtnFontGröße),
       command=to_start).grid(row=4,
                              column=0,
                              columnspan=2,
                              ipadx=50,
                              padx=5,
                              pady=5)
#creates a frame for checkboxes
BereichCheckbox.BereichCheckbox(CheckBoxFrameS).create("#ffffff")

if __name__ == "__main__":
    window.mainloop()
