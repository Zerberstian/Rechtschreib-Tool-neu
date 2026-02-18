from tkinter import *
from tkinter import messagebox
from tkinter import colorchooser
import sys
import os
sys.path.insert(0, os.path.dirname(__file__) + "/..")  # Used for imports like "from Programmlogik import logic2"
project_root = os.path.dirname(os.path.dirname(__file__))  # Used for defining file directories
from GUI.BereichCheckbox import BereichCheckbox

# logic_der_zweite.jsonladen()
# Json must be in directory

def on_value_change():
    try:
        print(f"{spinbox.get()} = Wert in Spinbox")  # Print for debugging purposes
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
    return spinbox.get()

# Max 10 questions -> quickselct (logic)
def callback_value_10():
    spinbox.delete(0, END)
    spinbox.insert(0, 10)

# Max 100 questions -> quickselect (logic)
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
        start_logic()
'''
        aktiv = BereichCheckbox.get_active()
        if not aktiv  == []:
            start_logic()
            for a in logic_der_zweite.list_uebungen(aktiv): print(a)
        else:
            messagebox.showerror("Fehlende Auswahl",
                                    "Es wurde kein Aufgabenbereich ausgewählt.")
'''

def to_start():
    combined_command()

# Main style constants
BG_Farbe = "#E0470A"        #Background Color Value (general)
Btn_BG_Farbe = "#ffffff"    #Background Color (all Btn except Spinbox & Buttons)
Btn_FG_Farbe = "#000000"    #BUtton fg Color
BtnFontArt = "Arial"        #Button Font Style (all Btn)
BtnFontGroesse = 30         #Button Font size (all Btn)
inside_Padding_Y = 0       #Button Inside pady Value (Main Menu)

# Defining window
window = Tk()
window.update_idletasks()

# Spacing within the Window
window.grid_rowconfigure(0, weight=2)
window.grid_columnconfigure(0, weight=2)
window.grid_rowconfigure(1, weight=3)
window.grid_columnconfigure(1, weight=3)

# Generating fullscreen with a little offset to avoid taskbar issues
x_pos = -9
y_pos = 0
window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}+{x_pos}+{y_pos}")

# Window-settings
window.minsize(1100, 650)
window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False))              # Escape = exit fullscreen
window.bind("<F12>", lambda e: window.attributes("-fullscreen", True))                  # F12 = enter fullscreen
window.title("Rechtschreibtool")                                                        # changing Title from tk to Rechtschreibtool
window.configure(bg=BG_Farbe)                                                           # backround Color to SRH Color
icon_path = os.path.join(project_root, "Assets", "srhIcon.png")
icon = PhotoImage(file=icon_path)
window.iconphoto(True, icon)                                          # Changing the tk icon to srh icon
window.iconphoto(True, icon)

window.bind("<F4>", lambda event: show_color_picker())
# ^ Hotkey for swaping Menu bc im genuinely about to crash out if i have to press Farbenwahl one more Time
window.bind("<F3>", lambda event: back_to_main_frame())
# ^ back to main Menu Hotkey

# Changing between frames
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
    ColorPickerFrame.grid_forget()

def open_instruction_pdf():
    project_root = os.path.dirname(os.path.dirname(__file__))
    pdf_path = os.path.join(project_root, "Assets", "A.pdf")
    if sys.platform.startswith("win"):
        os.startfile(pdf_path)

def show_color_picker():
    MenuFrame.grid_forget()
    MenuText.grid_forget()
    headline.grid_forget()
    ColorPickerFrame.grid(row=0, column=0, sticky=NW, ipadx=5)
    ColorPickerBackFrame.grid(row=0, column=1, sticky=NW, ipadx=5)
    ColorExampleFrame.grid(row=1, column=3, sticky=NW, ipadx=5)
    ColorPickerButtonFrame.grid(row=1, column=1, sticky=NSEW, ipadx=5, pady=30, padx=5)
'''
def pick_color_fg():
    color = colorchooser.askcolor(title="Farbe auswählen")
    if color[1]:
        MenuText.config(fg=color[1])
        for widget in MenuFrame.winfo_children():
            if isinstance(widget, Button):
                widget.config(fg=color[1])
        for widget in CheckBoxFrameS.winfo_children():
            if isinstance(widget, Button):
                widget.config(fg=color[1])
        for widget in ButtonFrameSB.winfo_children():
            if isinstance(widget, Button):
                widget.config(fg=color[1])
        for widget in SpinBoxFrame.winfo_children():
            if isinstance(widget, (Button, Label)):
                widget.config(fg=color[1])
            if isinstance(widget, Spinbox):
                widget.config(fg=color[1])
        for widget in ColorPickerFrame.winfo_children():
            if isinstance(widget, Button):
                widget.config(fg=color[1])
        for widget in ColorPickerButtonFrame.winfo_children():
            if isinstance(widget, Button):
                widget.config(fg=color[1])
'''

