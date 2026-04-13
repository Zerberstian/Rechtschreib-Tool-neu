# Currently, tasks must be manually edited and pushed to
# [https://github.com/orphcvs/Aufgabenkatalog/tree/main]
# as the editor is not yet implemented
# However, version checking and auto-update on program startup work when changes are made

import requests
import json
import os
from datetime import datetime
from Dtos.aufgabenkatalog_dto import AufgabenkatalogDto
from Dtos.uebungsbereich_dto import UebungsbereichDto

def count_aufgaben(data: list[UebungsbereichDto]) -> int:
    total = 0
    for bereich in data:
        teilgebiete = bereich.teilgebiete if bereich.teilgebiete else []
        for teil in teilgebiete:
            uebungen = teil.uebungsliste if teil.uebungsliste else []
            total += len(uebungen)
    return total

def check_json_version() -> list[UebungsbereichDto]:
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
                aufgabenkatalog = AufgabenkatalogDto.from_dict(cache)
                local_etag = aufgabenkatalog.etag
                local_version = aufgabenkatalog.version
                local_data = aufgabenkatalog.data if aufgabenkatalog.data else []
            print(f"⚪ Local task version available: v{local_version} "
                  f"({count_aufgaben(local_data)} tasks)")
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
        remote_data_full = AufgabenkatalogDto.from_dict(response.json())
        
        # Extracting the full set of tasks from GitHub
        remote_data = remote_data_full.data if remote_data_full.data else []
        
        # Now using the version stated in the Github-File - no longer incrementing locally
        remote_version = remote_data_full.version if remote_data_full.version else local_version + 1
        aufgaben_anzahl = count_aufgaben(remote_data)
        file_size = len(response.content)
        
        # Clean and structured cache format also containing metadata
        cache = AufgabenkatalogDto(
            version=remote_version,
            last_updated=datetime.now().isoformat(),
            etag=remote_etag,
            total_aufgaben=aufgaben_anzahl,
            size=file_size,
            data=remote_data
        )
        
        # Overwriting old cache
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache.to_dict(), f, indent=2, ensure_ascii=False)
        
        print(f"🟢 Updated to version: v{remote_version}")
        print(f"🟣 {aufgaben_anzahl} tasks ({file_size} bytes)")
        print(f"🕙 {cache.last_updated[:19]}")
        
        return remote_data
        
    except Exception as e:
        print(f"🔴 Download error: {e}")
        return local_data

# Using the cache, the offline version can always be loaded,
# which is then updated when the program starts with network access
# Initially required to download the JSON
def load_local_cache() -> list[UebungsbereichDto]:
    cache_file = "json_cache.json"
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                cache = AufgabenkatalogDto.from_dict(cache)
                data = cache.data if cache.data else []
                anzahl = count_aufgaben(data)
                print(f"⚪ Available Offline version: v{cache.version} ({anzahl} tasks)")
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
    # aufgaben_data[0].teilgebiete[0].uebungsliste[0]  -> First task
    print(f"🔵 {len(aufgaben_data)} exercise areas\n" + "=" * 60 +"\n")
    input("Press Enter to exit...")

# IMPORTANT: Versioning is currently local. Cache creation determines the version, 
# so different users might have identical tasks but different version numbers
# ==> This can be fixed by automatically writing the version during commits via the editor,
# ensuring the actual version is always displayed and stored on GitHub
