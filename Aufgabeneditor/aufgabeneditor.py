# E:\07_Rechtschreibtool\Rechtschreib-Tool-neu\Aufgabeneditor\aufgabeneditor.py
# MIT NUMMERN-ANZEIGE BEI JEDER EINGABE

import json
import os
import requests
from datetime import datetime
import git  # pip install GitPython
import subprocess
import shutil

# GLOBALER KONTEXT
current_context = []

def print_context():
    """Zeigt immer an: Bereich > Teilgebiet > Aufgabe"""
    print("\n" + "─"*70)
    if not current_context:
        print("📍 HAUPTMENÜ".center(70))
    else:
        path = " > ".join(current_context)
        print(f"📍 {path}".center(70))
    print("─"*70)

def count_aufgaben(data):
    total = 0
    if isinstance(data, list):
        for bereich in data:
            teilgebiete = bereich.get('Teilgebiet', [])
            if isinstance(teilgebiete, list):
                for teil in teilgebiete:
                    uebungen = teil.get('UebungenListe', [])
                    total += len(uebungen)
    return total

def print_numbered_list(items, prefix="", max_items=100):
    """Zeigt nummerierte Liste mit echten Namen an"""
    if not items:
        print("❌ Keine Einträge gefunden")
        return None
    
    print(f"\n📋 {prefix}Verfügbar:")
    display_count = min(len(items), max_items)
    
    for i, item in enumerate(items[:display_count]):
        if isinstance(item, dict):
            # ✨ ECHTE JSON-Felder priorisieren
            if 'Uebungsbereich' in item:  # Bereich
                name = item['Uebungsbereich']
            elif 'Titel' in item:         # Teilgebiet
                name = item['Titel']
            elif 'UebungsBeschreibung' in item:  # AUFGABE - wichtigster Fix!
                name = f"{item.get('Uebung_id', 'ID?')}: {item['UebungsBeschreibung'][:50]}..."
            elif 'id' in item:
                name = f"{item['id']}: {item.get('frage', 'keine Frage')[:40]}..."
            else:
                name = f"Eintrag {i+1}"
        else:
            name = str(item)[:40] + "..." if len(str(item)) > 40 else str(item)
        
        print(f"  {i+1:3d}. {name}")
    
    if len(items) > max_items:
        print(f"  ... und {len(items)-max_items} weitere")
    
    return items

def load_credentials():
    # ✅ FIX: Suche credentials.json IM SELBEN ORDNER wie das Script
    credentials_path = os.path.join(os.path.dirname(__file__), 'credentials.json')
    
    if not os.path.exists(credentials_path):
        print(f"🔴 credentials.json nicht gefunden in: {credentials_path}")
        print("📝 Erstelle Beispiel-Datei...")
        
        # Erstelle Beispiel-credentials.json
        example_creds = {
            "username": "dein_github_username",
            "token": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        }
        
        with open(credentials_path, 'w', encoding='utf-8') as f:
            json.dump(example_creds, f, indent=2, ensure_ascii=False)
        
        print("✅ Beispiel-credentials.json erstellt!")
        print("✏️  Bearbeite sie mit deinen echten GitHub-Daten:")
        print("   1. GitHub Token: https://github.com/settings/tokens")
        print("   2. 'repo' Permission aktivieren")
        print("   3. Token in credentials.json einfügen")
        return None, None  # Kein Commit möglich ohne echte Credentials
    
    try:
        with open(credentials_path, 'r', encoding='utf-8') as f:
            creds = json.load(f)
        return creds['username'], creds['token']
    except (KeyError, json.JSONDecodeError) as e:
        print(f"🔴 credentials.json Formatfehler: {e}")
        print("Erwartet: {\"username\": \"deinname\", \"token\": \"ghp_...\"}")
        return None, None

def load_local_data():
    cache_file = os.path.join(os.path.dirname(__file__), '..', 'Programmlogik', 'json_cache.json')
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache = json.load(f)
            return cache.get('data', [])
    return []

