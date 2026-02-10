# Cleaning up this funktion:
```python
def pick_color_fg():
    color = colorchooser.askcolor(title="Farbe auswählen")
    if color[1]:
        MenuText.config(fg=color[1])
        for widget in MenuFrame.winfo_children():
            if isinstance(widget, Button):
                widget.config(fg=color[1])
        for widget in CheckBoxFrameS.winfo_children():
            if isinstance(widget, Button):
                widget.config(fg=color[1])
        for widget in ButtonFrameSB.winfo_children():
            if isinstance(widget, Button):
                widget.config(fg=color[1])
        for widget in SpinBoxFrame.winfo_children():
            if isinstance(widget, (Button, Label)):
                widget.config(fg=color[1])
            if isinstance(widget, Spinbox):
                widget.config(fg=color[1])
        for widget in ColorPickerFrame.winfo_children():
            if isinstance(widget, Button):
                widget.config(fg=color[1])
        for widget in ColorPickerButtonFrame.winfo_children():
            if isinstance(widget, Button):
                widget.config(fg=color[1])
```

## Why is the current code not ideal?

### Repetition

The same pattern is repeated multiple times:

```python
from tkinter import Button, Label, Spinbox
SomeFrame = Frame(root)                     # <- Frame
for widget in SomeFrame.winfo_children():   # <- Widgets in Frame
    if isinstance(widget, Button):       
        widget.config(fg=color[1])
````   

## cleaning process
### Step 1: Centralized widget styling
```python


from tkinter import Button, Label, Spinbox

def apply_fg(widget, color):
    if isinstance(widget, (Button, Label)):
        widget.config(fg=color)

    elif isinstance(widget, Spinbox):
        widget.config(
            fg=color,
            insertbackground=color
        )
```
This function defines all foreground styling rules in one location.

---
### Step 2: Recursive widget traversal
```python
def apply_fg_recursive(parent, color):
    for widget in parent.winfo_children():
        apply_fg(widget, color)
        apply_fg_recursive(widget, color)
```
This ensures:
- Nested frames are handled correctly
- Future layout changes do not break theming
- No frame-specific loops are required
---
### Step 3: Simplified color picker function
```python
def pick_color_fg():
    color = colorchooser.askcolor(title="Farbe auswählen")
    if color[1]:
        MenuText.config(fg=color[1])
        apply_fg_recursive(root, color[1])
```
The color picker now focuses on intent, not widget traversal.

---
### Advantages of this approach
- Single source of truth for styling
- Works with nested layouts
- Easy to extend to new widget types (Entry, Text, etc.)
- Significantly reduced code duplication
- Easier debugging and maintenance
- Scales well with growing GUIs
