from tkinter import *               #import for tkinter
from tkinter import messagebox      #import messagebox
import os                           #import for Operating System
import sys                          #import system
import logic                        #import logic.py
import BereichCheckbox              #import BereichCheckbox.py

logic.jsonladen()  #load aufgaben.json (must be in directory)

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
        #message_label.config(text=f"Select value: {value}")

    except ValueError:
        #message_label.config(text=f"Select value: {value}")
        messagebox.showerror("Ungültige Eingabe",
                             "Start mit Standardwert für Aufgabenmenge (10).")

        spinbox.delete(0, END)
        spinbox.insert(0, 10)
        print(spinbox.get())

def start_logic():
    print("Start Logic")

def combined_command():
        on_value_change()
        print(spinbox.get())
        start_logic()

def to_start():
    combined_command()
    show_start_frame()

# def a Window
window = Tk()
window.update_idletasks()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

#'''
window.grid_rowconfigure(0, weight=2)
window.grid_columnconfigure(0, weight=2)
window.grid_rowconfigure(1, weight=3)
window.grid_columnconfigure(1, weight=3)
#'''
#stat point of Window
x_pos = -9
y_pos = 0
window.geometry(f"{screen_width}x{screen_height}+{x_pos}+{y_pos}")                      # Set window size to screen size

window.attributes("-fullscreen", False)                                                 #fullscreen
window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False))              #Escape fullscreen exit
window.bind("<F12>", lambda e: window.attributes("-fullscreen", True))                  #F12 fullscreen toggle
window.title("Rechtschreibtool")                                                        #changing Title from tk to Rechtschreibtool
window.configure(bg="#E0470A")                                                          #backround Color to SRH Color

'''
window.attributes("-alpha", 0.7)
'''

#changing the tk icon to srh icon
icon = PhotoImage(file="srhIcon.png")
window.iconphoto(True, icon)

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

def open_instruktion_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), "A.pdf")

    if sys.platform.startswith("win"):
        os.startfile(pdf_path)

# Frames

'''#################################################################################
'''                                                                                #
#the Main Menu Frame                                                               #
MenuFrame = Frame(window, bg="#E0470A")                                            #
MenuFrame.grid(row=0, column=0, rowspan=2, sticky=NW, ipadx=5)                     #
                                                                                   #
#the Frame to select your                                                          #
SelectFrame = Frame(window, bg="#E0470A")                                          #
                                                                                   #
#Frame for manageing grid                                                          #
CheckBoxFrameS = Frame(SelectFrame, bg="#E0470A")                                  #
CheckBoxFrameS.grid(row=1, column=1, sticky=N)                                     #
                                                                                   #
#Frame for manageing grid                                                          #
ButtonFrameSB = Frame(SelectFrame, bg="#E0470A")                                   #
ButtonFrameSB.grid(row=0, column=0, sticky=NW)                                     #
                                                                                   #
SBBFrame = Frame(SelectFrame, bg="#E0470A")                                        #
SBBFrame.grid(row=1, column=2, rowspan=1, sticky=NW)                               #
                                                                                   #
logicFrame  =   Frame(window, bg="#E0470A")                                        #
                                                                                   #
'''#################################################################################
'''
SelectFrame.grid_rowconfigure(0, weight=1)
SelectFrame.grid_columnconfigure(0, weight=1)

SelectFrame.grid_rowconfigure(1, weight=2)
SelectFrame.grid_columnconfigure(1, weight=4)

SelectFrame.grid_rowconfigure(2, weight=1)
SelectFrame.grid_columnconfigure(2, weight=0)


voidLabel = Label(SelectFrame, bg="#E0470A")
voidLabel.grid(row=0, column=1, sticky=NW)

#the Label for the Icon
iconLabel = Label(MenuFrame, image=icon)
iconLabel.pack(anchor="w", pady=(5, 15), fill="x")

#adding a big Title
headline = Label(window,
                text="Hallo",
                font=("Ariel", 30),
                bg="#E0470A",
                fg="#E0470A")

headline.grid(row=0,column=1, sticky=N)

MenuText = Label(window,
                 text= f"Die offizielle und\n"         #adding a Label with Text in the Center
                       f"verbesserte Version\n"
                       f"des Rechtschreibtools\n"
                       f"der SRH Dresden",
                font=("Ariel", 35),
                bg="#E0470A",
                fg="#ffffff")

MenuText.grid(row=1,column=1, sticky=NW)

# Button for starting the select options
Button(MenuFrame,
        text="Start",
        font=("Ariel", 30),
        bg="#ffffff",
        command=show_select_frame,
        ).pack(anchor="w",fill="x", pady=5)

#Button for going back to Main Menu
Button(ButtonFrameSB,
        text="zurück",
        font=("Ariel", 30),
        bg="#ffffff",
        command=back_to_main_frame,
        ).pack(anchor="w" ,fill="x", pady=2)

#Button for going back to Main Menu
Button(logicFrame,
       text="Start",
       font=("Ariel", 30),
       bg="#ffffff",
       command=back_to_main_frame,
       ).grid(row=3, column=3, padx=5, pady=5)

def callback_value_10():
    global value
    value = 10
    print("Button", value, "pressed")
    spinbox.delete(0, END)
    spinbox.insert(0, 10)

def callback_value_100():
    global value
    value = 100
    print("Button", value, "pressed")
    spinbox.delete(0, END)
    spinbox.insert(0, 100)

Button(SBBFrame,
       text="10",
       font=("Ariel", 30),
       bg="#ffffff",
       command=callback_value_10,
       ).grid(row=3, column=0, padx=5, pady=5, ipadx=15)

Button(SBBFrame,
       text="100",
       font=("Ariel", 30),
       bg="#ffffff",
       command=callback_value_100,
       ).grid(row=3,
              column=1,
              padx=5,
              pady=5)

# Button for Explaination of the Programm (it opens the PDF in same Folder as the Files)
Button(MenuFrame,
       text="Erklärung",
       font=("Ariel", 30),
       bg="#ffffff",
       command=open_instruktion_pdf,
       ).pack(anchor="w",
              fill="x",
              pady=5)

# Button for idk tbh
Button(MenuFrame,
       text="Beenden",
       font=("Ariel", 30),
       bg="#ffffff",
       command=sys.exit,).pack(anchor="w",
                               fill="x",
                               pady=5)

Label(SBBFrame,
      bg="#ffffff",
      text=f"Gieb die Menge\n "
           f"an Aufgaben an:\n "
           f"(1-100)",
      font=("Arial", 18)).grid(row=0,
                               column=0,
                               columnspan=2,
                               pady=5,
                               ipadx=13)

spinbox = Spinbox(SBBFrame,
                  from_=1,
                  to=100,
                  increment=1,
                  width=10,
                  font=("Ariel", 20),
                  command=on_value_change)

spinbox.delete(0, END)
spinbox.insert(0, 10)

spinbox.grid(row=2,
             column=0,
             columnspan=2,
             pady=5,
             ipadx=23)

Button(SBBFrame,
       bg="#ffffff",
       text="Start",
       font=("Ariel", 30),
       command=to_start).grid(row=4,
                              column=0,
                              columnspan=2,
                              ipadx=50,
                              padx=5,
                              pady=5)

#creates a frame for checkboxes
BereichCheckbox.BereichCheckbox(CheckBoxFrameS).create("#ffffff")

window.mainloop()