selected_bg_color = None
selected_fg_color = None
print(f"{selected_bg_color} (def None bg)")
print(f"{selected_fg_color} (def None fg)")

def pick_color_test_fg():
    global selected_fg_color

    color = colorchooser.askcolor()
    if color[1]:
        selected_fg_color = color[1]
        print(f"{selected_fg_color} pick_color_test_fg")

        for widget in ColorExampleFrame.winfo_children():
            try:
                widget.config(fg=selected_fg_color)
            except TclError:
                pass

def pick_color_test_bg():
    global selected_bg_color

    color = colorchooser.askcolor(title="Farbe auswählen")
    if color[1]:  # Hex value
        selected_bg_color = color[1]  # Save it
        print(f"{selected_bg_color} pick_color_test_bg")
        # Preview only
        ColorExampleFrame.config(bg=selected_bg_color)
        for widget in ColorExampleFrame.winfo_children():
            widget.config(bg=selected_bg_color)
        headline.config(bg=selected_bg_color, fg=selected_bg_color)

def apply_bg_color(color):
    def update_widgets(widget):
        # Only change bg for specific widget types
        if isinstance(widget, (Label, Frame)) or widget == window:
            try:
                widget.config(bg=color)

            except Exception:
                pass
        # Still recurse through children
        for child in widget.winfo_children():
            update_widgets(child)
    update_widgets(window)

def apply_fg_color(color):
    def update_widgets(widget):
        # Only change bg for specific widget types
        if isinstance(widget, Label):
            try:
                widget.config(fg=color)

            except Exception:
                pass
        # Still recurse through children
        for child in widget.winfo_children():
            update_widgets(child)
    update_widgets(window)

def pick_color_all():
    global selected_bg_color
    print(f"{selected_bg_color} pick_color_all")
    if selected_bg_color is not None: # Only if a color was chosen
        print("oi oi")
        apply_bg_color(selected_bg_color)
        print(BG_Farbe, "bg in all")
    elif selected_fg_color is not None:
        apply_fg_color(selected_fg_color)
        headline.config(fg=BG_Farbe)
    else:
        print("omegalul")

def reset_all_color():
    global BG_Farbe
    default_bg = BG_Farbe
    print(default_bg, "default")
    headline.config(bg=default_bg, fg=default_bg)
    def update_widgets_in_reset(widget):
        if isinstance(widget, (Label, Frame)) or widget == window:
            try:
                widget.config(bg=default_bg)

            except Exception:
                print("Error xD")
                pass

        for child in widget.winfo_children():
            update_widgets_in_reset(child)
    update_widgets_in_reset(window)  # Start recursion here

# Frames
##############################################################################
# Main window frame
MenuFrame = Frame(window, bg=BG_Farbe)
MenuFrame.grid(row=0, column=0, rowspan=2, sticky=NW, ipadx=5)

# Window for taskselection
SelectFrame = Frame(window, bg=BG_Farbe)

# Frame for managing grid
CheckBoxFrameS = Frame(SelectFrame, bg=BG_Farbe)
CheckBoxFrameS.grid(row=1, column=1, sticky=N)

# Frame for managing grid
ButtonFrameSB = Frame(SelectFrame, bg=BG_Farbe)
ButtonFrameSB.grid(row=0, column=0, sticky=NW)

# Frame for spinbox and buttons
SpinBoxFrame = Frame(SelectFrame, bg=BG_Farbe)
SpinBoxFrame.grid(row=1, column=2, rowspan=1, sticky=NW)

logicFrame  =   Frame(window, bg=BG_Farbe)

AufgabenFrameSeite = Frame(window, bg=BG_Farbe)

ColorPickerFrame = Frame(window, bg=BG_Farbe)

ColorPickerButtonFrame = Frame(ColorPickerFrame, bg=BG_Farbe)

ColorPickerBackFrame = Frame(ColorPickerFrame, bg=BG_Farbe)

ColorExampleFrame = Frame(ColorPickerFrame, bg="#ffffff")


##############################################################################

SelectFrame.grid_rowconfigure(0, weight=1)
SelectFrame.grid_columnconfigure(0, weight=1)

SelectFrame.grid_rowconfigure(1, weight=2)
SelectFrame.grid_columnconfigure(1, weight=4)

SelectFrame.grid_rowconfigure(2, weight=1)
SelectFrame.grid_columnconfigure(2, weight=0)

# Label for spacing
voidLabel = Label(SelectFrame, bg=BG_Farbe)
voidLabel.grid(row=0, column=1, sticky=NW)

# Iconlabel
iconLabel = Label(MenuFrame, image=icon, bg=Btn_BG_Farbe)
iconLabel.pack(anchor="w", pady=(5, 15), fill="x")

