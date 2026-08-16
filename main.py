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
    print("Warnung: Program Logic Module nicht gefunden")

if __name__ == "__main__":
    window.mainloop()  # starting GUI only testing...


# to create the executable simply install pyinstaller
# via 'pip install pyinstaller' and then run the
# following command in the terminal; same directory as main.py:
'''
python -m PyInstaller --onefile --windowed --name "RechtschreibTool" --add-data "assets;assets" --add-data "../Aufgabenkatalog;Aufgabenkatalog" --add-data "gui;gui" --add-data "program_logic;program_logic" --add-data "task_editor;task_editor" --add-data "dtos;dtos" --icon "assets/srhIcon.png" --hidden-import "gui.field_checkbox" --hidden-import "program_logic.task_logic" main.py
'''


# In order to create a virtual environment and install the required dependencies,
# run the following commands in the terminal:
'''
python -m venv venv
venv/Scripts/activate  # on Windows
pip install PyInstaller
pip install matplotlib
'''