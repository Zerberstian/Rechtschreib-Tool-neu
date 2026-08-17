import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
from dtos import *
from program_logic.path import Path

# pip install GitPython (requirements.txt) - as Git is essential for automatically pushing the new version to GitHub

def generate_auto_id(field_idx: int, subfield_idx: int, task_list: list[TaskDto]) -> str:
    # generating new ids based on the predecessor id
    field_num = field_idx + 1
    subfield_num = subfield_idx + 1

    # getting the highest id (predecessor) from the selection
    max_num = 0
    for task in task_list:
        if task.task_id:
            match = re.match(rf'^{field_num}\.{subfield_num}\.(\d+)$', task.task_id)
            if match:
                max_num = max(max_num, int(match.group(1)))

    return f"{field_num}.{subfield_num}.{max_num + 1}"

def find_task_by_id(catalogue: CatalogueDto, task_id: str) -> FoundTaskDto | None:
    for field_idx, field in enumerate(catalogue.fields):
        for subfield_idx, subfield in enumerate(field.subfields):
            for task_idx, task in enumerate(subfield.tasks):
                if task.task_id == task_id:
                    return FoundTaskDto(field_idx, subfield_idx, task_idx, task)
    return None

def count_tasks(catalogue: CatalogueDto) -> int:
    total = 0
    for field in catalogue.fields:
        for subfield in field.subfields:
            total += len(subfield.tasks)
    return total

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

def load_local_data() -> CatalogueDto:
    cache_file = Path().cache_path()
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            return CatalogueDto.from_dict(json.load(f))
    return CatalogueDto.create_empty()

def save_and_commit(catalogue: CatalogueDto,
                    repo_path_base: str ="temp_repo"
                    ) -> bool:
    creds = load_credentials()

    # Fallback - but in this case the automatic distribution of
    # the updated version does not work, as the katalog is only stored locally
    if not creds.username or not creds.token:
        __save_local(catalogue)
        return True

    username = creds.username
    token = creds.token
    try:
        __upload_github(catalogue, username, token, repo_path_base)
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
        total_tasks=count_tasks(katalog),
        size=len(json.dumps(katalog.to_dict()).encode('utf-8')),
        fields=katalog.fields
    )
    return new_katalog

def __write_to_json(katalog: CatalogueDto, path: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(katalog.to_dict(), f, indent=2, ensure_ascii=False)

def __save_local(catalogue: CatalogueDto) -> None:
    print("⚠️  Keine GitHub-Credentials → Nur lokal speichern")
    local_path = Path().cache_path()
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    new_catalogue = __create_new_katalog(catalogue)

    __write_to_json(new_catalogue, local_path)

    print(f"🟢 Lokal gespeichert: {local_path}")
    print(f"📊 {count_tasks(new_catalogue)} Aufgaben")

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

    aufgaben_count = count_tasks(new_katalog)
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