def save_and_commit(data, repo_path_base='temp_repo'):
    username, token = load_credentials()
    
    # ✅ FALLBACK: Ohne Credentials nur lokal speichern
    if not username or not token:
        print("⚠️  Keine GitHub-Credentials → Nur lokal speichern")
        local_path = os.path.join(os.path.dirname(__file__), '..', 'Programmlogik', 'Aufgabenkatalog.json')
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        full_json = {
            'version': 999,
            'lastUpdated': datetime.now().isoformat(),
            'totalAufgaben': count_aufgaben(data),
            'data': data
        }
        
        with open(local_path, 'w', encoding='utf-8') as f:
            json.dump(full_json, f, indent=2, ensure_ascii=False)
        
        print(f"🟢 Lokal gespeichert: {local_path}")
        print(f"📊 {count_aufgaben(data)} Aufgaben")
        return True
    
    import time
    timestamp = int(time.time())
    repo_path = os.path.join(os.path.dirname(__file__), f'{repo_path_base}_{timestamp}')
    print(f"📁 Fresh temp: {repo_path}")
    
    remote_url = "https://raw.githubusercontent.com/orphcvs/Aufgabenkatalog/main/Aufgabenkatalog.json"
    try:
        response = requests.get(remote_url, timeout=10)
        current_json = response.json()
        new_version = current_json.get('version', 0) + 1
        
        full_json = {
            'version': new_version,
            'lastUpdated': datetime.now().isoformat(),
            'etag': f'W/"{hash(str(data))}"',
            'totalAufgaben': count_aufgaben(data),
            'size': len(json.dumps(data).encode('utf-8')),
            'data': data
        }
        
        # ✅ FRESH CLONE - KEIN CLEANUP PROBLEM!
        print("🔄 Cloning fresh repo...")
        clone_cmd = [
            'git', '-c', 'http.sslVerify=false', 'clone',
            '--depth=1', '--single-branch', '-b', 'main',
            'https://github.com/orphcvs/Aufgabenkatalog.git',
            repo_path
        ]
        
        subprocess.run(clone_cmd, capture_output=True, text=True, check=True, timeout=30)
        print("✅ Repo cloned!")
        
        # JSON schreiben
        json_path = os.path.join(repo_path, 'Aufgabenkatalog.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(full_json, f, indent=2, ensure_ascii=False)
        
        # Git via subprocess (sauber & stabil)
        subprocess.run(['git', '-C', repo_path, 'config', 'http.sslVerify', 'false'], check=True)
        subprocess.run(['git', '-C', repo_path, 'config', 'user.name', username], check=True)
        subprocess.run(['git', '-C', repo_path, 'config', 'user.email', f'{username}@users.noreply.github.com'], check=True)
        
        subprocess.run(['git', '-C', repo_path, 'add', 'Aufgabenkatalog.json'], check=True)
        subprocess.run(['git', '-C', repo_path, 'commit', '-m', 
                       f'Auto-update v{new_version} - {count_aufgaben(data)} tasks'], check=True)
        
        # Push mit Credentials
        push_env = os.environ.copy()
        push_env['GIT_USERNAME'] = username
        push_env['GIT_PASSWORD'] = token
        subprocess.run(['git', '-C', repo_path, 'push', 'origin', 'main'], 
                      env=push_env, check=True, timeout=60)
        
        print(f"🟢 SUCCESS v{new_version}! ({count_aufgaben(data)} tasks)")
        
        # 🧹 Optional: Alte temp_repos löschen (nur wenn leer/frei)
        cleanup_old_temps(os.path.dirname(repo_path), repo_path_base)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"🔴 Git Error: {e.stderr or str(e)}")
        return False
    except Exception as e:
        print(f"🔴 Error: {e}")
        return False

def cleanup_old_temps(base_dir, prefix):
    """Löscht ALLE temp_repo_* außer den neuesten 3 - NUR wenn möglich"""
    try:
        temps = [d for d in os.listdir(base_dir) if d.startswith(prefix + '_')]
        if len(temps) <= 3: 
            return  # Weniger als 3? Nicht löschen
        
        temps.sort(key=lambda x: os.path.getmtime(os.path.join(base_dir, x)), reverse=True)
        
        for old_dir in temps[3:]:  # Nur die 4+ löschen
            old_path = os.path.join(base_dir, old_dir)
            try:
                shutil.rmtree(old_path)
                print(f"🧹 Gelöscht: {old_dir}")
            except:
                pass  # Ignoriere locked folders
    except:
        pass  # Silent fail

