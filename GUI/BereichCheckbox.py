from functools import partial
from tkinter import *
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Programmlogik import json_laden_logik


ober_dict = {}
unter_dict = {}

class BereichCheckbox:
    def __init__(self, master):
        self.master = master
        self.frame_dict = {}
        self.ausgeklappt_dict = {}
        self.checkbox_list = []

    # Funktion innerhalb der Klasse BereichCheckbox
    def update_checkbox_color(self, cb_widget, var, is_ober=False):
        """Färbt Ober-Checkbox komplett, Unter-Checkbox nur Text."""
        
        if is_ober:
            # Ober-Checkbox komplett einfärben
            if var.get() == 1:
                cb_widget.config(bg="#E0470A", fg="#ffffff")
            else:
                cb_widget.config(bg="#aaaaaa", fg="#000000")
        else:
            # Unter-Checkbox → NUR Textfarbe ändern
            if var.get() == 1:
                cb_widget.config(fg="#E0470A")  # orange
            else:
                cb_widget.config(fg="#000000")  # schwarz
            
    # Creates canvas with checkboxes
    def create(self,color):
        canvas_for_checkbox = Canvas(self.master, height=432)
        vertical_scrollbar = Scrollbar(self.master, command=canvas_for_checkbox.yview)
        main_checkbox_frame = Frame(canvas_for_checkbox, bg=color)
        canvas_for_checkbox.create_window((0,0),anchor="nw" ,  window=main_checkbox_frame)
        canvas_for_checkbox.configure(yscrollcommand=vertical_scrollbar.set)
        vertical_scrollbar.pack(side="right", fill="y")
        canvas_for_checkbox.pack(expand=True, fill="both")



        def on_configure(event):
            canvas_for_checkbox.configure(scrollregion=canvas_for_checkbox.bbox("all"))
            canvas_for_checkbox.update_idletasks()
            canvas_for_checkbox.config(
                width=main_checkbox_frame.winfo_reqwidth()
            )
        main_checkbox_frame.bind("<Configure>", on_configure)

        # Fills checkboxes with "Uebungsbereich"
        for index, bereich in enumerate(json_laden_logik.list_uebungsbereiche()):
            frame = Frame(main_checkbox_frame, bg=color)
            self.frame_dict[f"{bereich}"] = frame
            frame.columnconfigure(1, weight=1)
            frame.pack(fill="both")
            frame2 = Frame(frame, bg="white")
            self.frame_dict[f"{bereich}2"] = frame2
            self.ausgeklappt_dict[f"{bereich}"] = IntVar(value=0)

            # Haupt-Checkbutton für Auf-/Zuklappen
            cb_ausklappen = Checkbutton(
                frame,
                text=f"{bereich}",
                font=("Arial", 30),
                bg="#ffffff",
                highlightthickness=0,
                bd=0,
                variable=self.ausgeklappt_dict[f"{bereich}"],
                onvalue=1,
                offvalue=0,
                command=partial(BereichCheckbox.ausklappen, self, bereich),
                indicatoron=False,
            )
            cb_ausklappen.grid(pady=5, padx=5, sticky=NSEW, column=1, row=0)

            # Ober-Checkbox
            ober_dict[f"{bereich}"] = IntVar(value=0)
            unter_dict[f"{bereich}"] = {}
            cb_ober = Checkbutton(
                frame,
                fg="#000000",
                variable=ober_dict[f"{bereich}"],
                onvalue=1,
                offvalue=0,
                indicatoron=False,
                selectcolor="#E0470A",
                activebackground="#E0470A",
                activeforeground="#ffffff",
                font=("Arial", 28),
                highlightthickness=0,
                bd=0,
                padx=20,
                pady=1
            )
            cb_ober.grid(pady=8, padx=8, sticky=NSEW, column=0, row=0)

            # initial einfärben
            self.update_checkbox_color(cb_ober, ober_dict[bereich], is_ober=True)

            # Farb-Update beim Klick
            def ober_command(bereich=bereich, cb=cb_ober):
                
                # Farbe der Ober-Checkbox aktualisieren
                self.update_checkbox_color(cb, ober_dict[bereich], is_ober=True)

                # Unter-Checkboxen nur setzen (ohne Farbe)
                selected = ober_dict[bereich].get()

                widgets = list(self.frame_dict[f"{bereich}2"].children.values())
                for i, (titel, var) in enumerate(unter_dict[bereich].items()):
                    var.set(selected)
                    self.update_checkbox_color(widgets[i], var)

            cb_ober.config(command=ober_command)

            # Unter-Checkboxen
            for titelindex, titel in enumerate(json_laden_logik.list_titels(bereich)):
                var = IntVar(value=0)
                unter_dict[f"{bereich}"][f"{titel}"] = var
                cb_box = Checkbutton(
                self.frame_dict[f"{bereich}2"],
                text=f"{titel}",
                font=("Arial", 15),
                bg="#ffffff",
                fg="#000000",  # <<< schwarz starten
                variable=var,
                indicatoron=False,
                onvalue=1,
                offvalue=0,
                padx=10,
                pady=5
                )
                cb_box.pack(anchor="w", pady=2, padx=5)

                # Farb-Update bei Klick
                def box_command(var=var, cb=cb_box, bereich=bereich):
                    self.update_checkbox_color(cb, var)
                    self.update_hauptkategorie(bereich)
                cb_box.config(command=box_command)
                self.update_checkbox_color(cb_box, var)  # initial

    def ausklappen(self, bereich):
        if self.ausgeklappt_dict[bereich].get() == 1:
            self.frame_dict[f"{bereich}2"].grid(sticky="W", column=1, row=1)
            # Unter-Checkboxen beim Öffnen einfärben
            widgets = list(self.frame_dict[f"{bereich}2"].children.values())
            for i, (titel, var) in enumerate(unter_dict[bereich].items()):
                self.update_checkbox_color(widgets[i], var)
        else:
            self.frame_dict[f"{bereich}2"].grid_forget()

    def toggle_unter_dict(self,bereich):
        wert = ober_dict[f"{bereich}"].get()
        for var in unter_dict[f"{bereich}"].values():
            var.set(wert)

    def update_hauptkategorie(self, haupt):
        if all(var.get() for var in unter_dict[haupt].values()):
            ober_dict[haupt].set(1)
        else:
            ober_dict[haupt].set(0)

def get_active():
    aktiv = []
    for bereich, titel_var in unter_dict.items():
        for titel, var in titel_var.items():
            if var.get() == 1:
                aktiv.append(titel)
    #for titel in aktiv:
    #    print(titel)
    return aktiv

if __name__ == "__main__":
    json_laden_logik.jsonladen()
    root = Tk()
    BereichCheckbox(root).create("#ffffff")
    root.mainloop()
