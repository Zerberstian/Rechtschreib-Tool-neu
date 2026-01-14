from tkinter import *       #import für tkinter

#def en Fenster
window = Tk()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set window size to screen size
window.geometry(f"{screen_width}x{screen_height}+0+0")
window.attributes("-fullscreen", False)  #fullsc
window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False)) #Escape fullscreen exit
window.bind("<F12>", lambda e: window.attributes("-fullscreen", True))  #F12 fullscreen toggle
window.title("Rechtschreib-Tool")   #changing Title from tk to Rechtschreib-Tool
window.configure(bg="#E0470A")  #backround Farbe to SRH Farbe

'''
window.attributes("-alpha", 0.7)
'''

icon = PhotoImage(file="srhIcon.png")   #changing the tk icon to srh icon
window.iconphoto(True, icon)

#the Label for the Icon
label1 = Label(window, image=icon)
label1.place(x=0, y=0)

label2 = Label(window, text="Hallo",    #adding a big Title
               font=("Comic Sans", 30),
               bg="#E0470A",
               fg="#ffffff")

label2.pack()

window.mainloop()
