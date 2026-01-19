from functools import partial
from tkinter import *
import logic


class BereichCheckbox:
    def __init__(self, master):
        self.master = master
        self.var_list = []

    def create(self,color):
        main_checkbox_frame = Frame(self.master, bg=color)
        main_checkbox_frame.pack()

        # Checkboxes for "Bereiche"
        for index, x in enumerate(logic.uebungsbereich_auflisten()):
            self.var_list.append(IntVar(value=0))
            Checkbutton(main_checkbox_frame,
                        text=f"{x}",
                        font=("Ariel", 30),
                        bg="#ffffff",
                        variable=self.var_list[index],
                        onvalue=1,
                        offvalue=0,
                        command=partial(BereichCheckbox.checkbox,self, index, x),
                        ).pack(anchor="w", pady=5)

    def checkbox(self,index,x):
        print(f"{x}" if self.var_list[index].get() == 1 else f"")

if __name__ == "__main__":
    logic.jsonladen()
    root = Tk()
    BereichCheckbox(root).create("#ffffff")
    root.mainloop()