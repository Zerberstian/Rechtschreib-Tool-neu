import sys
import os
sys.path.insert(0, os.path.dirname(__file__) + "/..")  # Used for imports like "from Programmlogik import logic2"
project_root = os.path.dirname(os.path.dirname(__file__))  # Used for defining file directories
from Programmlogik import aufgaben_logik
from GUI.BereichCheckbox import BereichCheckbox, get_active
from GUI import Frame_Generation_Class
from typing import Any, Callable
import tkinter as tk
from tkinter import messagebox, colorchooser

BtnFontArt: str = "Arial"        #Button Font Style (all Btn)

def on_value_change() -> str:
    try:
        print(f"{spinbox.get()} = Wert in Spinbox")  # Print for debugging purposes
        if int(spinbox.get()) > 100:
            spinbox.delete(0, tk.END) # type: ignore
            spinbox.insert(0, "100")

        elif int(spinbox.get()) < 1:
            spinbox.delete(0, tk.END) # type: ignore
            spinbox.insert(0, "1")

    except ValueError:
        messagebox.showerror("Ungültige Eingabe",
                                "Start mit Standardwert für Aufgabenmenge (10).")
        spinbox.delete(0, tk.END) # type: ignore
        spinbox.insert(0, "10")
        print(spinbox.get(), "bei ungültiger spinbox.get()")
    return spinbox.get()

# Max 10 questions -> quickselct (logic)
def callback_value_10() -> None:
    spinbox.delete(0, tk.END) # type: ignore
    spinbox.insert(0, "10")

# Max 100 questions -> quickselect (logic)
def callback_value_100() -> None:
    spinbox.delete(0, tk.END) # type: ignore
    spinbox.insert(0, "100")

def start_logic() -> None:
    print("Start der logik")
    print(spinbox.get(), "= value check 2")
    aufgaben_logik.aufgaben_initialisieren(int(on_value_change()))
    show_start_frame()
    Frame_Generation_Class.aufgaben_frame_generation(logicFrame, BtnFontArt)

    #aufgaben_logik.aufgaben_anfangen_konsole()
    #aufgaben_logik.statistik_ausgeben()

def to_start() -> None:
    on_value_change()
    print(spinbox.get(), "= value check 1")
    aktiv = get_active()
    if not aktiv  == []:
        start_logic()
    else:
        messagebox.showerror("Fehlende Auswahl",
                                "Es wurde kein Aufgabenbereich ausgewählt.")


# Main style constants
BG_Farbe: str = "#E0470A"     #Background Color Value (general)
Btn_BG_Farbe: str = "#E0470A" #Background Color (all Btn except Spinbox & Buttons)
Btn_FG_Farbe: str = "#FFFFFF" #BUtton fg Color

BtnFontGroesse: int = 30        #Button Font size (all Btn)
inside_Padding_Y: int = 0       #Button Inside pady Value (Main Menu)

# Defining window
window: tk.Tk = tk.Tk()
window.update_idletasks()

# Spacing within the Window
window.grid_rowconfigure(0, weight=2)
window.grid_columnconfigure(0, weight=2)
window.grid_rowconfigure(1, weight=3)
window.grid_columnconfigure(1, weight=3)

# Generating fullscreen with a little offset to avoid taskbar issues
x_pos: int = -9
y_pos: int = 0
window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}+{x_pos}+{y_pos}")

# Window-settings
window.minsize(1100, 650)
window.bind("<Escape>", lambda e: set_fullscreen(window, False))
window.bind("<F12>", lambda e: set_fullscreen(window, True))
window.title("Rechtschreibtool")
window.configure(bg=BG_Farbe) # backround Color to SRH Color

icon_window_path = os.path.join(project_root, "Assets", "srhIcon.ico" \
"")
window.iconbitmap(icon_window_path) # type: ignore

