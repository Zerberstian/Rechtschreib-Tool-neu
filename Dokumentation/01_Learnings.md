# <span style="color:#f2d3a0"><u>Learnings during our Project:</u></span>

---
## <span style="color:#cae494"><u>1. Using VS Code or Pycharm "Run" was sometimes unreliable.</u></span>
- We started using cmd/PowerShell to run the file in the directory.<br>
``
*your directory* python.\GUI_new.py
``


- *in my case:* <br>
``
D:\Recht\GUI> python .\GUI_new.py
``


- Via ``D:\> tree /f`` you can "print" the directory tree to see where your file is located 
and determine what you need to execute.
````
D:.
└───Recht
    └───GUI
        │   GUI_new.py
        └───__pycache__
````

---
## <span style="color:#cae494"><u>2. In general using the Terminal and useful commands.</u></span>
### <span style="color:#f2d3a0">tree:</span>
Show directory structure<br>
*commands*:
  - ``tree`` <br>
  Displays the folder structure of the current directory.<br><br>
  - ``tree D:\`` <br>
  Shows the folder structure of the D: drive.<br><br>

  - ``tree /f`` <br> 
  Displays all folders and files in the current directory.<br><br>

  - ``tree /a`` <br>
  Uses ASCII characters instead of extended characters (useful for logs or text files).<br><br>
  
### <span style="color:#f2d3a0">cd:</span>
Change directory<br>
*commands*:
- ``cd foldername``<br>
navigate to folder<br><br>
- ``cd ..``<br>
will move you up one level, changing the current directory<br><br>
- ``cd D:\Projects``<br>
specifies the target path where you want to move

#### <span style="color:#aaffaa">*Note*:</span> for cmd the command to change to a directory on a different Drive is
- ``cd /d D:directory\`` <br>
the targeted drive is D:\

###  <span style="color:#f2d3a0">mkdir and rmdir:</span>
an quick way to create and remove Folders<br>
*commands*:
- ``mkdir *folder name*``
  -  creates a Folder in your current directory<br><br>
- ``rmdir *folder name*``
  - will remove the Folder<br><br>
- ``rmdir /s *folder name*``
  - will remove Folder with content

###  <span style="color:#f2d3a0">del:</span>
Delete a file
*command*:
- ``del *file name*``

### <span style="color:#f2d3a0">clear and cls:</span>
clear the Terminal Window
*commands*:<br>
- Powershell
  - ``clear``<br><br>
- cmd
  - ``cls``<br>
### <span style="color:#f2d3a0">python *run file*</span>
- ``python .\*your file*``<br>

for example:<br>
- ``python .\GUI_new.py``
#### <span style="color:#aaffaa">*Note*:</span> You need to be in the same directory as the File.

### <span style="color:#f2d3a0">python version</span>
Check your Python Version installed <br>
- ``python --version``
---
## <span style="color:#cae494"><u>3. Version control: </u></span>

