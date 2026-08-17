# Currently, tasks must be manually edited and pushed to
# [https://github.com/orphcvs/Aufgabenkatalog/tree/main]
# as the editor is not yet implemented
# However, version checking and auto-update on program startup work when changes are made

import requests
import json
import os
from datetime import datetime
from dtos import *
from program_logic.path import Path

class VersionCheck:
    RAW_URL = "https://raw.githubusercontent.com/orphcvs/Aufgabenkatalog/main/Aufgabenkatalog.json"

    def __init__(self):
        self.cache_file = Path().cache_path()

    # Using the cache, the offline version can always be loaded,
    # which is then updated when the program starts with network access
    # Initially required to download the JSON
    def load_local_cache(self) -> CatalogueDto:
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return CatalogueDto.from_dict(json.load(f))
            except Exception as e:
                print(f"🔴 Cache load failed: {e}")
        return CatalogueDto.create_empty()

    def save_cache(self, catalogue: CatalogueDto) -> None:
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(catalogue.to_dict(), f, indent=2, ensure_ascii=False)

    def check_json_version(self) -> list[FieldDto]:
        local = self.load_local_cache()
        if local.fields:
            print(f"⚪ Local task version available: v{local.version} ({local.total_tasks} tasks)")

        print("🌐 Checking for new task version...")
        try:
            remote_etag = requests.head(self.RAW_URL, timeout=10).headers.get('ETag', '')
            print(f"🌐 Remote ETag: {remote_etag[:20]}...")
        except requests.RequestException:
            print("🔴 Network error")
            return local.fields

        if remote_etag == local.etag and local.fields:
            print(f"🟣 {local.total_tasks} tasks loaded from cache")
            return local.fields

        print("🧭 New task version found, downloading...")
        try:
            response = requests.get(self.RAW_URL, timeout=10)
            remote = CatalogueDto.from_dict(response.json())
            remote.version = remote.version or local.version + 1
            remote.etag = remote_etag
            remote.last_updated = datetime.now().isoformat()
            remote.size = len(response.content)

            self.save_cache(remote)

            print(f"🟢 Updated to version: v{remote.version}")
            print(f"🟣 {remote.total_tasks} tasks ({remote.size} bytes)")
            print(f"🕙 {remote.last_updated[:19]}")
            return remote.fields
        except Exception as e:
            print(f"🔴 Download error: {e}")
            return local.fields


if __name__ == "__main__":
    print("═" * 60); print("Aufgabenkatalog".center(60)); print("═" * 60 + "\n")
    task_data = VersionCheck().check_json_version()

    print("\n" + "=" * 60)
    print(f"🔵 {len(task_data)} exercise areas\n" + "=" * 60 + "\n")
    input("Press Enter to exit...")

# IMPORTANT: Versioning is currently local. Cache creation determines the version,
# so different users might have identical tasks but different version numbers
# ==> This can be fixed by automatically writing the version during commits via the editor,
# ensuring the actual version is always displayed and stored on GitHub
