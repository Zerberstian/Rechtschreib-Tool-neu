# Aktuell müssen die Aufgaben [https://github.com/orphcvs/Aufgabenkatalog/tree/main]
# Manuell noch geändert und gepushed werden, da der Editor noch nicht gecoded wurde
# Der Versionscheck, und das Autoupdate beim Programmstart funktioniert jedoch, wenn Änderungen vorgenommen werden

import requests
import json
import os
from datetime import datetime

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

def check_json_version():
    RAW_URL = "https://raw.githubusercontent.com/orphcvs/Aufgabenkatalog/main/Aufgabenkatalog.json"
    CACHE_FILE = "json_cache.json"
    
    print("🌐 Prüfe auf neue Aufgabenversion...")
    
    try:
        response = requests.head(RAW_URL)
        remote_etag = response.headers.get('ETag', '')
        print(f"🌐 Remote ETag: {remote_etag[:20]}...")
    except:
        print("🔴 Netzwerkfehler")
        return load_local_cache()

# Lokaler Cache wird geladen, um mit einer neuen Version verglichen zu werden, oder aber als Fallback für einen Netzausfall zu funktionieren. Die "eigentliche" Aufgaben.json befindet sich nur auf GitHub.
    local_etag = ""
    local_version = 0
    local_data = []
    
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                local_etag = cache.get('etag', '')
                local_version = cache.get('version', 0)
                local_data = cache.get('data', [])
            print(f"⚪ Lokal vorhandene Aufgabenversion: v{local_version} ({count_aufgaben(local_data)} Aufgaben)")
        except:
            print("🟠 Cache kaputt, oder nicht gefunden")
    
# Githubversion mit lokal vorhandener Version abgleichen
    if remote_etag == local_etag and local_data:
        aufgaben_anzahl = count_aufgaben(local_data)
        print(f"🟣 {aufgaben_anzahl} Aufgaben geladen")
        return local_data
    
# Updaten der Version, und Überspeicherung der Cache, wenn neue Version vorhanden
    print("🧭 Neue Aufgabenversion gefunden, Lade herunter...")
    try:
        response = requests.get(RAW_URL, timeout=10)
        remote_data = response.json()
        
        remote_version = local_version + 1
        aufgaben_anzahl = count_aufgaben(remote_data)
        file_size = len(response.content)
        
        cache = {
            'version': remote_version,
            'lastUpdated': datetime.now().isoformat(), # Die Update Zeit ebenfalls in der GitHub json festhalten, damit es auch hier wieder keine Abweichungen von Benutzer zu Benutzer gibt
            'etag': remote_etag,
            'totalAufgaben': aufgaben_anzahl,
            'size': file_size,
            'data': remote_data
        }
        
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
        
        print(f"🟢 Neue Aufgabenversion: v{remote_version}")
        print(f"🟣 {aufgaben_anzahl} Aufgaben ({file_size} Bytes)")
        print(f"🕙 {cache['lastUpdated'][:19]}")
        
        return remote_data
        
    except Exception as e:
        print(f"🔴 Download-Fehler: {e}")
        return local_data

# Mithilfe der Cache kann immer auch die Offlineversion geladen werden, welche anschließend geupdated wird, wenn das Programm mit Netzwerkzugriff gestartet wird
# Initial ist dieser erforderlich um die json herunterzuladen
def load_local_cache():
    cache_file = "json_cache.json"
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache = json.load(f)
            data = cache.get('data', [])
            anzahl = count_aufgaben(data)
            print(f"⚪ Vorhandene Offline-Aufgabenversion: v{cache.get('version', 0)} ({anzahl} Aufgaben)")
            return data
    return []

if __name__ == "__main__":
    print("═" * 60); print("Aufgabeneditor".center(60)); print("═" * 60+"\n")
    aufgaben_data = check_json_version()
    total_aufgaben = count_aufgaben(aufgaben_data)
    
    print("\n" + "=" * 60)
    print(f"🟢 Verfügbare Aufgaben: {total_aufgaben} insgesamt")
    
# Zugriff auf Daten:
# aufgaben_data[0]['Teilgebiet'][0]['UebungenListe'][0]  -> Erste Aufgabe
    print(f"🔵 {len(aufgaben_data)} Übungsbereiche"+"\n"+ "=" * 60 +"\n")
    input("Drücke Enter zum Beenden...")

# WICHTIG: Die Versionierung ist aktuell lokal. Bedeutet die Erstellung der Cache bestimmt die Version, so kann es dazu kommmen, das zwei unterschiedliche Leute zwar die exakt selben Aufgaben haben, es aber als unterschiedliche Version angezeigt wird
# ==> Das kann gefixed werden indem Die Version auch immer automatisch mit dazugeschrieben wird bei einem Commit über den Editor. So wird immer die tatsächliche Version auch angezeigt, und steht auch auf GitHub drinnen