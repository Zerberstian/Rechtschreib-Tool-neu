import tkinter as tk
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Programmlogik import aufgaben_logik
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

aufgaben_frame_dict: dict[int, "AufgabenFrame"] = {}
statistik_frame_list: list["StatistikFrame"] = []

class StatistikFrame:
    def __init__(self,
                 master: tk.Tk | tk.Frame,
                 font: str,
                 stats: tuple[list[str], list[str], list[str], str]):
        self.master = master
        self.font = font
        self.stats_der_richtigen = stats[0]
        self.stats_der_falschen = stats[1]
        self.stats_der_korrigierten = stats[2]
        self.stats_gesamt = stats[3]

        statistik_frame_list.append(self)

        self.frame = tk.Frame(self.master)
        self.frame2 = tk.Frame(self.frame)
        self.frame2.grid(row=0, column=0)
        self.frame3 = tk.Frame(self.frame)
        self.frame3.grid(row=0, column=1, ipadx=60)
        self.gesamt_label = tk.Label(self.frame2, text=self.stats_gesamt, font=self.font)
        self.gesamt_label.pack(fill="both",expand=True, padx=5, pady=5)
        self.falschen_text = tk.Text(self.frame2,
                                     font=self.font,
                                     fg="#ff1111",
                                     bg="#000000",
                                     wrap="word")
        self.falschen_text.pack(padx=5, pady=5)
        for stat in self.stats_der_falschen:
            self.falschen_text.insert(tk.END, stat)
        self.falschen_text.config(state="disabled")
        self.fig = Figure(figsize=(1, 5), dpi=100)
        self.diagramm = self.fig.add_subplot()
        self.diagramm.title.set_text("Antworten")
        self.diagramm.xaxis.set_ticks([]) # type: ignore
        self.diagramm.yaxis.set_ticks([]) # type: ignore
        bottom = 0
        width = 1
        part = self.diagramm.bar(0, # type: ignore
                                 len(self.stats_der_richtigen),
                                 width=width,
                                 label="Richtig",
                                 bottom=bottom,
                                 color="green")
        bottom += len(self.stats_der_richtigen)
        self.diagramm.bar_label(part, label_type="center") # type: ignore
        part = self.diagramm.bar(0, # type: ignore
                                 len(self.stats_der_korrigierten),
                                 width=width,
                                 label="Korrigiert",
                                 bottom=bottom,
                                 color="yellow")
        bottom += len(self.stats_der_korrigierten)
        self.diagramm.bar_label(part, label_type="center") # type: ignore
        part = self.diagramm.bar(0, # type: ignore
                                 len(self.stats_der_falschen),
                                 width=width,
                                 label="Falsch",
                                 bottom=bottom,
                                 color="red")
        self.diagramm.bar_label(part, label_type="center") # type: ignore
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame3)
        self.canvas.get_tk_widget().config()
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.diagramm.legend() # type: ignore

    def stats_show(self):
        self.frame.grid(row=1, column=1)

    def stats_hide(self):
        self.frame.grid_forget()

class AufgabenFrame:
    def __init__(self, uebung_id: str, master: tk.Tk | tk.Frame, font: str):
        self.frame_id = len(aufgaben_frame_dict)
        self.uebung_id = uebung_id
        self.master = master
        self.font = font
        self.moeglichkeiten = aufgaben_logik.aufgaben_dict[self.uebung_id].moeglichkeiten

        aufgaben_frame_dict[self.frame_id] = self

        self.frame = tk.Frame(self.master)
        self.frame2 = tk.Frame(self.frame)
        self.frame2.pack(fill="both", expand=True)

        self.__create_textbox()
        self.__create_buttons()

    def __create_buttons(self):
        self.buttonframe = tk.Frame(self.frame2)
        self.buttonframe.pack()

        aufgabe = aufgaben_logik.aufgaben_dict[self.uebung_id]
        korrekte_antwort = aufgabe.korrekt

        for index, antwort_moeglichkeit in enumerate(self.moeglichkeiten):
            btn = tk.Button(
                self.buttonframe,
                text=antwort_moeglichkeit,
                font=(self.font, 25),
                wraplength=500,
                command=lambda f=self.buttonframe,
                               antwort=index + 1,
                               korrekte=korrekte_antwort,
                               aktuelle_aufgabe=aufgabe,
                               frame_id=self.frame_id: AufgabenFrame.button_click(
                                   self,
                                   f,
                                   antwort,
                                   aktuelle_aufgabe,
                                   frame_id,
                                   korrekte,
                               ),
            )
            btn.grid(row=0, column=index, padx=1, pady=1)
    
    def __create_textbox(self) -> None:
        self.aufgabenbeschreibung_textbox = tk.Text(self.frame2,
                                                  height=11,
                                                  font=(self.font, 20),
                                                  wrap="word")
        
        self.aufgabenbeschreibung_textbox.insert(
            tk.END,
            self.uebung_id + "\n" +
            aufgaben_logik.aufgaben_dict[self.uebung_id].aufgabenbeschreibung + "\n\n" +
            aufgaben_logik.aufgaben_dict[self.uebung_id].uebungs_beschreibung)
        self.aufgabenbeschreibung_textbox.config(state="disabled")
        self.aufgabenbeschreibung_textbox.pack()

    def show(self) -> None:
        self.frame.grid(row = 1, column = 1)

    def hide(self) -> None:
        self.frame.grid_forget()

    def warten(self) -> None:
        print("Fertig warten")
        self.hide()
        aufgaben_frame_generation(self.master, self.font)

    def button_click(
            self,
            frame: tk.Frame,
            x: int,
            aufgabe: aufgaben_logik.Aufgabe,
            frame_id: int,
            korrekte_antwort: int) -> None:
        aufgaben_logik.antwort_check(x, aufgabe, frame_id)
        # Buttons einfärben
        for index, widget in enumerate(frame.winfo_children()):
            print(index)
            if isinstance(widget, tk.Button):
                print("Ist Button")
                if index + 1 == korrekte_antwort:
                    widget.config(bg="#12a505", fg="#ffffff") # richtige Antwort grün
                    print("Button Grun")
                elif index + 1 != korrekte_antwort:
                    widget.config(bg="#ff0000", fg="#ffffff") # falsche Antwort rot
                    print("Button Rot")
                widget.config(state="disabled", disabledforeground="#ffffff")
                print("Button disabled")
        frame.update()
        self.master.after(1000, self.warten)

def aufgaben_frame_generation(master: tk.Tk | tk.Frame, font: str) -> None:
    try:
        aufgabe = aufgaben_logik.zu_loesende_aufgaben_list[len(aufgaben_frame_dict)]
    except IndexError:
        reset()
        statistik_frame_generation(master, font)
        return print("Fertig mit allen Aufgaben")
    AufgabenFrame(aufgabe, master, font)

    aufgaben_frame_dict[len(aufgaben_frame_dict)-1].show()
    return print("Deine Aufgabe wurde geladen")

def statistik_frame_generation(master: tk.Tk | tk.Frame, font: str) -> None:
    StatistikFrame(master, font, aufgaben_logik.statistik_ausgeben())
    aufgaben_logik.resetting()
    statistik_frame_list[-1].stats_show()

def reset() -> None:
    aufgaben_frame_dict.clear()


if __name__ == "__main__":
    print("deutsche pass")
