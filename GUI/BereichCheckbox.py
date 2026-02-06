#used to create the BereichCheckbox as packable Widget
from functools import partial
from tkinter import *
from Programmlogik import logic2

ober_dict = {}
unter_dict = {}



class BereichCheckbox:
    def __init__(self, master):
        self.master = master
        self.frame_dict = {}
        self.ausgeklappt_dict = {}
        self.checkbox_list = []

    def create(self,color):
        canvas_for_checkbox = Canvas(self.master, height=432)
        vertikale_scrollbar = Scrollbar(self.master, command=canvas_for_checkbox.yview)
        main_checkbox_frame = Frame(canvas_for_checkbox, bg=color)
        canvas_for_checkbox.create_window((0,0),anchor="nw" ,  window=main_checkbox_frame)
        canvas_for_checkbox.configure(yscrollcommand=vertikale_scrollbar.set)
        vertikale_scrollbar.pack(side="right", fill="y")
        canvas_for_checkbox.pack(expand=True, fill="both")

        def on_configure(event):
            canvas_for_checkbox.configure(scrollregion=canvas_for_checkbox.bbox("all"))

            canvas_for_checkbox.update_idletasks()
            canvas_for_checkbox.config(
                width=main_checkbox_frame.winfo_reqwidth()
            )

        main_checkbox_frame.bind("<Configure>", on_configure)

        # Checkboxes for "Bereiche"
        for index, bereich in enumerate(logic2.uebungsbereich_auflisten()):
            frame = Frame(main_checkbox_frame, bg=color)
            self.frame_dict[f"{bereich}"] = frame
            frame.columnconfigure(1, weight=1)
            frame.pack(fill="both")
            frame2 = Frame(frame, bg="white")
            self.frame_dict[f"{bereich}2"] = frame2
            self.ausgeklappt_dict[f"{bereich}"]=IntVar(value=0)
            Checkbutton(frame,
                        text=f"{bereich}",
                        font=("Arial", 30),
                        bg="#ffffff",
                        variable=self.ausgeklappt_dict[f"{bereich}"],
                        onvalue=1,
                        offvalue=0,
                        command=partial(BereichCheckbox.ausklappen,self, bereich),
                        indicatoron=False,
                        ).grid(pady=5, padx=5, sticky=NSEW, column=1, row=0)

            ober_dict[f"{bereich}"] = IntVar(value=0)
            unter_dict[f"{bereich}"] = {}
            Checkbutton(frame,
                        bg="#ffffff",
                        variable=ober_dict[f"{bereich}"],
                        onvalue=1,
                        offvalue=0,
                        command=partial(BereichCheckbox.toggle_unter_dict, self, bereich),
                        ).grid(pady=5, padx=5,sticky=NSEW, column=0, row=0)
            for titelindex, titel in enumerate(logic2.list_titels(bereich)):
                var = IntVar(value=0)
                unter_dict[f"{bereich}"][f"{titel}"] = var
                box = Checkbutton(self.frame_dict[f"{bereich}2"],
                            text=f"{titel}",
                            font=("Arial", 15),
                            bg="#ffffff",
                            variable=var,
                            onvalue=1,
                            offvalue=0,
                            command=partial(BereichCheckbox.update_hauptkategorie, self, bereich),
                                )
                self.checkbox_list.append(box)
                box.pack(anchor="w")


    def ausklappen(self,bereich):
        if self.ausgeklappt_dict[f"{bereich}"].get() == 1:
            self.frame_dict[f"{bereich}2"].grid(sticky="W",column=1, row=1)
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
    logic2.jsonladen()
    root = Tk()
    BereichCheckbox(root).create("#ffffff")
    root.mainloop()