def edit_task_menu(data):
    global current_context
    current_context = []
    
    while True:
        print_context()
        print("📋 HAUPTMENÜ")
        print("1. Alle Bereiche anzeigen")
        print("2. Bereich bearbeiten")
        print("3. Neuen Bereich hinzufügen")
        print("4. Speichern & GitHub Commit")
        print("5. Statistik")
        print("0. Beenden")
        
        choice = input("\nWähle (0-5): ").strip()
        
        if choice == '1' or choice == '2':
            print_numbered_list(data, "Bereiche - ")
            if choice == '1': continue
                
            try:
                bereich_idx = int(input("\n📍 Bereich-Nummer eingeben (1-6): ")) - 1
                if 0 <= bereich_idx < len(data):
                    current_context = [data[bereich_idx].get('Uebungsbereich', f'Bereich {bereich_idx+1}')]
                    edit_bereich_menu(data, bereich_idx)
                    current_context.pop()
                else:
                    print("❌ Ungültige Nummer!")
            except ValueError:
                print("❌ Bitte Nummer eingeben!")
        
        elif choice == '3':
            new_bereich = {
                'Uebungsbereich': input("🆕 Neuer Bereichsname: "),
                'Teilgebiet': []
            }
            data.append(new_bereich)
            print("✅ Neuer Bereich hinzugefügt!")
        
        elif choice == '4':
            if save_and_commit(data):  # repo_path_base entfällt
                print("✨ Update erfolgreich!")
            input("Enter zum Beenden...")

        elif choice == '5':
            total_tasks = count_aufgaben(data)
            print(f"📈 {total_tasks} Aufgaben in {len(data)} Bereichen")
        
        elif choice == '0':
            print("👋 Auf Wiedersehen!")
            break

def edit_bereich_menu(data, bereich_idx):
    global current_context
    bereich = data[bereich_idx]
    
    while True:
        print_context()
        print(f"📂 {bereich.get('Uebungsbereich')} ({len(bereich.get('Teilgebiet', []))} Teilgebiete)")
        print("1. Teilgebiete auflisten")
        print("2. Teilgebiet bearbeiten")
        print("3. Teilgebiet hinzufügen")
        print("4. Bereichsname ändern")
        print("0. Zurück")
        
        choice = input("Wähle: ").strip()
        
        if choice == '1' or choice == '2':
            teilgebiete = bereich.get('Teilgebiet', [])
            print_numbered_list(teilgebiete, "Teilgebiete - ")
            if choice == '1': continue
            
            try:
                teil_idx = int(input(f"\n📍 Teilgebiet-Nummer eingeben (1-{len(teilgebiete)}): ")) - 1
                if 0 <= teil_idx < len(teilgebiete):
                    current_context.append(teilgebiete[teil_idx].get('Titel', f'Teilgebiet {teil_idx+1}'))
                    edit_teilgebiet_menu(teilgebiete, teil_idx)
                    current_context.pop()
                else:
                    print("❌ Ungültige Nummer!")
            except ValueError:
                print("❌ Bitte Nummer eingeben!")
        
        elif choice == '3':
            new_teil = {
                'Titel': input("🆕 Teilgebiet-Titel: "),
                'Aufgabenbeschreibung': input("📝 Beschreibung: "),
                'UebungenListe': []
            }
            bereich.setdefault('Teilgebiet', []).append(new_teil)
        
        elif choice == '4':
            new_name = input("✏️ Neuer Bereichsname: ")
            if new_name.strip():
                bereich['Uebungsbereich'] = new_name
                current_context[0] = new_name
        
        elif choice == '0':
            break

