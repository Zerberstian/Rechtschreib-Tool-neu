import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import aufgabeneditor as editor
import os
import difflib

COLOR_PRIMARY = "#01386E"    # Deep Navy
COLOR_SECONDARY = "#3498DB"  # Bright Blue 
COLOR_BG_MAIN = "#F4F7F6"    # Soft Light Gray 
COLOR_BG_SIDEBAR = "#FFFFFF" # White
COLOR_TEXT_DARK = "#2C3E50"  # Dark Gray/Navy
COLOR_TEXT_LIGHT = "#FFFFFF" # White
COLOR_SUCCESS = "#27AE60"    # Green
COLOR_DANGER = "#E74C3C"     # Red
COLOR_BORDER = "#DCDDE1"     # Light Gray

# Consistent use of font types across the application
FONT_BOLD = ("Segoe UI", 11, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_HEADER = ("Segoe UI", 15, "bold")
FONT_SMALL = ("Segoe UI", 9)

class AufgabenGUI:
    """
    The main interface for the Task Editor.
    This class manages the display of exercise categories (Bereiche), sub-categories (Teilgebiete),
    and the individual tasks within them.
    """
    def __init__(self, master):
        self.master = master 
        self.master.title("Aufgabeneditor v2.0")
        self.master.geometry("1400x900")
        self.master.configure(bg=COLOR_BG_MAIN) 
        
        # Load the task database via the editor logic module
        self.data = editor.load_local_data()
        if not self.data:
            messagebox.showerror("Error", "Keine Daten gefunden! Bitte führen Sie versioncheck.py zuerst aus.")
            self.master.destroy()
            return

        # Perform cleanup of old temporary directories to keep the workspace clean
        editor.cleanup_old_temps(os.path.dirname(editor.__file__), 'temp_repo')

        self.setup_styles()
        self.create_widgets()
        
        # Track the currently selected category and sub-category
        self.current_bereich_idx = None
        self.current_teil_idx = None
        
        # Initial population of the category list
        self.refresh_bereiche()


        style = ttk.Style()
        style.theme_use('clam') # "clam" allows for consistent cross-platform styling
        
        # Layout Components
        style.configure("TFrame", background=COLOR_BG_MAIN)
        style.configure("Sidebar.TFrame", background=COLOR_BG_SIDEBAR)
        
        # Label Variations
        style.configure("TLabel", background=COLOR_BG_MAIN, foreground=COLOR_TEXT_DARK, font=FONT_NORMAL)
        style.configure("Header.TLabel", background=COLOR_PRIMARY, foreground=COLOR_TEXT_LIGHT, font=FONT_HEADER, padding=10)
        style.configure("Sidebar.TLabel", background=COLOR_BG_SIDEBAR, font=FONT_BOLD)
        style.configure("Stat.TLabel", background=COLOR_PRIMARY, foreground=COLOR_TEXT_LIGHT, font=FONT_BOLD)
        
        # Button Styles
        style.configure("TButton", font=FONT_NORMAL, padding=8)
        style.map("TButton",
                  background=[('active', COLOR_SECONDARY), ('!disabled', COLOR_PRIMARY)],
                  foreground=[('!disabled', COLOR_TEXT_LIGHT)])
        
        style.configure("Success.TButton", font=FONT_BOLD, background=COLOR_SUCCESS)
        style.map("Success.TButton", background=[('active', '#219150'), ('!disabled', COLOR_SUCCESS)])
        
        # Data Table Styling
        style.configure("Treeview", 
                        rowheight=35, 
                        font=FONT_NORMAL, 
                        background=COLOR_BG_SIDEBAR,
                        fieldbackground=COLOR_BG_SIDEBAR,
                        borderwidth=0)
        style.configure("Treeview.Heading", font=FONT_BOLD, background=COLOR_BORDER, foreground=COLOR_TEXT_DARK)
        # Setting highlights for the selected row
        style.map("Treeview", background=[('selected', COLOR_SECONDARY)], foreground=[('selected', COLOR_TEXT_LIGHT)])

    def create_widgets(self):
        # --- Header Bar: Logo, Global Stats, and Save Actions ---
        self.top_bar = tk.Frame(self.master, bg=COLOR_PRIMARY, height=70)
        self.top_bar.pack(side="top", fill="x")
        self.top_bar.pack_propagate(False)
        
        ttk.Label(self.top_bar, text="AUFGENEDITOR", style="Header.TLabel").pack(side="left", padx=20)
        
        self.stats_label = ttk.Label(self.top_bar, text="Berechne...", style="Stat.TLabel")
        self.stats_label.pack(side="right", padx=30)
        
        btn_save = ttk.Button(self.top_bar, text="Speichern & neue Version erstellen", command=self.save_data, style="Success.TButton")
        btn_save.pack(side="right", padx=10)
        
        ttk.Button(self.top_bar, text="Statistik", command=self.show_statistics).pack(side="right", padx=5)

        # --- Main Workspace ---
        self.main_container = tk.Frame(self.master, bg=COLOR_BG_MAIN)
        self.main_container.pack(expand=True, fill="both")

        # --- Sidebar Navigation ---
        self.left_sidebar = tk.Frame(self.main_container, bg=COLOR_BG_SIDEBAR, width=350)
        self.left_sidebar.pack(side="left", fill="y")
        self.left_sidebar.pack_propagate(False)
        
        # Visual separator line between sidebar and content
        tk.Frame(self.main_container, width=1, bg=COLOR_BORDER).pack(side="left", fill="y")

        # -- Section: Main Categories (Uebungsbereiche) --
        self.create_sidebar_header("KATEGORIEN")
        
        self.bereich_list = tk.Listbox(self.left_sidebar, height=8, font=FONT_NORMAL, 
                                       bg=COLOR_BG_SIDEBAR, fg=COLOR_TEXT_DARK,
                                       selectbackground=COLOR_SECONDARY, selectforeground=COLOR_TEXT_LIGHT,
                                       borderwidth=0, highlightthickness=0, activestyle='none')
        self.bereich_list.pack(fill="x", padx=15, pady=5)
        self.bereich_list.bind("<<ListboxSelect>>", self.on_bereich_select)
        
        # Category Control Buttons
        b_btn_frame = tk.Frame(self.left_sidebar, bg=COLOR_BG_SIDEBAR)
        b_btn_frame.pack(fill="x", padx=15, pady=(0, 20))
        ttk.Button(b_btn_frame, text="Neu", command=self.add_bereich).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(b_btn_frame, text="Bearbeiten", command=self.edit_bereich).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(b_btn_frame, text="Löschen", command=self.delete_bereich).pack(side="left", expand=True, fill="x", padx=2)

        # -- Section: Sub-Categories (Teilgebiete) --
        self.create_sidebar_header("Teilgebiete")
        
        self.teil_list = tk.Listbox(self.left_sidebar, height=22, font=FONT_NORMAL,
                                     bg=COLOR_BG_SIDEBAR, fg=COLOR_TEXT_DARK,
                                     selectbackground=COLOR_SECONDARY, selectforeground=COLOR_TEXT_LIGHT,
                                     borderwidth=0, highlightthickness=0, activestyle='none')
        self.teil_list.pack(fill="x", padx=15, pady=5)
        self.teil_list.bind("<<ListboxSelect>>", self.on_teil_select)
        
        # Sub-Category Control Buttons
        t_btn_frame = tk.Frame(self.left_sidebar, bg=COLOR_BG_SIDEBAR)
        t_btn_frame.pack(fill="x", padx=15, pady=(0, 10))
        ttk.Button(t_btn_frame, text="Neu", command=self.add_teil).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(t_btn_frame, text="Bearbeiten", command=self.edit_teil).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(t_btn_frame, text="Löschen", command=self.delete_teil).pack(side="left", expand=True, fill="x", padx=2)

        # --- Content Area: Task List ---
        self.content_area = tk.Frame(self.main_container, bg=COLOR_BG_MAIN)
        self.content_area.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        # Dynamic Breadcrumb Header
        self.path_label = tk.Label(self.content_area, text="Wähle ein Teilgebiet aus, um Aufgaben anzuzeigen", 
                                   bg=COLOR_BG_MAIN, fg=COLOR_PRIMARY, font=FONT_HEADER, anchor="w")
        self.path_label.pack(fill="x", pady=(0, 20))

        # Data Table (Treeview)
        table_wrap = tk.Frame(self.content_area, bg=COLOR_BG_SIDEBAR, relief="flat", bd=1)
        table_wrap.pack(expand=True, fill="both")
        
        cols = ("ID", "Description", "Correct", "Options")
        self.tree = ttk.Treeview(table_wrap, columns=cols, show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Description", text="Aufgabenbeschreibung")
        self.tree.heading("Correct", text="Korrekte Antwort")
        self.tree.heading("Options", text="Details")
        
        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Description", width=500)
        self.tree.column("Correct", width=150, anchor="center")
        self.tree.column("Options", width=120, anchor="center")
        
        sb = ttk.Scrollbar(table_wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", expand=True, fill="both")
        sb.pack(side="right", fill="y")
        
        # Interactive features
        self.tree.bind("<Double-1>", lambda e: self.edit_task_full())

        # Task Action Controls
        task_ctrls = tk.Frame(self.content_area, bg=COLOR_BG_MAIN, pady=20)
        task_ctrls.pack(fill="x")
        
        ttk.Button(task_ctrls, text="Aufgabe Hinzufügen", command=self.add_task).pack(side="left", padx=5)
        ttk.Button(task_ctrls, text="Aufgabe Bearbeiten", command=self.edit_task_full).pack(side="left", padx=5)
        ttk.Button(task_ctrls, text="Aufgabe Löschen", command=self.delete_task).pack(side="left", padx=5)
        ttk.Button(task_ctrls, text="ID-Suche", command=self.search_task).pack(side="right", padx=5)

    def create_sidebar_header(self, text):
        lbl = tk.Label(self.left_sidebar, text=text, bg=COLOR_BG_SIDEBAR, fg=COLOR_PRIMARY, font=FONT_BOLD, anchor="w")
        lbl.pack(fill="x", padx=15, pady=(15, 5))

    def show_diff_dialog(self, title, old_text, new_text, on_confirm):
        diff_win = tk.Toplevel(self.master)
        diff_win.title(f"Review: {title}")
        diff_win.geometry("1000x800")
        diff_win.configure(bg=COLOR_BG_MAIN)
        diff_win.grab_set()

        tk.Label(diff_win, text="ÄNDERUNGEN PRÜFEN", font=FONT_HEADER, bg=COLOR_BG_MAIN, fg=COLOR_PRIMARY).pack(pady=15)
        
        # Color Legend
        legend = tk.Frame(diff_win, bg=COLOR_BG_MAIN)
        legend.pack(fill="x", padx=25)
        tk.Label(legend, text="Red = Entfernt", fg=COLOR_DANGER, bg=COLOR_BG_MAIN, font=FONT_SMALL).pack(side="left", padx=10)
        tk.Label(legend, text="Green = Hinzugefügt", fg=COLOR_SUCCESS, bg=COLOR_BG_MAIN, font=FONT_SMALL).pack(side="left")

        # Diff View
        view_frame = tk.Frame(diff_win, bg=COLOR_BG_MAIN)
        view_frame.pack(expand=True, fill="both", padx=25, pady=10)
        
        txt_box = tk.Text(view_frame, wrap="none", font=("Consolas", 10), bg="#FFFFFF", relief="flat", padx=10, pady=10)
        txt_box.pack(side="left", expand=True, fill="both")
        
        sb_y = ttk.Scrollbar(view_frame, orient="vertical", command=txt_box.yview)
        sb_y.pack(side="right", fill="y")
        sb_x = ttk.Scrollbar(diff_win, orient="horizontal", command=txt_box.xview)
        sb_x.pack(fill="x", padx=25, pady=(0, 15))
        
        txt_box.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)

        # Generate comparison
        d = difflib.Differ()
        comparison = list(d.compare(old_text.splitlines(), new_text.splitlines()))

        txt_box.tag_configure("rem", background="#FFE3E6", foreground="#B31D28")
        txt_box.tag_configure("add", background="#E6FFED", foreground="#22863A")

        for line in comparison:
            if line.startswith("- "):
                txt_box.insert(tk.END, line + "\n", "rem")
            elif line.startswith("+ "):
                txt_box.insert(tk.END, line + "\n", "add")
            else:
                txt_box.insert(tk.END, line + "\n")

        txt_box.config(state="disabled")

        # Confirmation
        btn_box = tk.Frame(diff_win, bg=COLOR_BG_MAIN)
        btn_box.pack(pady=20)
        
        ttk.Button(btn_box, text="Bestätigen & Speichern", style="Success.TButton",
                  command=lambda: [on_confirm(), diff_win.destroy()]).pack(side="left", padx=10)
        ttk.Button(btn_box, text="Zurück", 
                  command=diff_win.destroy).pack(side="left")

    # --- Navigation & UI Refresh ---

    def refresh_bereiche(self):
        self.bereich_list.delete(0, tk.END)
        for i, b in enumerate(self.data):
            self.bereich_list.insert(tk.END, b.get("Uebungsbereich", f"Category {i+1}"))
        self.update_stats_label()

    def update_stats_label(self):
        count = editor.count_aufgaben(self.data)
        self.stats_label.config(text=f"Aufgabensammlung: {count} Aufgaben")

    def on_bereich_select(self, event):
        selection = self.bereich_list.curselection()
        if not selection: return
        self.current_bereich_idx = selection[0]
        self.current_teil_idx = None
        self.refresh_teilgebiete()
        self.refresh_tasks()
        self.update_breadcrumb()

    def refresh_teilgebiete(self):
        self.teil_list.delete(0, tk.END)
        if self.current_bereich_idx is None: return
        
        subs = self.data[self.current_bereich_idx].get("Teilgebiet", [])
        for i, s in enumerate(subs):
            title = s.get("Titel", "Untitled")
            count = len(s.get("UebungenListe", []))
            self.teil_list.insert(tk.END, f"{title} ({count})")

    def on_teil_select(self, event):
        selection = self.teil_list.curselection()
        if not selection: return
        self.current_teil_idx = selection[0]
        self.refresh_tasks()
        self.update_breadcrumb()

    def update_breadcrumb(self):
        if self.current_bereich_idx is not None:
            b_name = self.data[self.current_bereich_idx].get("Uebungsbereich", "Unknown")
            if self.current_teil_idx is not None:
                sub = self.data[self.current_bereich_idx]["Teilgebiet"][self.current_teil_idx]
                s_name = sub.get("Titel", "Untitled")
                self.path_label.config(text=f" {b_name}  ›  {s_name}")
            else:
                self.path_label.config(text=f" {b_name}  ›  Wähle ein Teilgebiet")
        else:
            self.path_label.config(text="Willkommen! Bitte wähle eine Kategorie aus, um zu beginnen.")

    def refresh_tasks(self):
        # Populates the main task table
        self.tree.delete(*self.tree.get_children())
        if self.current_bereich_idx is None or self.current_teil_idx is None:
            return
            
        tasks = self.data[self.current_bereich_idx]["Teilgebiet"][self.current_teil_idx].get("UebungenListe", [])
        for task in tasks:
            tid = task.get("Uebung_id", "")
            desc = task.get("UebungsBeschreibung", "")
            if len(desc) > 85: desc = desc[:82] + "..."
            
            c_idx = task.get("KorrekteAntwort", 0)
            opts = task.get("Moeglichkeiten", [])
            
            # Get textual representation of correct answer
            c_text = "?"
            if opts and 0 < c_idx <= len(opts):
                val = opts[c_idx-1]
                c_text = val[0] if isinstance(val, list) and val else str(val)
            
            details = f"{len(opts)} Antw"
            if task.get("Infotext"): details += " + Info"
            
            self.tree.insert("", "end", values=(tid, desc, c_text, details))

    # --- Structural Management (Add/Edit/Delete Categories) ---

    def add_bereich(self):
        name = simpledialog.askstring("Neu", "Kategoriename:")
        if name and name.strip():
            self.data.append({"Uebungsbereich": name.strip(), "Teilgebiet": []})
            self.refresh_bereiche()

    def edit_bereich(self):
        if self.current_bereich_idx is None: return
        old = self.data[self.current_bereich_idx]["Uebungsbereich"]
        new = simpledialog.askstring("Bearbeiten", "Neuer Kategoriename:", initialvalue=old)
        if new and new.strip():
            self.data[self.current_bereich_idx]["Uebungsbereich"] = new.strip()
            self.refresh_bereiche()
            self.update_breadcrumb()

    def delete_bereich(self):
        if self.current_bereich_idx is None: return
        name = self.data[self.current_bereich_idx]["Uebungsbereich"]
        if messagebox.askyesno("Bestätigen", f"Lösche '{name}' und ALL seine Inhalte?"):
            self.data.pop(self.current_bereich_idx)
            self.current_bereich_idx = self.current_teil_idx = None
            self.refresh_bereiche(); self.refresh_teilgebiete(); self.refresh_tasks(); self.update_breadcrumb()

    def add_teil(self):
        if self.current_bereich_idx is None: return
        t = simpledialog.askstring("Neu", "Teilgebiet-Titel:")
        if t and t.strip():
            d = simpledialog.askstring("Neu", "Beschreibungstext:")
            self.data[self.current_bereich_idx]["Teilgebiet"].append({
                "Titel": t.strip(), "Aufgabenbeschreibung": d or "", "UebungenListe": [], "IstSpeziell": False,
                "Teilgebiet_id": f"{self.current_bereich_idx+1}.{len(self.data[self.current_bereich_idx]['Teilgebiet'])+1}"
            })
            self.refresh_teilgebiete()

    def edit_teil(self):
        if self.current_bereich_idx is None or self.current_teil_idx is None: return
        sub = self.data[self.current_bereich_idx]["Teilgebiet"][self.current_teil_idx]
        
        old_view = f"Title: {sub.get('Titel')}\nIntro: {sub.get('Aufgabenbeschreibung')}"

        diag = tk.Toplevel(self.master); diag.title("Bearbeite Teilgebiet"); diag.geometry("600x450")
        
        tk.Label(diag, text="Title:", font=FONT_BOLD).pack(pady=5)
        title_in = ttk.Entry(diag, width=60); title_in.insert(0, sub.get("Titel")); title_in.pack(pady=5)
        
        tk.Label(diag, text="Intro Text:", font=FONT_BOLD).pack(pady=5)
        intro_in = tk.Text(diag, height=10, width=60, font=FONT_NORMAL); intro_in.insert("1.0", sub.get("Aufgabenbeschreibung")); intro_in.pack(pady=10)
        
        def commit():
            new_title = title_in.get().strip()
            new_intro = intro_in.get("1.0", tk.END).strip()
            new_view = f"Title: {new_title}\nIntro: {new_intro}"
            
            def finish():
                sub["Titel"] = new_title; sub["Aufgabenbeschreibung"] = new_intro
                self.refresh_teilgebiete(); self.update_breadcrumb(); diag.destroy()
            
            if old_view != new_view: self.show_diff_dialog("Teilgebiet", old_view, new_view, finish)
            else: diag.destroy()
            
        ttk.Button(diag, text="Änderungen speichern", command=commit, style="Success.TButton").pack(pady=10)

    def delete_teil(self):
        if self.current_bereich_idx is None or self.current_teil_idx is None: return
        sub = self.data[self.current_bereich_idx]["Teilgebiet"][self.current_teil_idx]
        if messagebox.askyesno("Bestätigen", f"Lösche Teilgebiet '{sub['Titel']}'?"):
            self.data[self.current_bereich_idx]["Teilgebiet"].pop(self.current_teil_idx)
            self.current_teil_idx = None
            self.refresh_teilgebiete(); self.refresh_tasks(); self.update_breadcrumb()

    # --- Task Management Logic ---

    def add_task(self):
        if self.current_bereich_idx is None or self.current_teil_idx is None: return
        sub = self.data[self.current_bereich_idx]['Teilgebiet'][self.current_teil_idx]
        tid = editor.generate_auto_id(self.current_bereich_idx, self.current_teil_idx, sub.get('UebungenListe', []))
        self.task_dialog(f"Neue Aufgabe in {sub['Titel']}", tid, sub['UebungenListe'])

    def edit_task_full(self):
        sel = self.tree.focus() or (self.tree.selection()[0] if self.tree.selection() else None)
        if not sel: return
        
        tid = self.tree.item(sel, 'values')[0]
        res = editor.find_task_by_id(self.data, tid)
        if res: self.task_dialog(f"✏️ Bearbeite Aufgabe {tid}", tid, None, res[3])

    def format_task_for_preview(self, t):
        opts = t.get("Moeglichkeiten", [])
        opt_str = "\n".join([f"  {i+1}. {m[0] if isinstance(m, list) else m}" for i, m in enumerate(opts)])
        return f"Q: {t.get('UebungsBeschreibung')}\nAntwortmöglichkeiten:\n{opt_str}\nKorrekt: {t.get('KorrekteAntwort')}\nInfo: {t.get('Infotext', 'None')}"

    def task_dialog(self, title, tid, target_list, task=None):
        # Universal dialog for adding/editing tasks
        d = tk.Toplevel(self.master); d.title(title); d.geometry("800x850"); d.configure(bg=COLOR_BG_SIDEBAR); d.grab_set()

        tk.Label(d, text=f"Task ID: {tid}", font=FONT_HEADER, bg=COLOR_BG_SIDEBAR, fg=COLOR_PRIMARY).pack(pady=15)

        tk.Label(d, text="Frage / Beschreibung:", font=FONT_BOLD, bg=COLOR_BG_SIDEBAR).pack(anchor="w", padx=30)
        q_in = tk.Text(d, height=4, font=FONT_NORMAL, relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1)
        if task: q_in.insert("1.0", task.get("UebungsBeschreibung"))
        q_in.pack(padx=30, pady=5, fill="x")

        # Options Management
        tk.Label(d, text="Antwortmöglichkeiten:", font=FONT_BOLD, bg=COLOR_BG_SIDEBAR).pack(anchor="w", padx=30, pady=(10,0))
        opt_box = tk.Frame(d, bg=COLOR_BG_SIDEBAR); opt_box.pack(fill="both", expand=True, padx=30)
        
        self.entries = []
        def add_opt_field(val=None):
            f = tk.Frame(opt_box, bg=COLOR_BG_SIDEBAR); f.pack(fill="x", pady=2)
            tk.Label(f, text=f"Antw {len(self.entries)+1}:", width=8, anchor="w", bg=COLOR_BG_SIDEBAR).pack(side="left")
            t = tk.Text(f, height=2, width=50, font=FONT_NORMAL, relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1)
            if val: t.insert("1.0", val[0] if isinstance(val, list) else str(val))
            t.pack(side="left", fill="x", expand=True); self.entries.append(t)

        if task:
            for o in task.get("Moeglichkeiten", []): add_opt_field(o)
        else:
            for _ in range(3): add_opt_field()

        ttk.Button(d, text="Antwortmöglichkeit Hinzufügen", command=add_opt_field).pack(pady=5)

        # Correct Answer Index
        ans_f = tk.Frame(d, bg=COLOR_BG_SIDEBAR); ans_f.pack(fill="x", padx=30, pady=10)
        tk.Label(ans_f, text="Korrekte Antwort # (1, 2, ...):", font=FONT_BOLD, bg=COLOR_BG_SIDEBAR).pack(side="left")
        idx_in = ttk.Entry(ans_f, width=8); idx_in.insert(0, str(task.get("KorrekteAntwort", 1) if task else 1)); idx_in.pack(side="left", padx=10)

        # Explanation Info
        tk.Label(d, text="Erklärung oder Info (Optional):", font=FONT_BOLD, bg=COLOR_BG_SIDEBAR).pack(anchor="w", padx=30)
        i_in = tk.Text(d, height=3, font=FONT_NORMAL, relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1)
        if task: i_in.insert("1.0", task.get("Infotext", "") or "")
        i_in.pack(padx=30, pady=5, fill="x")

        def save():
            opts = [[e.get("1.0", tk.END).strip()] for e in self.entries if e.get("1.0", tk.END).strip()]
            if not opts: return messagebox.showwarning("Error", "Es wird mindestens eine Antwortmöglichkeit benötigt!")
            
            try:
                idx = int(idx_in.get().strip())
                if not (1 <= idx <= len(opts)): raise ValueError()
            except: return messagebox.showwarning("Error", "Ungültiger Index für korrekte Antwort!")

            new_data = {"Uebung_id": tid, "UebungsBeschreibung": q_in.get("1.0", tk.END).strip(),
                        "Moeglichkeiten": opts, "KorrekteAntwort": idx, "Infotext": i_in.get("1.0", tk.END).strip() or None}

            old_p = self.format_task_for_preview(task) if task else "--- New Task ---"
            new_p = self.format_task_for_preview(new_data)

            def finalize():
                if task: task.update(new_data)
                else: target_list.append(new_data)
                self.refresh_tasks(); self.update_breadcrumb(); self.update_stats_label(); d.destroy()

            if old_p != new_p: self.show_diff_dialog("Aufgabendetails", old_p, new_p, finalize)
            else: d.destroy()

        # Footer Buttons
        f_btns = tk.Frame(d, bg=COLOR_BG_SIDEBAR); f_btns.pack(pady=20)
        ttk.Button(f_btns, text="Speichere Änderungen", command=save, style="Success.TButton").pack(side="left", padx=10)
        ttk.Button(f_btns, text="❌ Abbrechen", command=d.destroy).pack(side="left")

    def delete_task(self):
        sel = self.tree.focus()
        if not sel: return
        tid = self.tree.item(sel, 'values')[0]
        res = editor.find_task_by_id(self.data, tid)
        if res and messagebox.askyesno("Zustimmen", f"Lösche Aufgabe '{tid}'?"):
            self.data[res[0]]["Teilgebiet"][res[1]]["UebungenListe"].pop(res[2])
            self.refresh_tasks(); self.update_breadcrumb(); self.update_stats_label()

    def search_task(self):
        tid = simpledialog.askstring("Suchen", "Gib die Aufgaben-ID ein:")
        if not tid: return
        res = editor.find_task_by_id(self.data, tid)
        if res:
            # Navigate to it
            self.bereich_list.selection_clear(0, tk.END); self.bereich_list.selection_set(res[0]); self.on_bereich_select(None)
            self.teil_list.selection_clear(0, tk.END); self.teil_list.selection_set(res[1]); self.on_teil_select(None)
            self.master.update_idletasks()
            for item in self.tree.get_children():
                if str(self.tree.item(item, 'values')[0]) == str(tid):
                    self.tree.selection_set(item); self.tree.focus(item); self.tree.see(item); break
        else: messagebox.showinfo("Search", f"Aufgabe {tid} nicht gefunden.")

    # --- System Actions ---

    def show_statistics(self):
        s = tk.Toplevel(self.master); s.title("Stats"); s.geometry("500x600"); s.configure(bg=COLOR_BG_MAIN)
        tk.Label(s, text="KATALOG ÜBERSICHT", font=FONT_HEADER, bg=COLOR_BG_MAIN).pack(pady=20)
        
        total = editor.count_aufgaben(self.data)
        cats = len(self.data)
        
        f = tk.Frame(s, bg=COLOR_BG_MAIN); f.pack(pady=10, padx=40, fill="x")
        for k, v in [("Alle Aufgaben", total), ("Alle Kategorien", cats)]:
            row = tk.Frame(f, bg=COLOR_BG_MAIN); row.pack(fill="x", pady=5)
            tk.Label(row, text=k, bg=COLOR_BG_MAIN).pack(side="left"); tk.Label(row, text=str(v), font=FONT_BOLD, bg=COLOR_BG_MAIN).pack(side="right")

        tk.Label(s, text="Übersicht:", font=FONT_BOLD, bg=COLOR_BG_MAIN).pack(pady=10)
        l = tk.Listbox(s, font=FONT_NORMAL, relief="flat", highlightthickness=1); l.pack(fill="both", expand=True, padx=40, pady=10)
        for b in self.data:
            c = sum(len(t.get("UebungenListe", [])) for t in b.get("Teilgebiet", []))
            l.insert(tk.END, f" • {b['Uebungsbereich']}: {c} tasks")

    def save_data(self):
        if messagebox.askyesno("Speichern", "Lokal speichern und Version verteilen?"):
            if editor.save_and_commit(self.data): messagebox.showinfo("Fertig", "Erfolgreich überall aktualisiert!")
            else: messagebox.showwarning("Achtung", "Nur Lokal gespeichert, Cloudspeicher nicht möglich.")

if __name__ == "__main__":
    root = tk.Tk()
    try:
        icon_p = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Assets", "srhIcon.png")
        if os.path.exists(icon_p): root.iconphoto(True, tk.PhotoImage(file=icon_p))
    except: pass
    AufgabenGUI(root); root.mainloop()