# Adding a big title
headline = Label(window,
                text="",
                font=(BtnFontArt, BtnFontGroesse),
                bg=BG_Farbe,
                fg=BG_Farbe)

headline.grid(row=0,column=1, sticky=N)

MenuText = Label(window,
                    text= f"Die offizielle und\n"         # Adding a Label with Text in the Center
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
        fg=Btn_FG_Farbe,
        command=show_select_frame,
        ).pack(anchor="w",fill="x", pady=5, ipady=inside_Padding_Y)

# Button to open the color picker
Button(MenuFrame,
        text="Farbwahl",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=show_color_picker
        ).pack(anchor="w",fill="x", pady=5)

# Button for going back to Main Menu
Button(ButtonFrameSB,
        text="zurück",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=back_to_main_frame,
        ).pack(anchor="w" ,fill="x", pady=5, padx=5)

# Button for going back to Main Menu
Button(ColorPickerBackFrame,
        text="zurück",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=back_to_main_frame,
        ).grid(row=0, column=0, pady=5, padx=5)

# Button for going back to Main Menu
Button(logicFrame,
        text="zurück",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=back_to_main_frame,
        ).grid(row=3, column=3, padx=5, pady=5)

Button(ColorPickerButtonFrame,
        text="Hintergrund",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=lambda: pick_color_test_bg()).pack(anchor="w",fill="x", pady=5, padx=5)

Button(ColorPickerButtonFrame,
        text="Textfarbe",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=lambda: pick_color_test_fg()).pack(anchor="w",fill="x", pady=5, padx=5)

Button(ColorPickerButtonFrame,
        text="reset color",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=lambda: reset_all_color()
        ).pack(anchor="w",fill="x", pady=5, padx=5)

Button(ColorPickerButtonFrame,
        text="anwenden",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=lambda: pick_color_all()
        ).pack(anchor="w",fill="x", pady=5, padx=5)

Label(ColorExampleFrame,
        text=f"Nomen-Verb-Adjektiv Teil 1\n",
        font=(BtnFontArt, BtnFontGroesse),
        bg="#ffffff",
        fg="#000000").pack(anchor="n", pady=5, padx=5)

Label(ColorExampleFrame,
        text=f"Bitte die drei folgenden Wortarten unterscheiden:\nNomen = geben den Begriffen einen Namen: Ewigkeit, Geist, Mathematik\nVerben = alles was man tun kann: essen, läuft, malt, denkst\nAdjektive = beschreiben wie etwas ist: rot, warm, lang, schwer, eklig\n",
        font=(BtnFontArt, 20),
        bg="#ffffff",
        fg="#000000").pack(anchor="n", pady=5, padx=5)

ColorExampleButtonFrame = Frame(ColorExampleFrame, bg="#ffffff")
ColorExampleButtonFrame.pack(anchor="n", pady=5, padx=5)

button1 = Button(
    ColorExampleButtonFrame,
    text="Nomen",
    font=(BtnFontArt, BtnFontGroesse),
)
button1.pack(side="left", pady=5, padx=5)

button1.config(state=DISABLED)

button2 = Button(ColorExampleButtonFrame,
        text="Verb",
        font=(BtnFontArt, BtnFontGroesse),
        )
button2.pack(side="left", pady=5, padx=5)
button2.config(state=DISABLED)

button3 = Button(ColorExampleButtonFrame,
        text="Adjektiv",
        font=(BtnFontArt, BtnFontGroesse),
        )
button3.pack(side="left", pady=5, padx=5)
button3.config(state=DISABLED)

# Max 10 questions -> quickselct (logic)
Button(SpinBoxFrame,
        text="10",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=callback_value_10,
        ).grid(row=3, column=0, padx=5, pady=5, ipadx=15)

# Max 100 questions -> quickselct (logic)
Button(SpinBoxFrame,
        text="100",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=callback_value_100,
        ).grid(row=3,
            column=1,
            padx=5,
            pady=5)

# Button for explaination of the programm (it opens the PDF in same folder as the files)
Button(MenuFrame,
        text="Erklärung",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=open_instruction_pdf,
        ).pack(anchor="w",
            fill="x",
            pady=5,
            ipady=inside_Padding_Y)

# sys exit
Button(MenuFrame,
        text="Beenden",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=sys.exit,).pack(anchor="w",
                                fill="x",
                                pady=5,
                                ipady=inside_Padding_Y)
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
spinbox.insert(0, 10)  # Setting default value to 10

spinbox.grid(row=2,
                column=0,
                columnspan=2,
                pady=5,
                ipadx=23)

# Logic + extras
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

# Creating checkboxes
BereichCheckbox(CheckBoxFrameS).create("#ffffff")

'''
Franzosen Grrr
щ(゜ロ゜щ)
jk
'''

if __name__ == "__main__":
    window.mainloop()