icon_path = os.path.join(project_root, "Assets", "srhIcon2.png")
icon = tk.PhotoImage(file=icon_path)
'''
window.bind("<F4>", lambda event: show_color_picker())
# ^ Hotkey for swaping Menu bc im genuinely about to crash out if i have to press Farbenwahl one more Time
window.bind("<F3>", lambda event: back_to_main_frame())
# ^ back to main Menu Hotkey
'''
# Changing between frames
def show_start_frame() -> None:
    logicFrame.grid(row=0, column=0, sticky=tk.NW)
    SelectFrame.place_forget()

def show_select_frame() -> None:
    MenuFrame.grid_forget()
    headline.grid_forget()
    SelectFrame.place(x=0, y=0, relwidth=1, relheight=1)
    MenuText.grid_forget()

def back_to_main_frame() -> None:
    MenuFrame.grid(row=0, column=0, rowspan=2, sticky=tk.NW)
    SelectFrame.place_forget()
    headline.grid(row=0,column=1, sticky=tk.N)
    MenuText.grid(row=1,column=1, sticky=tk.NW)
    logicFrame.grid_forget()
    ColorPickerFrame.grid_forget()
    
    try :
        Frame_Generation_Class.statistik_frame_list[-1].stats_hide()
    except IndexError:
        pass
    for frame in Frame_Generation_Class.aufgaben_frame_dict:
        Frame_Generation_Class.aufgaben_frame_dict[frame].hide()
    Frame_Generation_Class.reset()
    aufgaben_logik.resetting()

def set_fullscreen(win: tk.Tk, state: bool) -> None:
    win.attributes("-fullscreen", state) # type: ignore

def open_instruction_pdf() -> None:
    project_root = os.path.dirname(os.path.dirname(__file__))
    pdf_path = os.path.join(project_root, "Assets", "A.pdf")
    if sys.platform.startswith("win"):
        os.startfile(pdf_path)

def show_color_picker() -> None:
    MenuFrame.grid_forget()
    MenuText.grid_forget()
    headline.grid_forget()
    ColorPickerFrame.grid(row=0, column=0, sticky=tk.NW, ipadx=5)
    ColorPickerBackFrame.grid(row=0, column=1, sticky=tk.NW, ipadx=5)
    ColorExampleFrame.grid(row=1, column=3, sticky=tk.NW, ipadx=5)
    ColorPickerButtonFrame.grid(row=1, column=1, sticky=tk.NSEW, ipadx=5, pady=30, padx=5)

selected_bg_color = None
selected_fg_color = None
print(f"{selected_bg_color} (def None bg)")
print(f"{selected_fg_color} (def None fg)")

def pick_color_test_fg() -> None:
    global selected_fg_color
    color = colorchooser.askcolor()
    if color[1]:
        selected_fg_color = color[1]
        print(f"{selected_fg_color} pick_color_test_fg")
        for widget in ColorExampleFrame.winfo_children():
            try:
                widget.config(fg=selected_fg_color) # type: ignore
            except tk.TclError:
                pass

def pick_color_test_bg() -> None:
    global selected_bg_color
    color = colorchooser.askcolor(title="Farbe auswählen")
    if color[1]:
        selected_bg_color = color[1]
        print(f"{selected_bg_color} pick_color_test_bg")
        # Preview only
        ColorExampleFrame.config(bg=selected_bg_color)
        for widget in ColorExampleFrame.winfo_children():
            widget.config(bg=selected_bg_color) # type: ignore
        headline.config(bg=selected_bg_color, fg=selected_bg_color)

def apply_color(widget: tk.Tk | tk.Widget, bg: str | None = None, fg: str | None = None) -> None:
    try:
        if bg is not None and (isinstance(widget, (tk.Label, tk.Frame))
                               or widget is window): # type: ignore
            widget.config(bg=bg) # type: ignore

        if fg is not None and isinstance(widget, tk.Label):
            widget.config(fg=fg) # type: ignore

    except Exception:
        pass

    # Recurse through children
    for child in widget.winfo_children():
        apply_color(child, bg=bg, fg=fg) # type: ignore

