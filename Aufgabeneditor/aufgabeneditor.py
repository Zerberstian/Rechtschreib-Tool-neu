import json
import os
import requests
from datetime import datetime
# used for pushing repo via subprocess
import subprocess
import shutil
# both used for handling file permissions during cleanup of temp repos
import stat
import time
# regex pattern used for finding the predecessor id for auto-id generation
import re
from Dtos import *

# pip install GitPython (requirements.txt) - as Git is essential for automatically pushing the new version to GitHub

def generate_auto_id(bereich_idx: int, teilgebiet_idx: int, uebungen_liste: list[TaskDto]) -> str:
    # generating new ids based on the predecessor id
    bereich_num = bereich_idx + 1
    teil_num = teilgebiet_idx + 1
    
    # getting the highest id (predecessor) from the selection
    max_num = 0
    for aufgabe in uebungen_liste:
        if aufgabe.task_id:
            match = re.match(rf'^{bereich_num}\.{teil_num}\.(\d+)$', aufgabe.task_id)
            if match:
                max_num = max(max_num, int(match.group(1)))
    
    return f"{bereich_num}.{teil_num}.{max_num + 1}"

def find_task_by_id(katalog: CatalogueDto, aufgabe_id: str) -> FoundTaskDto | None:
    for bereich_idx, bereich in enumerate(katalog.fields):
        for teil_idx, teil in enumerate(bereich.subfields):
            for aufgabe_idx, aufgabe in enumerate(teil.tasks):
                if aufgabe.task_id == aufgabe_id:
                    return FoundTaskDto(bereich_idx, teil_idx, aufgabe_idx, aufgabe)
    return None

def print_context(current_context: EditorContextDto) -> None:
    print("\n" + "─"*70)
    if not current_context:
        print("📍 HAUPTMENÜ".center(70))
    else:
        path = (current_context.bereich_name + " > "
                + current_context.teilgebiet_name + " > "
                + current_context.aufgabe_label)
        print(f"📍 {path}".center(70))
    print("─"*70)

def count_aufgaben(katalog: CatalogueDto) -> int:
    total = 0
    for bereich in katalog.fields:
        for teil in bereich.subfields:
            total += len(teil.tasks)
    return total

# max needs to be overwritten if there are picked more than those tasks (performance reasons)
def print_id_list(
        uebungen: list[TaskDto], verfuegbar_prefix: str = "", max_items: int = 1000
        ) -> list[TaskDto] | None:
    if not uebungen:
        print("❌ Keine Einträge gefunden")
        return None
    
    print(f"\n📋 {verfuegbar_prefix}Verfügbar:")
    for uebung in uebungen[:max_items]:
        task_id = uebung.task_id
        name = f"{task_id}: {uebung.task_description[:150]}"
        print(f"  {name}")
    
    if len(uebungen) > max_items:
        print(f" ... und {len(uebungen)-max_items} weitere")
    return uebungen

def print_numbered_list(
        liste: list[SubfieldDto] | list[FieldDto],
        verfuegbar_prefix: str = "",
        max_items: int = 100
        ) -> list[SubfieldDto] | list[FieldDto] | None:
    # only showing the section via numbers, but not the ids,
    # for better overview when picking a section to edit
    if not liste:
        print("❌ Keine Einträge gefunden")
        return None
    
    print(f"\n📋 {verfuegbar_prefix}Verfügbar:")
    display_count = min(len(liste), max_items)
    
    for i, bereich in enumerate(liste[:display_count]):
        if isinstance(bereich, FieldDto):
            name = bereich.title
        else:
            name = bereich.title
        
        print(f"  {i+1:3d}. {name}")

    if len(liste) > max_items:
        print(f" ... und {len(liste)-max_items} weitere")
    
    return liste

