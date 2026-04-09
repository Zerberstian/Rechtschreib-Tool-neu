# Currently, tasks must be manually edited and pushed to [https://github.com/orphcvs/Aufgabenkatalog/tree/main]
# as the editor is not yet implemented
# However, version checking and auto-update on program startup work when changes are made

import requests
import json
import os
from datetime import datetime

RAW_URL = "https://raw.githubusercontent.com/orphcvs/Aufgabenkatalog/main/Aufgabenkatalog.json"
CACHE_FILE = "json_cache.json"

def _unwrap_nested_data(raw):
    # Recursively unwrap nested 'data' fields to get to the actual task list, in case the structure might change in the future
    data = raw
    while isinstance(data, dict) and 'data' in data:
        data = data['data']
    return data


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
    print("🌐 Checking for new task version...")
    # Fetch remote ETag via HEAD request - no file download needed
    try:
        response = requests.head(RAW_URL)
        remote_etag = response.headers.get('ETag', '')
        print(f"🌐 Remote ETag: {remote_etag[:20]}...")
    except:
        print("🔴 Network error")
        return load_local_cache()

    # Load local cache state (used for comparison / as fallback)
    local_etag = ""
    local_version = 0
    local_data = []

    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                local_etag = cache.get('etag', '')
                local_version = cache.get('version', 0)
                # FIX: Now Extracting the the actual task data
                data = _unwrap_nested_data(cache.get('data', {}))
                local_data = data if isinstance(data, list) else []
            print(f"⚪ Local task version available: v{local_version} ({count_aufgaben(local_data)} tasks)")
        except:
            print("🟠 Cache corrupted or not found")

    # Cache hit: ETags match and we have data 
    if remote_etag == local_etag and local_data:
        aufgaben_anzahl = count_aufgaben(local_data)
        print(f"🟣 {aufgaben_anzahl} tasks loaded from cache")
        return local_data

    # Cache miss: download and overwrite the old cache 
    print("🧭 New task version found, downloading...")
    try:
        response = requests.get(RAW_URL, timeout=10)
        remote_data_full = response.json()

        # Extract the full set of tasks from the GitHub payload
        remote_data = _unwrap_nested_data(remote_data_full)

        # Use the version stated in the GitHub file — no longer incremented locally
        remote_version = remote_data_full.get('version', local_version + 1)
        aufgaben_anzahl = count_aufgaben(remote_data)
        file_size = len(response.content)

        cache = {
            'version': remote_version,
            'lastUpdated': datetime.now().isoformat(),
            'etag': remote_etag,
            'totalAufgaben': aufgaben_anzahl,
            'size': file_size,
            'data': remote_data,  # The actual task data to be modified by the editor
        }

        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)

        print(f"🟢 Updated to version: v{remote_version}")
        print(f"🟣 {aufgaben_anzahl} tasks ({file_size} bytes)")
        print(f"🕙 {cache['lastUpdated'][:19]}")
        return remote_data

    except Exception as e:
        print(f"🔴 Download error: {e}")
        return local_data

"""
Using the cache, the offline version can always be loaded,
which is then updated when the program starts with network access.
Initially required to download the JSON.
"""

def load_local_cache():
    if not os.path.exists(CACHE_FILE):
        return []

    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)
            # Ignore older/more obfuscated structures by picking only the task data
            data = _unwrap_nested_data(cache.get('data', {}))
            data = data if isinstance(data, list) else []
            anzahl = count_aufgaben(data)
            print(f"⚪ Available Offline version: v{cache.get('version', 0)} ({anzahl} tasks)")
            return data
    except Exception as e:
        print(f"🔴 Cache load failed: {e}")
        return []

if __name__ == "__main__":
    print("═" * 60); print("Aufgabeneditor".center(60)); print("═" * 60 + "\n")
    aufgaben_data = check_json_version()
    total_aufgaben = count_aufgaben(aufgaben_data)

    print("\n" + "=" * 60)
    print(f"🟢 Available tasks: {total_aufgaben} total")

    # Access data:
    # aufgaben_data[0]['Teilgebiet'][0]['UebungenListe'][0]  -> First task
    print(f"🔵 {len(aufgaben_data)} exercise areas\n" + "=" * 60 + "\n")
    input("Press Enter to exit...")