def edit_teilgebiet_menu(teilgebiete, teil_idx):
    global current_context
    teil = teilgebiete[teil_idx]
    
    while True:
        print_context()
        print(f"📚 {teil.get('Titel')} ({len(teil.get('UebungenListe', []))} Aufgaben)")
        print("1. Aufgaben auflisten")
        print("2. Aufgabe bearbeiten")
        print("3. Neue Aufgabe hinzufügen")
        print("4. Titel/Beschreibung ändern")
        print("0. Zurück")
        
        choice = input("Wähle: ").strip()
        
        if choice == '1' or choice == '2':
            aufgaben = teil.get('UebungenListe', [])
            print_numbered_list(aufgaben, "Aufgaben - ", max_items=20)  # Weniger anzeigen
            if choice == '1': continue
            
            try:
                task_idx = int(input(f"\n📍 Aufgaben-Nummer eingeben (1-{len(aufgaben)}): ")) - 1
                if 0 <= task_idx < len(aufgaben):
                    aufgabe = aufgaben[task_idx]
                    current_context.append(f"Aufgabe {task_idx+1}: {aufgabe.get('Uebung_id', 'no-id')} - {aufgabe.get('UebungsBeschreibung', '')[:30]}")
                    edit_single_task(aufgaben, task_idx)
                    current_context.pop()
                else:
                    print("❌ Ungültige Nummer!")
            except ValueError:
                print("❌ Bitte Nummer eingeben!")
        
        elif choice == '3':
            # ✨ NEUE AUFGABE im echten JSON-Format
            new_task = {
                'Uebung_id': input("🆕 Uebung_id (z.B. 1.1.1): ") or f"{len(teil.get('UebungenListe', []))+1}",
                'UebungsBeschreibung': input("❓ UebungsBeschreibung (Frage): "),
                'Moeglichkeiten': json.loads(input("📋 Moeglichkeiten als JSON-Liste [ [\"A\",\"B\",\"C\"] ]: ")) or ["Option 1", "Option 2", "Option 3"],
                'KorrekteAntwort': int(input("✅ KorrekteAntwort (Index 1-3): ") or 1),
                'Infotext': input("ℹ️ Infotext (optional): ")
            }
            teil.setdefault('UebungenListe', []).append(new_task)
            print("✅ Neue Aufgabe hinzugefügt!")
        
        elif choice == '4':
            new_titel = input("✏️ Neuer Titel (Enter=behalten): ") or teil.get('Titel', '')
            if new_titel.strip():
                teil['Titel'] = new_titel
                current_context[-1] = new_titel
            teil['Aufgabenbeschreibung'] = input("📝 Neue Beschreibung: ") or teil.get('Aufgabenbeschreibung', '')
        
        elif choice == '0':
            break

