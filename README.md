# Rechtschreiblerntool

## Installation for users

The application is a Windows desktop application. A Python installation is only
needed when running the source code. For a built `.exe`, copy the executable to
the target computer and start it normally.

The task catalogue is loaded from the GitHub repository
`orphcvs/Aufgabenkatalog`. The application uses the local file
`program_logic/json_cache.json` as an offline cache. The first source checkout
must therefore contain this cache, or the catalogue must be downloaded once
before starting the application. Internet access is required to download a
new catalogue version.

## Development setup

Install the following prerequisites:

- Python 3.10 or newer
- Git, if you use the task editor or need to clone/update the catalogue
- Internet access for downloading the catalogue and Python packages

Open PowerShell in the directory containing `main.py` and run:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

If PowerShell prevents activation, run the commands from `venv\Scripts\activate.bat`
in Command Prompt instead, or activate the environment using the VS Code Python
interpreter selector.

## Catalogue and Git requirement

Normal users do not need Git to read the catalogue. The application reads the
cached JSON file and can download the published `Aufgabenkatalog.json` over
HTTPS. Git is required for the task editor's publish workflow because the
editor clones the catalogue repository, commits the changed JSON file, and
pushes the commit to the `main` branch.

Verify that Git is installed and available on `PATH`:

```powershell
git --version
```

If the cache is missing, the application shows a warning and cannot display
tasks until a valid catalogue cache is available. Do not delete
`program_logic/json_cache.json` unless you intend to recreate the local cache.

## Task editor configuration

The task editor can save changes locally without GitHub credentials. To publish
changes to GitHub, create the file `task_editor/credentials.json` with this
content:

```json
{
	"username": "your_github_username",
	"token": "your_github_token"
}
```

Create the token in GitHub settings and grant it permission to write to the
`orphcvs/Aufgabenkatalog` repository. Keep this file private and never commit
it. The editor also needs the Git executable available on `PATH`.

## Build a Windows executable

Install the dependencies first, including PyInstaller:

```powershell
venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

From the project directory, build the executable with:

```powershell
python -m PyInstaller --onefile --windowed --name "RechtschreibTool" --add-data "assets;assets" --add-data "program_logic;program_logic" --add-data "gui;gui" --add-data "task_editor;task_editor" --add-data "dtos;dtos" --icon "assets/srhIcon.ico" --hidden-import "gui.field_checkbox" --hidden-import "program_logic.task_logic" main.py
```

The result is written to `dist\RechtschreibTool.exe`. The writable catalogue
cache is stored beside the executable. If the bundled cache is not available,
the executable starts without tasks and displays a warning.

### Build the task editor

Build the editor as a separate executable. Run this command from the project
directory:

```powershell
python -m PyInstaller --onefile --windowed --name "Aufgabeneditor" --add-data "assets;assets" --add-data "program_logic;program_logic" --add-data "gui;gui" --add-data "task_editor;task_editor" --add-data "dtos;dtos" --icon "assets\srhIcon.ico" --hidden-import "task_editor.gui" --hidden-import "task_editor.task_editor" task_editor\gui.py
```

The result is written to `dist\Aufgabeneditor.exe`. The editor needs a
catalogue cache to load tasks. Git must be installed and available on `PATH`
to publish changes. For publishing, place `credentials.json` in the
`task_editor` directory used by the application and **do not distribute that
file with the executable.**

## Project structure

### assets
Images, icons, and the PDF used by the application.

### dtos
Data-transfer objects for catalogues, fields, subfields, and tasks.

### gui
The main Tkinter interface and its widgets.

### program_logic
Catalogue loading, cache handling, path handling, and task logic.

### task_editor
The catalogue editor and its optional GitHub publishing workflow.

### documentation
Development notes and project documentation.