from tkinter import *       #import für tkinter

#def en Fenster
window = Tk()

window.update_idletasks()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set window size to screen size
x_pos = -9 #stat point of Window
y_pos = 0
window.geometry(f"{screen_width}x{screen_height}+{x_pos}+{y_pos}")

window.attributes("-fullscreen", False)  #fullscreen
window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False)) #Escape fullscreen exit
window.bind("<F12>", lambda e: window.attributes("-fullscreen", True))  #F12 fullscreen toggle
window.title("Rechtschreib-Tool")   #changing Title from tk to Rechtschreib-Tool
window.configure(bg="#E0470A")  #backround Farbe to SRH Farbe

'''
window.attributes("-alpha", 0.7)
'''

icon = PhotoImage(file="srhIcon.png")   #changing the tk icon to srh icon
window.iconphoto(True, icon)

MenuFrame = Frame(window, bg="#E0470A")
MenuFrame.place(x=0, y=0)

#the Label for the Icon
label1 = Label(MenuFrame, image=icon)
label1.pack(anchor="w", pady=(5, 20))
#label1.place(x=0, y=0)

label2 = Label(window,
               text="Hallo",    #adding a big Title
               font=("Ariel", 30),
               bg="#E0470A",
               fg="#ffffff")

label2.pack()

Button(MenuFrame,text="Start",
       font=("Ariel", 30),
       bg="#ffffff",
       #command=
       ).pack(anchor="w", fill="x", pady=5)

Button(MenuFrame,text="Stop",
       font=("Ariel", 30),
       bg="#ffffff",
       command="").pack(anchor="w", fill="x", pady=5)

Button(MenuFrame,text="Exit",
       font=("Ariel", 30),
       bg="#ffffff").pack(anchor="w", fill="x", pady=5)

window.mainloop()
