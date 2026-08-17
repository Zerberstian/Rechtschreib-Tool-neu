import os
import sys
import shutil

class Path:
    CACHE_FILENAME = "json_cache.json"

    def _frozen(self) -> bool:
        # Pyinstaller builds the .exe with the attribute "Frozen" for immutability.
        # We check for that to find out whether it's an exe or loose files.
        return getattr(sys, "frozen", False)

    def _project_root(self) -> str:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def data_dir(self) -> str:
        if self._frozen():
            return os.path.dirname(sys.executable)
        return os.path.join(self._project_root(), "program_logic")

    def base_dir(self) -> str:
        # dynamic base-path (important when trying to create .exe):
        # PyInstaller extracts bundled files to _MEIPASS, otherwise the project root is used
        if self._frozen():
            return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        return self._project_root()

    def setup_sys_path(self) -> None:
        # relative import of the modules (relative regarding base_dir)
        for folder in ("gui", "program_logic", "task_editor", "dtos"):
            sys.path.insert(0, os.path.join(self.base_dir(), folder))
        sys.path.insert(0, self.base_dir())

    def _bundled_cache(self) -> str:
        return os.path.join(self.base_dir(), "program_logic", self.CACHE_FILENAME)

    def cache_path(self) -> str:
        # Absolute path to the writable task cache used by every module.
        target = os.path.join(self.data_dir(), self.CACHE_FILENAME)
        if not os.path.exists(target):
            source = self._bundled_cache()
            if (source and os.path.exists(source)
                    and os.path.abspath(source) != os.path.abspath(target)):
                try:
                    os.makedirs(os.path.dirname(target), exist_ok=True)
                    shutil.copyfile(source, target)
                except OSError as e:
                    print(f"⚠️ Konnte Cache nicht initialisieren: {e}")
        return target
