# type: ignore
from program_logic.path import Path

# relative import of the modules (relative regarding base_dir)
Path().setup_sys_path()

from program_logic.json_loader import json_loader
import program_logic.task_logic

# Load JSON data into memory
json_loader.load_json()
# Create Aufgabe objects for all tasks
program_logic.task_logic.aufgaben_objekte_erstellen()

from gui.gui_new import *  # importing GUI completely
from gui.field_checkbox import FieldCheckbox
try:
    import program_logic.task_logic as task_logic
except ImportError:
    print("Warnung: Programmlogik Module nicht gefunden")

if __name__ == "__main__":
    window.mainloop()  # starting GUI only testing...


# to create the executable simply install pyinstaller
# via 'pip install pyinstaller' and then run the
# following command in the terminal; same directory as main.py:

'''python -m PyInstaller --onefile --windowed --name "RechtschreibTool" --add-data "Assets;Assets" --add-data "../Aufgabenkatalog;Aufgabenkatalog" --add-data "GUI;GUI" --add-data "Programmlogik;Programmlogik" --add-data "Aufgabeneditor;Aufgabeneditor" --add-data "Dtos;Dtos" --icon "Assets/srhIcon.png" --hidden-import "GUI.BereichCheckbox" --hidden-import "Programmlogik.logic_der_zweite" main.py'''
