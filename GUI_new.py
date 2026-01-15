from tkinter import *       #import for tkinter
import os                   #import for Operating System
import sys                  #impoer system
#from test2 import uebungsbereich_auflisten, aufgabenListe

##
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
window.title("Rechtschreib-Tool")                                                       #changing Title from tk to Rechtschreib-Tool
window.configure(bg="#E0470A")                                                          #backround Color to SRH Color

'''
window.attributes("-alpha", 0.7)
'''

#changing the tk icon to srh icon
icon = PhotoImage(file="srhIcon.png")
window.iconphoto(True, icon)

def show_select_frame():
    MenuFrame.place_forget()
    label2.pack_forget()
    SelectFrame.place(x=0, y=0,relwidth=1, relheight=1)
    #SelectUebungFrame.place(x=screen_width/2, y=screen_height/2)

def back_to_main_frame():
    MenuFrame.place(x=0, y=0)
    SelectFrame.place_forget()
    #SelectUebungFrame.place_forget()
    label2.pack()

def open_instruktion_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), "A.pdf")

    if sys.platform.startswith("win"):
        os.startfile(pdf_path)


#the Main Menu Frame
MenuFrame = Frame(window, bg="#E0470A")
MenuFrame.place(x=0, y=0)

#the Frame to select your
SelectFrame = Frame(window, bg="#E0470A")

#SelectUebungFrame = Frame(SelectFrame, bg="#E0470A")

#the Label for the Icon
label1 = Label(MenuFrame, image=icon)
label1.pack(anchor="w", pady=(5, 20))


label2 = Label(window,
               text="Hallo",    #adding a big Title
               font=("Ariel", 30),
               bg="#E0470A",
               fg="#ffffff")

label2.pack()

# Button for starting the select options
Button(MenuFrame,text="Start",
       font=("Ariel", 30),
       bg="#ffffff",
       command=show_select_frame,
       ).pack(anchor="w",fill="x", pady=5)


#Button for going back to Main Menu

Button(SelectFrame,text="zurück",
       font=("Ariel", 30),
       bg="#ffffff",
       command=back_to_main_frame,
       ).pack(anchor="w", pady=5)

# Button for idk tbh
Button(MenuFrame,text="Erklärung",
       font=("Ariel", 30),
       bg="#ffffff",
       command=open_instruktion_pdf,
       ).pack(anchor="w",fill="x",  pady=5)

'''
# Button for idk tbh
Button(MenuFrame,text="Exit",
       font=("Ariel", 30),
       bg="#ffffff",
       command="",
       ).pack(anchor="w",fill="x",  pady=5)
'''

Button(SelectFrame,text= "leck eier du leleck",
       font=("Ariel", 30),
       bg="#ffffff",
       command="",
       ).place(x=screen_width/2, y=screen_height/2, anchor="center")

#,relx=0.5, rely=0.5,

window.mainloop()
