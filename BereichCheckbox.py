from functools import partial
from tkinter import *
import logic


class BereichCheckbox:
    def __init__(self, master):
        self.master = master
        self.var_list = []
        self.frame_list = []
        self.frame_list2 = []
        self.var_list2 = []
        self.var_list3 = []
        self.var_list4 = []
        self.var_list5 = []
        self.var_list6 = []
        self.var_list7 = []
        self.var_list8 = []
        self.checkbox_list = []
        self.list_list = []
        self.list_list.append(self.var_list3)
        self.list_list.append(self.var_list4)
        self.list_list.append(self.var_list5)
        self.list_list.append(self.var_list6)
        self.list_list.append(self.var_list7)
        self.list_list.append(self.var_list8)

    def create(self,color):
        main_checkbox_frame = Canvas(self.master, bg=color, scrollregion=(0,0,10000,10000))
        v = Scrollbar(self.master)
        main_checkbox_frame.config(yscrollcommand=v.set)
        v.pack(side="right", fill="y")
        v.config(command=main_checkbox_frame.yview)
        main_checkbox_frame.pack()

        # Checkboxes for "Bereiche"
        for index, x in enumerate(logic.uebungsbereich_auflisten()):
            index2 = index
            x2 = x
            frame = Frame(main_checkbox_frame, bg=color)
            self.frame_list.append(frame)
            frame.columnconfigure(1, weight=1)
            frame.pack(fill="both")
            frame2 = Frame(frame, bg=color)
            self.frame_list2.append(frame2)
            self.var_list.append(IntVar(value=0))
            Checkbutton(frame,
                        text=f"{x}",
                        font=("Ariel", 30),
                        bg="#ffffff",
                        variable=self.var_list[index],
                        onvalue=1,
                        offvalue=0,
                        command=partial(BereichCheckbox.checkbox,self, index, x),
                        indicatoron=False,
                        ).grid(pady=5, padx=5, sticky=NSEW, column=1, row=0)
            for index3, x3 in enumerate(logic.list_titels(x)):
                i_am_a_variable = self.list_list[index]
                i_am_a_variable.append(IntVar(value=0))
                box = Checkbutton(self.frame_list2[index],
                            text=f"{x3}",
                            font=("Ariel", 15),
                            bg="#ffffff",
                            variable=i_am_a_variable[index3],
                            onvalue=1,
                            offvalue=0,
                            command=partial(BereichCheckbox.checkbox3, self,index, index3, x3),
                                  )
                self.checkbox_list.append(box)
                box.pack(anchor="w")
            self.var_list2.append(IntVar(value=0))
            Checkbutton(frame,
                        font=("Ariel", 30),
                        bg="#ffffff",
                        variable=self.var_list2[index2],
                        onvalue=1,
                        offvalue=0,
                        command=partial(BereichCheckbox.checkbox2, self, index2, x2),
                        ).grid(pady=5, padx=5,sticky=NSEW, column=0, row=0)

    def checkbox(self,index,x):
        if self.var_list[index].get() == 1:
            self.frame_list2[index].grid(sticky="W",column=1, row=1)
        else:
            self.frame_list2[index].grid_forget()

    def checkbox2(self,index2,x2):
        print(f"{x2} {index2}" if self.var_list2[index2].get() == 1 else f"omg")

    def checkbox3(self,index, index3,x3):
        i_am_a_variable = self.list_list[index]
        print(f"{x3} {index3}" if i_am_a_variable[index3].get() == 1 else f"omg")

if __name__ == "__main__":
    logic.jsonladen()
    root = Tk()
    BereichCheckbox(root).create("#ffffff")
    root.mainloop()