def pick_color_all():
    print(f"{selected_bg_color} pick_color_all")
    if selected_bg_color is not None:
        print("oi oi")
        apply_color(window, bg=selected_bg_color)
        print(BG_Farbe, "bg in all")
    elif selected_fg_color is not None:
        apply_color(window, fg=selected_fg_color)
        headline.config(fg=BG_Farbe)
    else:
        print("omegalul")
'''
def reset_all_color(): #global
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

def reset_to_default_design(widget):
    default_bg_white = "#ffffff"
    ColorExampleFrame.config(bg=default_bg_white)
    if isinstance(widget, (Label, Frame)):
        try:
            widget.config(bg=default_bg_white)
            print("Troll lol lol lol lol loloho")
        except Exception:
            print("Error2 xD")
            pass
    for widget in ColorExampleFrame.winfo_children():
        reset_to_default_design(widget)

def reset_and_default(widget):
    reset_all_color()
    for widget in ColorExampleFrame.winfo_children():
        reset_to_default_design(widget)
'''
def reset_all_color():
    global BG_Farbe
    default_bg = BG_Farbe
    print(default_bg, "default")
    headline.config(bg=default_bg, fg=default_bg)
    def update_widgets_in_reset(widget):
        if isinstance(widget, (tk.Label, tk.Frame)) or widget == window:
            try:
                widget.config(bg=default_bg)
            except Exception:
                pass
        for child in widget.winfo_children():
            update_widgets_in_reset(child)
    update_widgets_in_reset(window)

def reset_to_default_design(widget):
    default_bg_white = "#ffffff"
    ColorExampleFrame.config(bg=default_bg_white)
    if isinstance(widget, (tk.Label, tk.Frame)):
        try:
            widget.config(bg=default_bg_white)
        except Exception:
            pass
    for child in widget.winfo_children():
        reset_to_default_design(child)

def reset_and_default(widget):
    reset_all_color()
    for child in ColorExampleFrame.winfo_children():
        reset_to_default_design(child)

# Frames
##############################################################################
# Main window frame
MenuFrame = tk.Frame(window, bg=BG_Farbe)
MenuFrame.grid(row=0, column=0, rowspan=2, sticky=tk.NW, ipadx=5)

# Window for taskselection
SelectFrame = tk.Frame(window, bg=BG_Farbe)

# Frame for managing grid
CheckBoxFrameS = tk.Frame(SelectFrame, bg=BG_Farbe)
CheckBoxFrameS.grid(row=1, column=1,  sticky=tk.N)

# Frame for managing grid
ButtonFrameSB = tk.Frame(SelectFrame, bg=BG_Farbe)
ButtonFrameSB.grid(row=0, column=0, sticky=tk.NW)

# Frame for spinbox and buttons
SpinBoxFrame: tk.Frame = tk.Frame(SelectFrame, bg=BG_Farbe)
SpinBoxFrame.grid(row=1, column=2, rowspan=1, sticky=tk.NW)

logicFrame  =   tk.Frame(window, bg=BG_Farbe)

AufgabenFrameSeite = tk.Frame(window, bg=BG_Farbe)

ColorPickerFrame = tk.Frame(window, bg=BG_Farbe)

ColorPickerButtonFrame = tk.Frame(ColorPickerFrame, bg=BG_Farbe)

ColorPickerBackFrame = tk.Frame(ColorPickerFrame, bg=BG_Farbe)

ColorExampleFrame = tk.Frame(ColorPickerFrame, bg="#ffffff")

statisticFrame = tk.Frame(window, bg=BG_Farbe)
##############################################################################

SelectFrame.grid_rowconfigure(0, weight=1)
SelectFrame.grid_columnconfigure(0, weight=1)

SelectFrame.grid_rowconfigure(1, weight=2)
SelectFrame.grid_columnconfigure(1, weight=4)

SelectFrame.grid_rowconfigure(2, weight=1)
SelectFrame.grid_columnconfigure(2, weight=0)

