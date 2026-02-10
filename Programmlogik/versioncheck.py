# Currently, tasks must be manually edited and pushed to [https://github.com/orphcvs/Aufgabenkatalog/tree/main]
# as the editor is not yet implemented
# However, version checking and auto-update on program startup work when changes are made

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
    
    print("🌐 Checking for new task version...")
    
    try:
        response = requests.head(RAW_URL)
        remote_etag = response.headers.get('ETag', '')
        print(f"🌐 Remote ETag: {remote_etag[:20]}...")
    except:
        print("🔴 Network error")
        return load_local_cache()

    # Local cache check
    local_etag = ""
    local_version = 0
    local_data = []
    
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                local_etag = cache.get('etag', '')
                local_version = cache.get('version', 0)
                # FIX: Extracting only the actual task-data
                data = cache.get('data', {})
                while isinstance(data, dict) and 'data' in data:
                    data = data['data']
                local_data = data if isinstance(data, list) else []
            print(f"⚪ Local task version available: v{local_version} ({count_aufgaben(local_data)} tasks)")
        except:
            print("🟠 Cache corrupted or not found")
    
    # Comparing ETags for version check
    if remote_etag == local_etag and local_data:
        aufgaben_anzahl = count_aufgaben(local_data)
        print(f"🟣 {aufgaben_anzahl} tasks loaded from cache")
        return local_data

    # The Download does now overwrite the old Cache, instead of appending the version-tag
    print("🧭 New task version found, downloading...")
    try:
        response = requests.get(RAW_URL, timeout=10)
        remote_data_full = response.json()
        
        # Extracting the full set of tasks from GitHub
        remote_data = remote_data_full
        while isinstance(remote_data, dict) and 'data' in remote_data:
            remote_data = remote_data['data']
        
        # Now using the version stated in the Github-File - no longer incrementing locally
        remote_version = remote_data_full.get('version', local_version + 1)
        aufgaben_anzahl = count_aufgaben(remote_data)
        file_size = len(response.content)
        
        # Clean and structured cache format also containing metadata
        cache = {
            'version': remote_version,
            'lastUpdated': datetime.now().isoformat(),
            'etag': remote_etag,
            'totalAufgaben': aufgaben_anzahl,
            'size': file_size,
            'data': remote_data  # this is the actual task data to be modified by the editor
        }
        
        # Overwriting old cache
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
        
        print(f"🟢 Updated to version: v{remote_version}")
        print(f"🟣 {aufgaben_anzahl} tasks ({file_size} bytes)")
        print(f"🕙 {cache['lastUpdated'][:19]}")
        
        return remote_data
        
    except Exception as e:
        print(f"🔴 Download error: {e}")
        return local_data

    RAW_URL = "https://raw.githubusercontent.com/orphcvs/Aufgabenkatalog/main/Aufgabenkatalog.json"
    CACHE_FILE = "json_cache.json"
    
    print("🌐 Checking for new task version...")
    
    try:
        response = requests.head(RAW_URL)
        remote_etag = response.headers.get('ETag', '')
        print(f"🌐 Remote ETag: {remote_etag[:20]}...")
    except:
        print("🔴 Network error")
        return load_local_cache()

    # Local cache is loaded to compare with new version or as fallback for network failure.
    # The "actual" tasks.json exists only on GitHub.
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
            print(f"⚪ Local task version available: v{local_version} ({count_aufgaben(local_data)} tasks)")
        except:
            print("🟠 Cache corrupted or not found")
    
    # Compare GitHub version with local version
    if remote_etag == local_etag and local_data:
        aufgaben_anzahl = count_aufgaben(local_data)
        print(f"🟣 {aufgaben_anzahl} tasks loaded")
        return local_data
    
    # Update version and overwrite cache if new version available
    print("🧭 New task version found, downloading...")
    try:
        response = requests.get(RAW_URL, timeout=10)
        remote_data = response.json()
        
        remote_version = local_version + 1
        aufgaben_anzahl = count_aufgaben(remote_data)
        file_size = len(response.content)
        
        cache = {
            'version': remote_version,
            'lastUpdated': datetime.now().isoformat(),  # Also store update time in GitHub JSON to ensure consistency across users
            'etag': remote_etag,
            'totalAufgaben': aufgaben_anzahl,
            'size': file_size,
            'data': remote_data
        }
        
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
        
        print(f"🟢 New task version: v{remote_version}")
        print(f"🟣 {aufgaben_anzahl} tasks ({file_size} bytes)")
        print(f"🕙 {cache['lastUpdated'][:19]}")
        
        return remote_data
        
    except Exception as e:
        print(f"🔴 Download error: {e}")
        return local_data

# Using the cache, the offline version can always be loaded, which is then updated when the program starts with network access
# Initially required to download the JSON
def load_local_cache():
    cache_file = "json_cache.json"
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                data = cache.get('data', {})
                # now ignoring older structure, or even a more obsfucated json file by just picking the data (tasks) alone
                while isinstance(data, dict) and 'data' in data:
                    data = data['data']
                data = data if isinstance(data, list) else []
                anzahl = count_aufgaben(data)
                print(f"⚪ Available Offline version: v{cache.get('version', 0)} ({anzahl} tasks)")
                return data
        except Exception as e:
            print(f"🔴 Cache load failed: {e}")
    return []


if __name__ == "__main__":
    print("═" * 60); print("Aufgabeneditor".center(60)); print("═" * 60+"\n")
    aufgaben_data = check_json_version()
    total_aufgaben = count_aufgaben(aufgaben_data)
    
    print("\n" + "=" * 60)
    print(f"🟢 Available tasks: {total_aufgaben} total")
    
    # Access data:
    # aufgaben_data[0]['Teilgebiet'][0]['UebungenListe'][0]  -> First task
    print(f"🔵 {len(aufgaben_data)} exercise areas\n" + "=" * 60 +"\n")
    input("Press Enter to exit...")

# IMPORTANT: Versioning is currently local. Cache creation determines the version, 
# so different users might have identical tasks but different version numbers
# ==> This can be fixed by automatically writing the version during commits via the editor,ensuring the actual version is always displayed and stored on GitHub
