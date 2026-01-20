from tkinter import *       #import for tkinter
import os                   #import for Operating System
import sys                  #import system
import logic                #import logic.py
import BereichCheckbox      #import BereichCheckbox.py

logic.jsonladen()  #load aufgaben.json (must be in directory)

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


def open_instruktion_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), "A.pdf")

    if sys.platform.startswith("win"):
        os.startfile(pdf_path)

#the Main Menu Frame
MenuFrame = Frame(window, bg="#E0470A")
MenuFrame.grid(row=0, column=0, rowspan=2, sticky=NW, ipadx=5)

#the Frame to select your
SelectFrame = Frame(window, bg="#E0470A")

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

MenuText = Label(window, text= f"Die offizielle und\n"         #adding a Label with Text in the Center
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
Button(SelectFrame,
       text="zurück",
       font=("Ariel", 30),
       bg="#ffffff",
       command=back_to_main_frame,
       ).place(x=0, y=0)

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

#creates a frame for checkboxes
BereichCheckbox.BereichCheckbox(SelectFrame).create("#ffffff")

window.mainloop()