def load_credentials() -> ConfigDto:
    credentials_path = os.path.join(os.path.dirname(__file__), 'credentials.json')
    
    if not os.path.exists(credentials_path):
        print(f"🔴 credentials.json nicht gefunden in: {credentials_path}")
        print("📝 Erstelle Beispiel-Datei...")
        
        example_creds = ConfigDto(
            username="dein_github_username",
            token="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            ).to_dict()

        with open(credentials_path, 'w', encoding='utf-8') as f:
            json.dump(example_creds, f, indent=2, ensure_ascii=False)
        
        print("✅ Beispiel-credentials.json erstellt!")
        print("✏️  Bearbeite sie mit deinen echten GitHub-Daten:")
        print("   1. GitHub Token: https://github.com/settings/tokens")
        print("   2. 'repo' Permission aktivieren")
        print("   3. Token in credentials.json einfügen")
        print("⚠️ Gebe deine Credentials niemals weiter!")
        return ConfigDto(None, None) # no commit possible if no credentials provided
    
    try:
        with open(credentials_path, 'r', encoding='utf-8') as f: 
            creds = json.load(f)
        return ConfigDto.from_dict(creds)
    except (KeyError, json.JSONDecodeError) as e:
        print(f"🔴 credentials.json Formatfehler: {e}")
        print("Erwartet: {\"username\": \"deinname\", \"token\": \"ghp_...\"}")
        return ConfigDto(None, None)

def load_local_data() -> list[FieldDto]:
    cache_file = os.path.join(os.path.dirname(__file__), '..', 'Programmlogik', 'json_cache.json')
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache = CatalogueDto.from_dict(json.load(f))
            return cache.fields
    return []

def save_and_commit(katalog: CatalogueDto,
                    repo_path_base: str ="temp_repo"
                    ) -> bool:
    creds = load_credentials()

    # Fallback - but in this case the automatic distribution of
    # the updated version does not work, as the katalog is only stored locally
    if not creds.username or not creds.token:
        __save_local(katalog)
        return True
    
    username = creds.username
    token = creds.token
    try:
        __upload_github(katalog, username, token, repo_path_base)
        return True
    except subprocess.CalledProcessError as e:
        print(f"🔴 Git Error: {e.stderr or str(e)}")
        return False
    except Exception as e:
        print(f"🔴 Error: {e}")
        return False

def __create_new_katalog(katalog: CatalogueDto,
                  local_only: bool = True,
                  current_katalog: CatalogueDto | None = None) -> CatalogueDto:
    new_version = (999 if local_only
                   else (current_katalog.version + 1 if current_katalog else 999))

    new_katalog = CatalogueDto(
        version=new_version,
        last_updated=datetime.now().isoformat(),
        etag="local-only" if local_only else f'W/"{hash(str(katalog))}"',
        total_tasks=count_aufgaben(katalog),
        size=len(json.dumps(katalog.to_dict()).encode('utf-8')),
        fields=katalog.fields
    )
    return new_katalog

def __write_to_json(katalog: CatalogueDto, path: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(katalog.to_dict(), f, indent=2, ensure_ascii=False)

def __save_local(katalog: CatalogueDto) -> None:
    print("⚠️  Keine GitHub-Credentials → Nur lokal speichern")
    local_path = os.path.join(os.path.dirname(__file__),
                                '..',
                                'Programmlogik',
                                'Aufgabenkatalog.json')
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    new_katalog = __create_new_katalog(katalog)
    
    __write_to_json(new_katalog, local_path)
    
    print(f"🟢 Lokal gespeichert: {local_path}")
    print(f"📊 {count_aufgaben(new_katalog)} Aufgaben")

def __get_current_katalog() -> CatalogueDto | None:
    remote_url = "https://raw.githubusercontent.com/orphcvs/Aufgabenkatalog/main/Aufgabenkatalog.json"
    response = requests.get(remote_url, timeout=10)
    return CatalogueDto.from_dict(response.json())

def __clone_git_repo(target_repo_path: str) -> None:
    print("🔄 Cloning fresh repo...")
    clone_cmd = [
        'git', '-c', 'http.sslVerify=false', 'clone',
        '--depth=1', '--single-branch', '-b', 'main',
        'https://github.com/orphcvs/Aufgabenkatalog.git',
        target_repo_path
    ]

    subprocess.run(clone_cmd, capture_output=True, text=True, check=True, timeout=30)
    print("✅ Repo cloned!")

def __commit_git_repo(repo_path: str, username: str, commit_msg: str) -> None:
    subprocess.run(['git', '-C', repo_path, 'config', 'http.sslVerify', 'false'], check=True)
    subprocess.run(['git', '-C', repo_path, 'config', 'user.name', username], check=True)
    subprocess.run(['git', '-C', repo_path, 'config', 'user.email', f'{username}@users.noreply.github.com'], check=True)
    
    subprocess.run(['git', '-C', repo_path, 'add', 'Aufgabenkatalog.json'], check=True)
    subprocess.run(['git', '-C', repo_path, 'commit', '-m', commit_msg], check=True)

def __push_git_repo(repo_path: str, username: str, token: str) -> None:
    push_env = os.environ.copy()
    push_env['GIT_USERNAME'] = username
    push_env['GIT_PASSWORD'] = token
    subprocess.run(['git', '-C', repo_path, 'push', 'origin', 'main'], 
                    env=push_env, check=True, timeout=60)

def __upload_github(katalog: CatalogueDto,
                    username: str,
                    token: str,
                    repo_path_base: str
                    ) -> None:
    repo_path = os.path.join(os.path.dirname(__file__),
                             f'{repo_path_base}_{int(time.time())}')
    print(f"📁 temp-repo: {repo_path}")
    
    new_katalog = __create_new_katalog(katalog,
                                       local_only=False,
                                       current_katalog=__get_current_katalog())
    
    # no cleanup problems, as the programm is always cloned freshly
    __clone_git_repo(repo_path)
    
    json_path = os.path.join(repo_path, 'Aufgabenkatalog.json')
    __write_to_json(new_katalog, json_path)
    
    aufgaben_count = count_aufgaben(new_katalog)
    commit_msg = f"Update Aufgabenkatalog v{new_katalog.version} - {aufgaben_count} Aufgaben"
    __commit_git_repo(repo_path, username, commit_msg)
    __push_git_repo(repo_path, username, token)
    print(f"🟢 SUCCESS v{new_katalog.version}! ({aufgaben_count} tasks)")
    
    # now cleaning up old temp_repos, but keeping the latest 2 locally for safety
    cleanup_old_temps(os.path.dirname(repo_path), repo_path_base)

def __on_rm_error(func, path: str, _) -> None: # type: ignore
    # removing writing protection, and retrying if the file should be locked
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        print(f"⚠️ Konnte {path} trotz chmod-Approach nicht löschen: {e}")

def cleanup_old_temps(base_dir: str, prefix: str) -> None:
    try:
        temps = [d for d in os.listdir(base_dir) if d.startswith(prefix + '_')]

        if len(temps) <= 2:
            print("\nKein Cleanup nötig, nur wenige temp_repos gefunden.")
            return

        temps.sort(key=lambda x: os.path.getmtime(os.path.join(base_dir, x)), reverse=True)
        to_delete = temps[2:]

        for old_dir in to_delete:
            old_path = os.path.join(base_dir, old_dir)
            
            # 1. setting write permissions recursively for all files and folders inside the old temp repo
            for root, dirs, files in os.walk(old_path):
                for name in dirs + files:
                    p = os.path.join(root, name)
                    try:
                        os.chmod(p, stat.S_IWRITE)
                    except Exception as e:
                        print(f"⚠️ Schreibschutz konnte nicht entfernt werden {p}: {e}")
                        
            # 2. waiting if the file is still locked by another process (e.g. git)
            time.sleep(0.2)
            # 3. rmtree with debugging if it fails
            try:
                shutil.rmtree(old_path, onexc=__on_rm_error) # type: ignore
                print(f"✅ Gelöscht: {old_dir}")
            except Exception as e:
                print(f"❌ Konnte {old_dir} nicht löschen: {e}")
    except Exception as e:
        print(f"⚠️ Cleanup-Fehler: {e}")

def __task_menu_1or2(uebungsbereiche: list[FieldDto], choice: str) -> None:
    print_numbered_list(uebungsbereiche, "Bereiche - ")
    
    if choice == '2':
        try:
            bereich_idx = int(input(f"\n📍 Bereich-Nummer eingeben (1-{len(uebungsbereiche)}): ")) - 1
            if 0 <= bereich_idx < len(uebungsbereiche):
                current_context = EditorContextDto(
                    bereich_name=uebungsbereiche[bereich_idx].title,
                    teilgebiet_name="",
                    aufgabe_label=""
                )
                edit_bereich_menu(current_context, uebungsbereiche, bereich_idx, uebungsbereiche)
                current_context.clear()
            else:
                print("❌ Ungültige Nummer!")
        except ValueError:
            print("❌ Bitte Nummer eingeben!")

def __task_menu_3(current_context: EditorContextDto, uebungsbereiche: list[FieldDto]) -> None:
    new_bereich = {
        'Uebungsbereich': input("🆕 Neuer Bereichsname: "),
        'Teilgebiet': []
    }
    uebungsbereiche.append(new_bereich)
    return new_bereich
    print("✅ Neuer Bereich hinzugefügt!")

def edit_task_menu(uebungsbereiche: list[FieldDto]) -> None:
    current_context = EditorContextDto("", "", "")
    
    while True:
        print_context(current_context)
        print("📋 HAUPTMENÜ")
        print("1. Alle Bereiche anzeigen")
        print("2. Bereich bearbeiten") 
        print("3. Neuen Bereich hinzufügen")
        print("4. Aufgabe per ID suchen & bearbeiten")
        print("5. Speichern & GitHub Commit")
        print("6. Statistik")
        print("0. Beenden")
        
        choice = input("\nWähle (0-6): ").strip()
        
        match choice:
            case '1' | '2':
                __task_menu_1or2(uebungsbereiche, choice)
            case '3':
                pass
            case '4':
                pass
            case '5':
                pass
            case '6':
                pass
            case '0':
                pass
            case _:
                print("❌ Ungültige Auswahl!")

        if choice == '3':
            new_bereich = {
                'Uebungsbereich': input("🆕 Neuer Bereichsname: "),
                'Teilgebiet': []
            }
            uebungsbereiche.append(new_bereich)
            print("✅ Neuer Bereich hinzugefügt!")
        if choice == '4':
            task_id = input("\n🔍 Aufgabe-ID eingeben (z.B. 1.2.45): ").strip()
            result = find_task_by_id(uebungsbereiche, task_id)
            if result:
                bereich_idx, teil_idx, task_idx, aufgabe = result
                bereich_name = uebungsbereiche[bereich_idx].get('Uebungsbereich', f'Bereich {bereich_idx+1}')
                teil_name = uebungsbereiche[bereich_idx]['Teilgebiet'][teil_idx].get('Titel', f'Teilgebiet {teil_idx+1}')
                
                current_context.extend([bereich_name, teil_name, f"Aufgabe {task_id}"])
                print(f"\n✅ Aufgabe {task_id} gefunden!")
                print(f"   📂 {bereich_name} > {teil_name}")
                edit_single_task(uebungsbereiche[bereich_idx]['Teilgebiet'][teil_idx]['UebungenListe'], task_idx, uebungsbereiche)
                current_context.pop()
            else:
                print(f"❌ Aufgabe mit ID '{task_id}' nicht gefunden!")
        if choice == '5':
            if save_and_commit(uebungsbereiche): 
                print("✨ Update erfolgreich!")
            input("Enter zum Beenden...")
        if choice == '6':
            total_tasks = count_aufgaben(uebungsbereiche)
            print(f"📈 {total_tasks} Aufgaben in {len(uebungsbereiche)} Bereichen")
        if choice == '0':
            print("👋 Auf Wiedersehen!")
            break

def edit_bereich_menu(data, bereich_idx, data_param): # now also passing data, as it is needed for the quick preview of the newly created task
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
                    edit_teilgebiet_menu(teilgebiete, teil_idx, bereich_idx, data_param)
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
                if current_context: # checking context length for safety
                    current_context[0] = new_name
        
        elif choice == '0':
            break

def edit_teilgebiet_menu(uebungsbereich: FieldDto, teil_idx: int, bereich_idx: int, data):
    global current_context
    
    teil = (uebungsbereich.subfields[teil_idx]
                if len(uebungsbereich.subfields) > teil_idx
                else SubfieldDto.create_empty())

    while True:
        print_context()
        print(f"📚 {teil.title} ({len(teil.tasks)} Aufgaben)")
        print("1. Aufgaben auflisten")
        print("2. Aufgabe bearbeiten")
        print("3. Neue Aufgabe hinzufügen")
        print("4. Aufgabe per ID in diesem Teilgebiet")
        print("5. Titel/Beschreibung ändern")
        print("0. Zurück")
        
        choice = input("Wähle: ").strip()
        
        if choice == '1':
            aufgaben = teil.tasks
            print_id_list(aufgaben, "Aufgaben - ") # now only showing ids
            continue
        
        elif choice == '2':
            aufgaben = teil.tasks
            print_id_list(aufgaben, "Aufgaben - ")
            task_id = input("\n🔍 Aufgabe-ID eingeben (z.B. 3.1.5): ").strip()
            result = find_task_by_id([{'Teilgebiet': [teil]}], task_id)
            if result:
                _, _, task_idx, _ = result
                aufgabe = aufgaben[task_idx]
                current_context.append(f"Aufgabe {task_id}")
                edit_single_task(aufgaben, task_idx, data)
                current_context.pop()
            else:
                print(f"❌ Aufgabe '{task_id}' nicht gefunden!")
        
        elif choice == '4':
            aufgaben = teil.tasks
            task_id = input("\n🔍 Aufgabe-ID eingeben (z.B. 1.2.45): ").strip()
            result = find_task_by_id([{'Teilgebiet': [teil]}], task_id)
            if result:
                _, _, task_idx, _ = result
                aufgabe = aufgaben[task_idx]
                current_context.append(f"Aufgabe {task_id}")
                edit_single_task(aufgaben, task_idx, data)
                current_context.pop()
            else:
                print(f"❌ Aufgabe '{task_id}' nicht in diesem Teilgebiet gefunden!")

        
        elif choice == '3':
            auto_id = generate_auto_id(bereich_idx, teil_idx, teil.tasks)
            
            new_task = {
                'Uebung_id': auto_id,
                'UebungsBeschreibung': input("❓ UebungsBeschreibung (Frage): "),
                'Moeglichkeiten': json.loads(input("📋 Moeglichkeiten als JSON-Liste [[\"A\",\"B\",\"C\"]]: ") or '[["Option 1"], ["Option 2"], ["Option 3"]]'),
                'KorrekteAntwort': int(input("✅ KorrekteAntwort (Index 1-3): ") or 1),
                'Infotext': input("ℹ️ Infotext (optional): ")
            }
            # added new preview of created task, and auto-push if really created, so it does not need to be done manually via the menu
            print("\n" + "─"*70)
            print(" 👀 VORSCHAU - Neue Aufgabe:")
            print(f"   ID: {new_task['Uebung_id']}")
            print(f"   Frage: {new_task['UebungsBeschreibung']}")
            print(f"   Optionen: {new_task['Moeglichkeiten']}")
            moeg = new_task.get('Moeglichkeiten') or [] # previous handling did not allow "IstSpeziell"-Tasks to be configured by the editor, due to the index being out of range
            # old line: the korrekte_option = new_task['Moeglichkeiten'][new_task['KorrekteAntwort']-1][0] if new_task['Moeglichkeiten'] else '❌'
            idx = new_task.get('KorrekteAntwort', 0) - 1

            if 0 <= idx < len(moeg):
                # for normal tasks
                eintrag = moeg[idx]
                if isinstance(eintrag, (list, tuple)) and eintrag:
                    korrekte_option = eintrag[0]
                else:
                    # now also allowing strings (but still the indexes) in order to be able to handle "IstSpeziell"-Tasks properly, and allowing  
                    korrekte_option = eintrag
            else:
                korrekte_option = '❌'
            
            print(f"   Korrekt: {new_task['KorrekteAntwort']} → {korrekte_option}")
            if new_task['Infotext']:
                print(f"   Info: {new_task['Infotext']}")
            print("─"*70)
            
            confirm = input("✅ Aufgabe erstellen und direkt pushen? (JA/NEIN): ").strip().upper()
            if confirm == 'JA':
                teil.tasks.append(new_task)
                print("✅ Neue Aufgabe hinzugefügt!")
                
                if save_and_commit(data):
                    print("🎉 Automatischer GitHub-Commit erfolgreich!")
                else:
                    print("⚠️ Commit fehlgeschlagen - Aufgabe aber lokal gespeichert, versuche den Push manuell über das Hauptmenü!")
            else:
                print("❌ Erstellung abgebrochen.")
        
        elif choice == '5':
            new_titel = input("✏️ Neuer Titel (Enter=behalten): ") or teil.title
            if new_titel.strip():
                teil.title = new_titel
                if len(current_context) > 1:
                    current_context[-1] = new_titel
            teil.task_description = input("📝 Neue Beschreibung: ") or teil.task_description
        
        elif choice == '0':
            break

def edit_single_task(uebungen_liste: list[TaskDto], task_idx: int, katalog: CatalogueDto):
    task = uebungen_liste[task_idx]
    
    print(f"\n{'─'*70}")
    print(f"✏️ Aufgabe {task_idx+1} - ID: {task.task_id if task.task_id else 'no-id'} (🔒 AUTO-GENERATED)")
    print(f"{'─'*70}")
    
    beschreibung = task.task_description
    print(f"📝 UebungsBeschreibung: {beschreibung}")
    
    korrekt_idx = task.correct_answer
    moeglichkeiten = task.answer_options
    korrekte_option = moeglichkeiten[korrekt_idx-1] if moeglichkeiten and 0 < korrekt_idx <= len(moeglichkeiten) else "🥸 wahrscheinlich speziell"
    print(f"✅ KorrekteAntwort: {korrekt_idx} → '{korrekte_option}'")
    
    if moeglichkeiten:
        moeg_items = [f"({i+1})'{opt}'" for i, opt in enumerate(moeglichkeiten)]
        moeg_str = ", ".join(moeg_items)
        print(f"📋 Moeglichkeiten: {moeg_str}")
    
    infotext = task.information_text
    if infotext:
        print(f"ℹ️  Infotext: {infotext}")
    
    print(f"{'─'*70}")
    
    while True:
        print("\nWelches Feld bearbeiten?")
        print("1. UebungsBeschreibung")
        print("2. KorrekteAntwort (+Option)")
        print("3. Moeglichkeiten") 
        print("4. Infotext")
        print("5. Aufgabe LÖSCHEN")
        print("0. Fertig ✓")
        
        choice = input("Wähle (0-5): ").strip()
        
        if choice == '1':
            new_beschreibung = input(f"📝 UebungsBeschreibung (aktuell: '{beschreibung[:200]}'): ").strip()
            if new_beschreibung:
                task.task_description = new_beschreibung
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
                task.correct_answer = int(new_idx)
                korrekt_idx = int(new_idx)
                korrekte_option = moeglichkeiten[korrekt_idx-1]
                print(f"✅ Jetzt korrekt: {korrekt_idx} → '{korrekte_option}'")
            else:
                print("❌ Ungültige Nummer!")
        
        elif choice == '3':
            if moeglichkeiten:
                moeg_items = [f"({i+1})'{opt}'" for i, opt in enumerate(moeglichkeiten)]
                moeg_str = ", ".join(moeg_items)
                print(f"\nAktuelle Moeglichkeiten: {moeg_str}")
            action = input("Komplett neu eingeben? (j/n): ").strip().lower()
            if action == 'j':
                new_moeg = input("📋 Neue Liste (Komma-separiert): ").split(',')
                task.answer_options = [opt.strip() for opt in new_moeg if opt.strip()]
                moeglichkeiten = task.answer_options
                
                moeg_items = [f"({i+1})'{opt}'" for i, opt in enumerate(moeglichkeiten)]
                print(f"✅ Neue Optionen: {', '.join(moeg_items)}")
        
        elif choice == '4':
            new_infotext = input(f"ℹ️ Infotext (aktuell: '{infotext[:50] if infotext else ''}...'): ").strip()
            task.information_text = new_infotext if new_infotext else None
            print("✅ Aktualisiert!")
        
        elif choice == '5':
            confirm = input(f"\n⚠️ Aufgabe '{task.task_id}' LÖSCHEN? (JA/NEIN): ").strip().upper()
            if confirm == 'JA':
                uebungen_liste.pop(task_idx)
                print("🗑️  Aufgabe gelöscht!")
                if save_and_commit(katalog):
                    print("🎉 Automatischer GitHub-Commit erfolgreich!")
                else:
                    print("⚠️ Commit fehlgeschlagen - Aufgabenänderung aber lokal gespeichert, versuche den Push manuell über das Hauptmenü!")
            else:
                print("❌ Löschung abgebrochen.")
            
        elif choice == '0':
            print("\n🎉 Aufgabe komplett gespeichert!")
            break
        
        else:
            print("❌ Ungültige Auswahl!")
        
        # showing the updated task after each edit for better clarity
        print(f"\n📊 Status: {task.task_id} | {task.task_description[:30]}... | Korrekt: '{korrekte_option}'")

if __name__ == "__main__":
    
    cleanup_old_temps(os.path.dirname(__file__), 'temp_repo')
    print("═" * 70)
    print("📝 AUFGABENEDITOR V6 - AUTO-COMMIT NACH NEUER AUFGABE".center(70))
    print("═" * 70)
    
    aufgaben_data = load_local_data()
    if not aufgaben_data:
        print("🔴 Keine Aufgaben gefunden! Führe zuerst versioncheck.py aus.")
        exit(1)
    
    print(f"✅ {count_aufgaben(aufgaben_data)} Aufgaben aus {len(aufgaben_data)} Bereichen geladen")
    
    try:
        edit_task_menu(aufgaben_data)
    except KeyboardInterrupt:
        print("\n👋 wir sehen uns nie wieder!!!")