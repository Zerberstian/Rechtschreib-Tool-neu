# <span style="color:#00ff00">Learnings during our Project:</span>

---
## <span style="color:#00fff0">1. Using VS Code or Pycharm "Run" was sometimes unreliable.</span>
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
## <span style="color:#00fff0">2. In general using the Terminal and useful commands.</span>
### <span style="color:#ff4b4b">tree:</span>
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
  
### <span style="color:#ff4b4b">cd:</span>
Change directory<br>
*commands*:
- ``cd foldername``<br>
navigate to folder<br><br>
- ``cd ..``<br>
will move you up one level, changing the current directory<br><br>
- ``cd D:\Projects``<br>
specifies the target path where you want to move

###  <span style="color:#ff4b4b">mkdir and rmdir</span>
an quick way to create and remove Folders<br>
*commands*:
- ``mkdir *folder name*``
  -  creates a Folder in your current directory<br><br>
- ``rmdir *folder name*``
  - will remove the Folder<br><br>
- ``rmdir /s *folder name*``
  - will remove Folder with content

###  <span style="color:#ff4b4b">del</sman>