def edit_single_task(uebungen_liste, task_idx):
    task = uebungen_liste[task_idx]
    
    # 🎨 VOLLSTÄNDIGE AUFGABE ANZEIGEN
    print(f"\n{'─'*70}")
    print(f"✏️ Aufgabe {task_idx+1} - ID: {task.get('Uebung_id', 'no-id')}")
    print(f"{'─'*70}")
    
    # UebungsBeschreibung
    beschreibung = task.get('UebungsBeschreibung', '')
    print(f"📝 UebungsBeschreibung: {beschreibung}")
    
    # KorrekteAntwort MIT zugehöriger Option
    korrekt_idx = task.get('KorrekteAntwort', 0)
    moeglichkeiten = task.get('Moeglichkeiten', [])
    korrekte_option = moeglichkeiten[korrekt_idx-1] if moeglichkeiten and 0 < korrekt_idx <= len(moeglichkeiten) else "❌ Ungültig"
    print(f"✅ KorrekteAntwort: {korrekt_idx} → '{korrekte_option}'")
    
    # Moeglichkeiten kompakt
    if moeglichkeiten:
        # ✅ FIX: Backslash außerhalb der f-string Expression
        moeg_items = [f"({i+1})'{opt}'" for i, opt in enumerate(moeglichkeiten)]
        moeg_str = ", ".join(moeg_items)
        print(f"📋 Moeglichkeiten: {moeg_str}")
    
    # Infotext
    infotext = task.get('Infotext', '')
    if infotext:
        print(f"ℹ️  Infotext: {infotext}")
    
    print(f"{'─'*70}")
    
    # 🎯 GEZIELTE BEARBEITUNG - Benutzer wählt Feld
    while True:
        print("\nWelches Feld bearbeiten?")
        print("1. UebungsBeschreibung")
        print("2. KorrekteAntwort (+Option)")
        print("3. Moeglichkeiten")
        print("4. Infotext")
        print("5. Uebung_id")
        print("0. Fertig ✓")
        
        choice = input("Wähle (0-5): ").strip()
        
        if choice == '1':
            new_beschreibung = input(f"📝 UebungsBeschreibung (aktuell: '{beschreibung[:50]}...'): ").strip()
            if new_beschreibung:
                task['UebungsBeschreibung'] = new_beschreibung
                beschreibung = new_beschreibung
                print("✅ Aktualisiert!")
        
        elif choice == '2':
            print(f"\nAktuelle korrekte Antwort: {korrekt_idx} → '{korrekte_option}'")
            if moeglichkeiten:
                print("Verfügbare Optionen:")
                for i, opt in enumerate(moeglichkeiten):
                    print(f"  {i+1}. '{opt}'")
            
            new_idx = input("✅ Neue KorrekteAntwort (Nummer 1-3): ").strip()
            if new_idx.isdigit() and 1 <= int(new_idx) <= len(moeglichkeiten):
                task['KorrekteAntwort'] = int(new_idx)
                korrekt_idx = int(new_idx)
                korrekte_option = moeglichkeiten[korrekt_idx-1]
                print(f"✅ Jetzt korrekt: {korrekt_idx} → '{korrekte_option}'")
            else:
                print("❌ Ungültige Nummer!")
        
        elif choice == '3':
            print(f"\nAktuelle Moeglichkeiten: {moeg_str}")
            action = input("Komplett neu eingeben? (j/n): ").strip().lower()
            if action == 'j':
                new_moeg = input("📋 Neue Liste (Komma-separiert): ").split(',')
                task['Moeglichkeiten'] = [opt.strip() for opt in new_moeg if opt.strip()]
                moeglichkeiten = task['Moeglichkeiten']
                
                # ✅ FIX: Backslash-Problem gelöst durch Zwischenschritt
                moeg_items = [f"({i+1})'{opt}'" for i, opt in enumerate(moeglichkeiten)]
                print(f"✅ Neue Optionen: {', '.join(moeg_items)}")
        
        elif choice == '4':
            new_infotext = input(f"ℹ️ Infotext (aktuell: '{infotext[:50]}...'): ").strip()
            task['Infotext'] = new_infotext if new_infotext else None
            print("✅ Aktualisiert!")
        
        elif choice == '5':
            new_id = input(f"🆕 Uebung_id (aktuell: '{task.get('Uebung_id', 'no-id')}'): ").strip()
            if new_id:
                task['Uebung_id'] = new_id
                print("✅ ID aktualisiert!")
        
        elif choice == '0':
            print("\n🎉 Aufgabe komplett gespeichert!")
            break
        
        else:
            print("❌ Ungültige Auswahl!")
        
        # 🔄 Aufgaben-Zusammenfassung nach Änderung
        print(f"\n📊 Status: {task.get('Uebung_id')} | {task.get('UebungsBeschreibung', '')[:30]}... | Korrekt: '{korrekte_option}'")

if __name__ == "__main__":
    print("═" * 70)
    print("📝 AUFGABENEDITOR V3 - MIT NUMMERANZEIGE".center(70))
    print("═" * 70)
    
    aufgaben_data = load_local_data()
    if not aufgaben_data:
        print("🔴 Keine Aufgaben gefunden! Führe zuerst versioncheck.py aus.")
        exit(1)
    
    print(f"✅ {count_aufgaben(aufgaben_data)} Aufgaben aus {len(aufgaben_data)} Bereichen geladen")
    
    try:
        edit_task_menu(aufgaben_data)
    except KeyboardInterrupt:
        print("\n👋 Abgebrochen, wir sehen uns nie wieder!")
