import sys
import os

# dynamic base-path (important when trying to create .exe)
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# relative import of the modules (relative regarding BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'GUI'))
sys.path.insert(0, os.path.join(BASE_DIR, 'Programmlogik'))
sys.path.insert(0, os.path.join(BASE_DIR, 'Aufgabeneditor'))
sys.path.insert(0, BASE_DIR)

from GUI.GUI_new import *  # importing GUI completely
from GUI.BereichCheckbox import BereichCheckbox
try:
    from Programmlogik.logic_der_zweite import list_uebungen
    from Programmlogik.aufgaben_logik import *
except ImportError:
    print("Warnung: Programmlogik Module nicht gefunden")

if __name__ == "__main__":
    window.mainloop()  # starting GUI only testing...


# to create the executable simply install pyinstaller via 'pip install pyinstaller' and then run the following command in the terminal; same directory as main.py:

'''python -m PyInstaller --onefile --windowed --name "RechtschreibTool" --add-data "Assets;Assets" --add-data "../Aufgabenkatalog;Aufgabenkatalog" --add-data "GUI;GUI" --add-data "Programmlogik;Programmlogik" --add-data "Aufgabeneditor;Aufgabeneditor" --icon "Assets/srhIcon.png" --hidden-import "GUI.BereichCheckbox" --hidden-import "Programmlogik.logic_der_zweite" main.py'''