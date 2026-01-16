from tkinter import *       #import for tkinter
import os                   #import for Operating System
import sys                  #import system
import logic                #import logic.py

logic.jsonladen()           #load aufgaben.json (must be in directory)

# def a Window
window = Tk()

window.update_idletasks()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

#stat point of Window
x_pos = -9
y_pos = 0
window.geometry(f"{screen_width}x{screen_height}+{x_pos}+{y_pos}")                      # Set window size to screen size

window.attributes("-fullscreen", False)                                                 #fullscreen
window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False))              #Escape fullscreen exit
window.bind("<F12>", lambda e: window.attributes("-fullscreen", True))                  #F12 fullscreen toggle
window.title("Rechtschreibtool")                                                       #changing Title from tk to Rechtschreibtool
window.configure(bg="#E0470A")                                                          #backround Color to SRH Color

'''
window.attributes("-alpha", 0.7)
'''

#changing the tk icon to srh icon
icon = PhotoImage(file="srhIcon.png")
window.iconphoto(True, icon)

def show_select_frame():
    MenuFrame.place_forget()
    headline.pack_forget()
    SelectFrame.place(x=0, y=0,relwidth=1, relheight=1)
    MenuText.place_forget()

def back_to_main_frame():
    MenuFrame.place(x=0, y=0)
    SelectFrame.place_forget()
    headline.pack()
    MenuText.place(x=screen_width / 2, y=screen_height / 2, anchor="center")

def open_instruktion_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), "A.pdf")

    if sys.platform.startswith("win"):
        os.startfile(pdf_path)

#the Main Menu Frame
MenuFrame = Frame(window, bg="#E0470A")
MenuFrame.place(x=0, y=0)

#the Frame to select your
SelectFrame = Frame(window, bg="#E0470A")

#the Label for the Icon
iconLabel = Label(MenuFrame, image=icon)
iconLabel.pack(anchor="w", pady=(5, 20))

#adding a big Title
headline = Label(window,
               text="Hallo",
               font=("Ariel", 30),
               bg="#E0470A",
               fg="#ffffff")

headline.pack()

MenuText = Label(window, text= f"Die offizielle und\n"         #adding a Label with Text in the Center
                               f"verbesserte Version\n"
                               f"des Rechtschreibtools\n"
                               f"der SRH Dresden",
                               font=("Ariel", 35),
                               bg="#E0470A",
                               fg="#ffffff")

MenuText.place(x=screen_width/2,
               y=screen_height/2,
               anchor="center")

# Button for starting the select options
Button(MenuFrame,
       text="Start",
       font=("Ariel", 30),
       bg="#ffffff",
       command=show_select_frame,
       ).pack(anchor="w",fill="x", pady=5)

#Button for going back to Main Menu
Button(SelectFrame,
       text="zurück",
       font=("Ariel", 30),
       bg="#ffffff",
       command=back_to_main_frame,
       ).pack(anchor="w", pady=5)

# Button for Explaination of the Programm (it opens the PDF in same Folder as the Files)
Button(MenuFrame,
       text="Erklärung",
       font=("Ariel", 30),
       bg="#ffffff",
       command=open_instruktion_pdf,
       ).pack(anchor="w",fill="x",  pady=5)

# Button for idk tbh
Button(MenuFrame,text="Beenden",
       font=("Ariel", 30),
       bg="#ffffff",
       command=sys.exit,
       ).pack(anchor="w",fill="x",  pady=5)

Button(SelectFrame,
       text= "leck eier du leleck",
       font=("Ariel", 30),
       bg="#ffffff",
       command=sys.exit,
       ).place(x=screen_width/2,
               y=screen_height/2,
               anchor="center")

#creates a frame for checkboxes
maincheckboxframe = Frame(SelectFrame, bg="#ffffff", width=screen_width/3-20, height=screen_height)
maincheckboxframe.pack_propagate(False)
maincheckboxframe.place(x=screen_width/3*2)

#Checkboxes for "Bereiche"
for x in logic.uebungsbereich_auflisten():
    Checkbutton(maincheckboxframe,
                text= f"{x}",
                font=("Ariel", 30),
                bg="#ffffff",
                ).pack(anchor="w")

window.mainloop()