# Label for spacing
voidLabel = tk.Label(SelectFrame, bg=BG_Farbe)
voidLabel.grid(row=0, column=1, sticky=tk.NW)

# Iconlabel
iconLabel = tk.Label(MenuFrame, image=icon, bg=BG_Farbe)
iconLabel.pack(anchor="w", pady=(5, 15), fill="x")

# Adding a big title
headline = tk.Label(window,
                text="",
                font=(BtnFontArt, BtnFontGroesse),
                bg=BG_Farbe,
                fg=BG_Farbe)

headline.grid(row=0,column=1, sticky=tk.N)

MenuText = tk.Label(window,
                    text= f"Die offizielle und\n"         # Adding a Label with Text in the Center
                        f"verbesserte Version\n"
                        f"des Rechtschreibtools\n"
                        f"der SRH Dresden",
                font=(BtnFontArt, 35),
                bg=BG_Farbe,
                fg="#ffffff")

MenuText.grid(row=1,column=1, sticky=tk.NW)


#defining a function for a default button
def create_button(
        parent: tk.Widget, text: str, command: Callable[[], None], **kwargs: Any) -> tk.Button:
    return tk.Button(
        parent,
        text=text,
        font=(BtnFontArt, BtnFontGroesse),
        bg="#ffffff",
        fg="#000000",
        activebackground="#f2f2f2",
        activeforeground="#000000",
        bd=0,
        highlightthickness=0,
        padx=20,
        pady=10,
        command=command,
        **kwargs  # erlaubt extra Parameter wie grid/pack später
    )

# Button for starting the select options
create_button(
    MenuFrame,
    "Start",
    show_select_frame
).pack(anchor="w", fill="x", pady=8)

'''
# Button to open the color picker
Button(MenuFrame,
        text="Farbwahl",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=show_color_picker
        ).pack(anchor="w",fill="x", pady=15)
'''
def not_ready():
    messagebox.showinfo("Info", "Aus zeitlichen Gründen wird dieses Feature zu einem späteren Zeitpunkt implementiert.")

# Button to open the color picker
create_button(
    MenuFrame,
    "Farbwah",
    not_ready
).pack(anchor="w", fill="x", pady=8)

# Button for going back to Main Menu
create_button(
    ButtonFrameSB,
    "Zurück",
    back_to_main_frame
).pack(anchor="w", fill="x", pady=8)

# Button for going back to Main Menu
tk.Button(ColorPickerBackFrame,
        text="Zurück",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=back_to_main_frame,
        ).grid(row=0, column=0, pady=15, padx=5)

# Button for going back to Main Menu
tk.Button(logicFrame,
        text="Abbrechen",
        font=(BtnFontArt, BtnFontGroesse),
        bg=BG_Farbe,
        fg=Btn_FG_Farbe,
        bd=0,
        highlightthickness=0,
        command=back_to_main_frame,
        ).grid(row=0, column=0, padx=5, pady=15)

tk.Button(ColorPickerButtonFrame,
        text="Hintergrund",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=lambda: pick_color_test_bg()).pack(anchor="w",fill="x", pady=15, padx=5)

tk.Button(ColorPickerButtonFrame,
        text="Textfarbe",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=lambda: pick_color_test_fg()).pack(anchor="w",fill="x", pady=15, padx=5)

tk.Button(ColorPickerButtonFrame,
        text="reset color",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=lambda: reset_all_color()
        ).pack(anchor="w",fill="x", pady=15, padx=5)

tk.Button(ColorPickerButtonFrame,
        text="anwenden",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=lambda: pick_color_all()
        ).pack(anchor="w",fill="x", pady=15, padx=5)

for widget in ColorPickerButtonFrame.winfo_children(): # disables all buttons in this frame
    if isinstance(widget, tk.Button):
        widget.config(state=tk.DISABLED)

