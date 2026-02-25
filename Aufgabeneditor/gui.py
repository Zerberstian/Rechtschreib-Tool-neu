import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import aufgabeneditor as editor
import json


class AufgabenGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("📝 Aufgabeneditor GUI - Vollständige Bearbeitung")
        self.master.geometry("1200x800")
        self.data = editor.load_local_data()
        
        if not self.data:
            messagebox.showerror("Fehler", "Keine Aufgaben gefunden! Bitte zuerst versioncheck.py ausführen.")
            self.master.destroy()
            return
        
        self.left_frame = ttk.Frame(master, padding=10, width=300)
        self.right_frame = ttk.Frame(master, padding=10)
        self.left_frame.pack(side="left", fill="y")
        self.right_frame.pack(side="right", expand=True, fill="both")
        self.left_frame.pack_propagate(False)

        ttk.Label(self.left_frame, text="📚 BEREICHE", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0,5))
        self.bereich_list = tk.Listbox(self.left_frame, height=12)
        self.bereich_list.pack(fill="both", expand=True, pady=(0,10))
        self.bereich_list.bind("<<ListboxSelect>>", self.on_bereich_select)
        
        ttk.Label(self.left_frame, text="📖 TEILGEBIETE", font=("Arial", 11, "bold")).pack(anchor="w")
        self.teil_list = tk.Listbox(self.left_frame, height=10)
        self.teil_list.pack(fill="both", expand=True, pady=(0,10))
        self.teil_list.bind("<<ListboxSelect>>", self.on_teil_select)

        btn_frame = ttk.Frame(self.left_frame)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="➕ Neuer Bereich", command=self.add_bereich).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="➕ Neues Teilgebiet", command=self.add_teil).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="💾 Speichern & Commit", command=self.save_data).pack(fill="x", pady=(5,0))

        self.teil_header = ttk.Label(self.right_frame, text="📂 Kein Bereich/Teilgebiet ausgewählt",
                                      font=("Arial", 14, "bold"), foreground="blue")
        self.teil_header.pack(pady=10)

        columns = ("ID", "Beschreibung", "Korrekt", "Optionen")
        self.tree = ttk.Treeview(self.right_frame, columns=columns, show="headings", height=20)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Beschreibung", text="Übungsbeschreibung")
        self.tree.heading("Korrekt", text="Korrekt")
        self.tree.heading("Optionen", text="Optionen")
        self.tree.column("ID", width=80)
        self.tree.column("Beschreibung", width=400)
        self.tree.column("Korrekt", width=100)
        self.tree.column("Optionen", width=200)
        self.tree.pack(expand=True, fill="both", pady=(0,10))

        # renamed buttons
        btn_frame_right = ttk.Frame(self.right_frame)
        btn_frame_right.pack(fill="x")
        ttk.Button(btn_frame_right, text="➕ Neue Aufgabe im Teilgebiet erstellen", command=self.add_task).pack(side="left", padx=5)
        ttk.Button(btn_frame_right, text="✏️ Bearbeiten", command=self.edit_task_full).pack(side="left", padx=5)
        ttk.Button(btn_frame_right, text="🗑️ Löschen", command=self.delete_task).pack(side="left", padx=5)
        ttk.Button(btn_frame_right, text="🔍 Suche ID...", command=self.search_task).pack(side="right", padx=5)

        self.current_bereich_idx = None
        self.current_teil_idx = None
        self.refresh_bereiche()

    def refresh_bereiche(self):
        self.bereich_list.delete(0, tk.END)
        for i, b in enumerate(self.data):
            self.bereich_list.insert(tk.END, b.get("Uebungsbereich", f"Bereich {i+1}"))

    def on_bereich_select(self, event):
        sel = self.bereich_list.curselection()
        if not sel:
            return
        self.current_bereich_idx = sel[0]
        self.refresh_teilgebiete()
        self.teil_list.selection_clear(0, tk.END)

    def refresh_teilgebiete(self):
        self.teil_list.delete(0, tk.END)
        if self.current_bereich_idx is None:
            return
        teilgebiete = self.data[self.current_bereich_idx].get("Teilgebiet", [])
        for i, t in enumerate(teilgebiete):
            titel = t.get("Titel", f"Teilgebiet {i+1}")
            count = len(t.get("UebungenListe", []))
            self.teil_list.insert(tk.END, f"{titel} ({count} Aufgaben)")

    def on_teil_select(self, event):
        sel = self.teil_list.curselection()
        if not sel:
            return
        self.current_teil_idx = sel[0]
        self.refresh_tasks()
        self.update_header()

    def update_header(self):
        if self.current_bereich_idx is not None and self.current_teil_idx is not None:
            bereich_name = self.data[self.current_bereich_idx]["Uebungsbereich"]
            teil = self.data[self.current_bereich_idx]["Teilgebiet"][self.current_teil_idx]
            teil_name = teil.get("Titel", "ohne Titel")
            count = len(teil.get("UebungenListe", []))
            self.teil_header.config(text=f"📂 {bereich_name} > {teil_name} ({count} Aufgaben)")

    def refresh_tasks(self):
        self.tree.delete(*self.tree.get_children())
        if self.current_bereich_idx is None or self.current_teil_idx is None:
            return
        teil = self.data[self.current_bereich_idx]["Teilgebiet"][self.current_teil_idx]
        for task in teil.get("UebungenListe", []):
            id_ = task.get("Uebung_id", "")
            desc = task.get("UebungsBeschreibung", "")[:60] + "..." if len(task.get("UebungsBeschreibung", "")) > 60 else task.get("UebungsBeschreibung", "")
            korrekt_idx = task.get("KorrekteAntwort", 0)
            moeg = task.get("Moeglichkeiten", [])
            korrekt_text = moeg[korrekt_idx-1][0] if moeg and 0 < korrekt_idx <= len(moeg) else "?"
            opts_str = f"[{len(moeg)} Optionen]"
            self.tree.insert("", "end", values=(id_, desc, korrekt_text, opts_str))

    def add_bereich(self):
        name = simpledialog.askstring("Neuer Bereich", "Name des neuen Bereichs:")
        if name:
            self.data.append({"Uebungsbereich": name, "Teilgebiet": []})
            self.refresh_bereiche()

    def add_teil(self):
        if self.current_bereich_idx is None:
            messagebox.showerror("Fehler", "Bitte zuerst einen Bereich auswählen.")
            return
        titel = simpledialog.askstring("Neues Teilgebiet", "Titel:")
        beschreibung = simpledialog.askstring("Neues Teilgebiet", "Beschreibung (optional):")
        if titel:
            self.data[self.current_bereich_idx]["Teilgebiet"].append({
                "Titel": titel,
                "Aufgabenbeschreibung": beschreibung or "",
                "UebungenListe": []
            })
            self.refresh_teilgebiete()

    # Helper function to create option input fields dynamically - handles both normal tasks (3 options) and special tasks (1 field)
    def create_option_fields(self, dialog, task=None):
        """Creates individual input fields for each answer option. Automatically detects special tasks (1 option) vs normal tasks (3 options)"""
        option_frame = ttk.LabelFrame(dialog, text="📋 Antwortoptionen", padding=10)
        option_frame.pack(fill="both", expand=True, pady=10)
        
        self.option_entries = []  # Store references to all option entry fields
        
        # Determine number of options based on task type
        if task and len(task.get("Moeglichkeiten", [])) == 1:
            # SPECIAL TASK: Only 1 field for the special text/content
            ttk.Label(option_frame, text="Spezialtext/Inhalt:").pack(anchor="w")
            entry = tk.Text(option_frame, height=3, width=60)
            if task:
                entry.insert("1.0", task["Moeglichkeiten"][0])
            entry.pack(pady=5, fill="x")
            self.option_entries.append(entry)
        else:
            # NORMAL TASK: 3 separate fields for options 1,2,3
            for i in range(3):
                frame = ttk.Frame(option_frame)
                frame.pack(fill="x", pady=2)
                
                # Option number label
                ttk.Label(frame, text=f"Option {i+1}:", width=10).pack(side="left")
                
                # Text entry field
                entry = tk.Text(frame, height=2, width=50)
                if task and i < len(task.get("Moeglichkeiten", [])):
                    # Pre-fill with existing option if editing
                    option_text = task["Moeglichkeiten"][i]
                    entry.insert("1.0", option_text if isinstance(option_text, str) else option_text[0])
                else:
                    # Default text for new tasks
                    entry.insert("1.0", f"Option {i+1}")
                entry.pack(side="right", fill="x", expand=True, padx=(10,0))
                
                self.option_entries.append(entry)
        
        return option_frame

    def add_task(self):
        if self.current_bereich_idx is None or self.current_teil_idx is None:
            messagebox.showerror("Fehler", "Bitte Bereich UND Teilgebiet auswählen.")
            return
        
        teil = self.data[self.current_bereich_idx]['Teilgebiet'][self.current_teil_idx]
        auto_id = editor.generate_auto_id(self.current_bereich_idx, self.current_teil_idx, teil.get('UebungenListe', []))
        
        dialog = tk.Toplevel(self.master)
        dialog.title(f"🆕 Neue Aufgabe {auto_id}")
        dialog.geometry("600x550")
        dialog.transient(self.master)
        dialog.grab_set()
        
        ttk.Label(dialog, text=f"ID: {auto_id} (automatisch)", font=("Arial", 11, "bold")).pack(pady=10)
        
        # Description field
        ttk.Label(dialog, text="📝 Übungsbeschreibung:").pack(anchor="w", padx=10)
        self.beschr_entry = tk.Text(dialog, height=4, width=70)
        self.beschr_entry.pack(pady=5, padx=10, fill="x")
        
        # Dynamic option fields instead of JSON
        self.create_option_fields(dialog)
        
        # Correct answer selector
        ttk.Label(dialog, text="✅ Korrekte Antwort (1-3):").pack(anchor="w", padx=10, pady=(15,0))
        self.korrekt_entry = ttk.Entry(dialog, width=10)
        self.korrekt_entry.insert(0, "1")
        self.korrekt_entry.pack(pady=5, padx=10, fill="x")
        
        # Optional info text
        ttk.Label(dialog, text="ℹ️ Infotext (optional):").pack(anchor="w", padx=10, pady=(10,0))
        self.info_entry = tk.Text(dialog, height=3, width=70)
        self.info_entry.pack(pady=5, padx=10, fill="x")
        
        def create_task():
            try:
                # Convert option fields back to proper JSON list format
                moeglichkeiten = []
                for entry in self.option_entries:
                    text_content = entry.get("1.0", tk.END).strip()
                    if text_content:
                        moeglichkeiten.append([text_content])  # Store as list with single string
                
                new_task = {
                    "Uebung_id": auto_id,
                    "UebungsBeschreibung": self.beschr_entry.get("1.0", tk.END).strip(),
                    "Moeglichkeiten": moeglichkeiten,
                    "KorrekteAntwort": int(self.korrekt_entry.get()),
                    "Infotext": self.info_entry.get("1.0", tk.END).strip()
                }
                teil.setdefault("UebungenListe", []).append(new_task)
                self.refresh_tasks()
                self.update_header()
                dialog.destroy()
                messagebox.showinfo("✅ Erfolg", f"Aufgabe {auto_id} erstellt!")
            except Exception as e:
                messagebox.showerror("❌ Fehler", f"Fehler beim Erstellen:\n{e}")
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="✅ Aufgabe erstellen", command=create_task).pack(pady=5)
        ttk.Button(btn_frame, text="❌ Abbrechen", command=dialog.destroy).pack(pady=5)

    def edit_task_full(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showerror("Fehler", "Bitte Aufgabe auswählen.")
            return
        
        values = self.tree.item(sel, 'values')
        task_id = values[0]
        result = editor.find_task_by_id(self.data, task_id)
        if not result:
            return
        bereich_idx, teil_idx, task_idx, task = result
        
        dialog = tk.Toplevel(self.master)
        dialog.title(f"✏️ Bearbeite Aufgabe {task_id}")
        dialog.geometry("650x600")
        dialog.transient(self.master)
        dialog.grab_set()
        
        ttk.Label(dialog, text=f"ID: {task_id} 🔒", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Description field
        ttk.Label(dialog, text="📝 Übungsbeschreibung:").pack(anchor="w", padx=10)
        beschr_entry = tk.Text(dialog, height=4, width=80)
        beschr_entry.insert("1.0", task.get("UebungsBeschreibung", ""))
        beschr_entry.pack(pady=5, padx=10, fill="x")
        
        # Dynamic option fields for editing (pre-filled with existing values)
        self.create_option_fields(dialog, task)
        
        # Correct answer field
        ttk.Label(dialog, text="✅ Korrekte Antwort (Index 1-3):").pack(anchor="w", padx=10, pady=(10,0))
        korrekt_var = tk.StringVar(value=str(task.get("KorrekteAntwort", 1)))
        korrekt_entry = ttk.Entry(dialog, textvariable=korrekt_var, width=10)
        korrekt_entry.pack(pady=5, padx=10, fill="x")
        
        # Info text
        ttk.Label(dialog, text="ℹ️ Infotext:").pack(anchor="w", padx=10, pady=(10,0))
        info_entry = tk.Text(dialog, height=3, width=80)
        info_entry.insert("1.0", task.get("Infotext", ""))
        info_entry.pack(pady=5, padx=10, fill="x")
        
        #  notice about saving
        notice_frame = ttk.LabelFrame(dialog, text="💾 WICHTIG", foreground="orange", padding=8)
        notice_frame.pack(fill="x", padx=10, pady=10)
        ttk.Label(notice_frame, 
                 text="✅ Änderungen werden automatisch übernommen wenn du dieses Fenster schließt.\n💾 Danach 'Speichern & Commit' im Hauptfenster drücken!").pack()
        
        def save_changes():
            try:
                # Update task with new values from individual option fields
                task["UebungsBeschreibung"] = beschr_entry.get("1.0", tk.END).strip()
                
                # Convert option fields back to JSON format
                moeglichkeiten = []
                for entry in self.option_entries:
                    text_content = entry.get("1.0", tk.END).strip()
                    if text_content:
                        moeglichkeiten.append([text_content])
                
                task["Moeglichkeiten"] = moeglichkeiten
                task["KorrekteAntwort"] = int(korrekt_var.get())
                task["Infotext"] = info_entry.get("1.0", tk.END).strip()
                
                self.refresh_tasks()
                dialog.destroy()
                messagebox.showinfo("✅ Erfolg", f"Aufgabe {task_id} aktualisiert!")
            except Exception as e:
                messagebox.showerror("❌ Fehler", f"Fehler beim Speichern:\n{e}")
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="💾 Änderungen übernehmen", command=save_changes).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="❌ Schließen (Änderungen verwerfen)", command=dialog.destroy).pack(side="left")

    def delete_task(self):
        sel = self.tree.focus()
        if not sel:
            return
        values = self.tree.item(sel, 'values')
        task_id = values[0]
        result = editor.find_task_by_id(self.data, task_id)
        if not result:
            return
        bereich_idx, teil_idx, task_idx, _ = result
        if messagebox.askyesno("Löschen", f"Aufgabe '{task_id}' wirklich löschen?"):
            self.data[bereich_idx]["Teilgebiet"][teil_idx]["UebungenListe"].pop(task_idx)
            self.refresh_tasks()
            self.update_header()

    def search_task(self):
        task_id = simpledialog.askstring("Suche Aufgabe", "Aufgaben-ID eingeben (z.B. 1.2.45):")
        if not task_id:
            return
        result = editor.find_task_by_id(self.data, task_id)
        if result:
            bereich_idx, teil_idx, task_idx, _ = result
            self.bereich_list.selection_set(bereich_idx)
            self.on_bereich_select(None)
            self.teil_list.selection_set(teil_idx)
            self.on_teil_select(None)
            self.tree.selection_set(self.tree.get_children()[task_idx])
            messagebox.showinfo("Gefunden", f"Aufgabe {task_id} ausgewählt!")
        else:
            messagebox.showinfo("Nicht gefunden", f"Aufgabe {task_id} nicht gefunden.")

    def save_data(self):
        success = editor.save_and_commit(self.data)
        status = "🟢 Erfolg" if success else "🟡 Nur lokal"
        messagebox.showinfo("Speichern", f"Änderungen gespeichert!\n{status}")
        self.refresh_bereiche()


if __name__ == "__main__":
    root = tk.Tk()
    app = AufgabenGUI(root)
    root.mainloop()
