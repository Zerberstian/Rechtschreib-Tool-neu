#used to create the BereichCheckbox as packable Widget
from functools import partial
from tkinter import *
import logic

ober_dict = {}
unter_dict = {}

class BereichCheckbox:
    def __init__(self, master):
        self.master = master
        self.frame_dict = {}
        self.ausgeklappt_dict = {}
        self.checkbox_list = []

        #opinojnondodbdonehtusphhnhodhtso 9thboxthibzst xibu hstiubgth rto9gh Ich muss das ändern

    def create(self,color):
        canvas = Canvas(self.master, height=432)
        v = Scrollbar(self.master, command=canvas.yview)
        main_checkbox_frame = Frame(canvas, bg=color)
        canvas.create_window((0,0),anchor="nw" ,  window=main_checkbox_frame)
        canvas.configure(yscrollcommand=v.set)
        v.pack(side="right", fill="y")
        canvas.pack(expand=True, fill="both")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

            canvas.update_idletasks()
            canvas.config(
                width=main_checkbox_frame.winfo_reqwidth()
            )

        main_checkbox_frame.bind("<Configure>", on_configure)

        # Checkboxes for "Bereiche"
        for index, x in enumerate(logic.uebungsbereich_auflisten()):
            frame = Frame(main_checkbox_frame, bg=color)
            self.frame_dict[f"{x}"] = frame
            frame.columnconfigure(1, weight=1)
            frame.pack(fill="both")
            frame2 = Frame(frame, bg="white")
            self.frame_dict[f"{x}2"] = frame2
            self.ausgeklappt_dict[f"{x}"]=IntVar(value=0)
            Checkbutton(frame,
                        text=f"{x}",
                        font=("Arial", 30),
                        bg="#ffffff",
                        variable=self.ausgeklappt_dict[f"{x}"],
                        onvalue=1,
                        offvalue=0,
                        command=partial(BereichCheckbox.ausklappen,self, x),
                        indicatoron=False,
                        ).grid(pady=5, padx=5, sticky=NSEW, column=1, row=0)

            ober_dict[f"{x}"] = IntVar(value=0)
            unter_dict[f"{x}"] = {}
            Checkbutton(frame,
                        bg="#ffffff",
                        variable=ober_dict[f"{x}"],
                        onvalue=1,
                        offvalue=0,
                        command=partial(BereichCheckbox.toggle_unter_dict, self, x),
                        ).grid(pady=5, padx=5,sticky=NSEW, column=0, row=0)
            for index3, x3 in enumerate(logic.list_titels(x)):
                var = IntVar(value=0)
                unter_dict[f"{x}"][f"{x3}"] = var
                box = Checkbutton(self.frame_dict[f"{x}2"],
                            text=f"{x3}",
                            font=("Arial", 15),
                            bg="#ffffff",
                            variable=var,
                            onvalue=1,
                            offvalue=0,
                            command=partial(BereichCheckbox.update_hauptkategorie, self, x),
                                  )
                self.checkbox_list.append(box)
                box.pack(anchor="w")


    def ausklappen(self,x):
        if self.ausgeklappt_dict[f"{x}"].get() == 1:
            self.frame_dict[f"{x}2"].grid(sticky="W",column=1, row=1)
        else:
            self.frame_dict[f"{x}2"].grid_forget()

    def toggle_unter_dict(self,x2):
        wert = ober_dict[f"{x2}"].get()
        for var in unter_dict[f"{x2}"].values():
            var.set(wert)

    def update_hauptkategorie(self, haupt):
        if all(var.get() for var in unter_dict[haupt].values()):
            ober_dict[haupt].set(1)
        else:
            ober_dict[haupt].set(0)


def get_active():
    aktiv = []
    for bereich, titelliste in unter_dict.items():
        for titel, var in titelliste.items():
            if var.get() == 1:
                aktiv.append(titel)
    for a in aktiv:
        print(a)
    return aktiv

if __name__ == "__main__":
    logic.jsonladen()
    root = Tk()
    BereichCheckbox(root).create("#ffffff")
    root.mainloop()