tk.Label(ColorExampleFrame,
        text=f"Nomen-Verb-Adjektiv Teil 1\n",
        font=(BtnFontArt, BtnFontGroesse),
        bg="#ffffff",
        fg="#000000").pack(anchor="n", pady=15, padx=5)

tk.Label(ColorExampleFrame,
        text=f"Bitte die drei folgenden Wortarten unterscheiden:\n"
            f"Nomen = geben den Begriffen einen Namen: Ewigkeit, Geist, Mathematik\n"
            f"Verben = alles was man tun kann: essen, läuft, malt, denkst\n"
            f"Adjektive = beschreiben wie etwas ist: rot, warm, lang, schwer, eklig\n",
        font=(BtnFontArt, 20),
        bg="#ffffff",
        fg="#000000").pack(anchor="n", pady=15, padx=5)

ColorExampleButtonFrame = tk.Frame(ColorExampleFrame, bg="#ffffff")
ColorExampleButtonFrame.pack(anchor="n", pady=15, padx=5)

button1 = tk.Button(
    ColorExampleButtonFrame,
    text="Nomen",
    font=(BtnFontArt, BtnFontGroesse),
)
button1.pack(side="left", pady=15, padx=5)
button1.config(state=tk.DISABLED)

button2 = tk.Button(ColorExampleButtonFrame,
        text="Verb",
        font=(BtnFontArt, BtnFontGroesse),
        )
button2.pack(side="left", pady=15, padx=5)
button2.config(state=tk.DISABLED)

button3 = tk.Button(ColorExampleButtonFrame,
        text="Adjektiv",
        font=(BtnFontArt, BtnFontGroesse),
        )
button3.pack(side="left", pady=15, padx=5)
button3.config(state=tk.DISABLED)

# Max 10 questions -> quickselct (logic)
tk.Button(SpinBoxFrame,
        text="10",
        fg="#ffffff",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        command=callback_value_10,
        ).grid(row=3, column=0, padx=5, pady=15, ipadx=15)

# Max 100 questions -> quickselct (logic)
tk.Button(SpinBoxFrame,
        text="100",
        font=(BtnFontArt, BtnFontGroesse),
        bg=Btn_BG_Farbe,
        fg="#ffffff",
        command=callback_value_100,
        ).grid(row=3,
            column=1,
            padx=5,
            pady=15)

# Button for explaination of the programm (it opens the PDF in same folder as the files)
create_button(
    MenuFrame,
    "Erklärung",
    open_instruction_pdf
).pack(anchor="w", fill="x", pady=8)



# sys exit
create_button(
    MenuFrame,
    "Beenden",
    sys.exit
).pack(anchor="w", fill="x", pady=8)
tk.Label(SpinBoxFrame,
        bg="#E0470A",
        fg="#ffffff",
        text=f"Gib die Menge\n "
            f"an Aufgaben an:\n "
            f"(1-100)",
        font=("Arial", 18)).grid(row=0,
                                column=0,
                                columnspan=2,
                                pady=15,
                                ipadx=13)

# Spinbox
spinbox = tk.Spinbox(SpinBoxFrame,
                    from_=1,
                    to=100,
                    increment=1,
                    width=10,
                    font=("Arial", 20),
                    command=on_value_change)

spinbox.delete(0, tk.END) # type: ignore
spinbox.insert(0, str(10))  # Setting default value to 10

spinbox.grid(row=2,
                column=0,
                columnspan=2,
                pady=15,
                ipadx=23)

tk.Button(SpinBoxFrame,
        bg=BG_Farbe,
        fg="#ffffff",
        text="Start",
        bd=0,
        highlightthickness=0,
        font=(BtnFontArt, BtnFontGroesse),
        command=to_start).grid( row=4,
                                column=0,
                                columnspan=2,
                                ipadx=50,
                                padx=5,
                                pady=15,)

# Creating checkboxes
BereichCheckbox(CheckBoxFrameS).create("#ffffff")

'''
Franzosen Grrr
щ(゜ロ゜щ)
jk
'''


if __name__ == "__main__":
    window.mainloop()
