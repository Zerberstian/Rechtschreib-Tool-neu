import os
import sys
import shutil

CACHE_FILENAME = "json_cache.json"


def _frozen() -> bool:
    # Pyinstaller builds the .exe with the attribute "Frozen" for immutability.
    # We check for that to find out whether it's an exe or loose files.
    return getattr(sys, "frozen", False)


def _project_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def data_dir() -> str:
    if _frozen():
        return os.path.dirname(sys.executable)
    return os.path.join(_project_root(), "Programmlogik")


def _bundled_cache() -> str | None:
    if _frozen():
        meipass = getattr(sys, "_MEIPASS", None)
        if not meipass:
            return None
        return os.path.join(meipass, "Programmlogik", CACHE_FILENAME)
    return os.path.join(_project_root(), "Programmlogik", CACHE_FILENAME)


def cache_path() -> str:
    # Absolute path to the writable task cache used by every module.
    target = os.path.join(data_dir(), CACHE_FILENAME)
    if not os.path.exists(target):
        source = _bundled_cache()
        if (source and os.path.exists(source)
                and os.path.abspath(source) != os.path.abspath(target)):
            try:
                os.makedirs(os.path.dirname(target), exist_ok=True)
                shutil.copyfile(source, target)
            except OSError as e:
                print(f"⚠️ Konnte Cache nicht initialisieren: {e}")
    return target
