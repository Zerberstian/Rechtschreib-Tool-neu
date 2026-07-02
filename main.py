# type: ignore
from Programmlogik.path import Path

# relative import of the modules (relative regarding base_dir)
Path().setup_sys_path()

from Programmlogik.json_loader import json_loader
import Programmlogik.task_logic

# Load JSON data into memory
json_loader.load_json()
# Create Aufgabe objects for all tasks
Programmlogik.task_logic.aufgaben_objekte_erstellen()

from GUI.gui_new import *  # importing GUI completely
from GUI.field_checkbox import FieldCheckbox
try:
    import Programmlogik.task_logic as task_logic
except ImportError:
    print("Warnung: Programmlogik Module nicht gefunden")

if __name__ == "__main__":
    window.mainloop()  # starting GUI only testing...


# to create the executable simply install pyinstaller via 'pip install pyinstaller' and then run the following command in the terminal; same directory as main.py:

'''python -m PyInstaller --onefile --windowed --name "RechtschreibTool" --add-data "Assets;Assets" --add-data "../Aufgabenkatalog;Aufgabenkatalog" --add-data "GUI;GUI" --add-data "Programmlogik;Programmlogik" --add-data "Aufgabeneditor;Aufgabeneditor" --add-data "Dtos;Dtos" --icon "Assets/srhIcon.png" --hidden-import "GUI.BereichCheckbox" --hidden-import "Programmlogik.logic_der_zweite" main.py'''
