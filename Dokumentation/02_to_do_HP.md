
##### TO-DO's Projekt Rechtschreibtool

###### Übergeordnete Sachen

> Übersichtlichkeit und Struktur

- [ ] gitignore umfassend in der Parent-folder
- [ ] requirements.txt
- [ ] Executable erstellen
- [ ] Ordner aufräumen und files richtig benennen

---

###### Aufgabeneditor

> Globale Versionierung, statt nur lokal

- [x] Anwendung soll auf GitHub JSON zugreifen können (statt nur lokal)
- [x] Anwendung soll einen Update Check beim Start machen
- [x] Version soll auf GitHub ebenfalls automatisch inkrementiert werden
- [x] Automatischer GitHub Commit
- [ ] Temp-Repo-Files - Dienen als Fallback - Es sollen automatisch ältere Versionen gelöscht werden

> Aktuell Fehlende Funktionalität für den Editierungsprozess

- [ ] Anzeigen der Aufgabe mit der eingebenen ID, statt Identifizierung über Position innerhalb des Aufgabenbereiches
- [x] Anpassen der Antwortmöglichkeiten
- [x] Anpassen der korrekten Antwort
- [x] Bearbeiten des Infotextes
- [x] Anpassen der Übungsbeschreibung
- [ ] Übungs-ID automatisch generieren beim Hinzufügen
- [ ] Aufgaben löschen
- [ ] Die Reihenfolge beim Hinzufügen anpassen, sodass sie wie überall auch in der JSON ist

> Technisches

- [ ] Verschlüsselung der Accountcredentials
- [ ] imports überall auf die gleiche weise und verständlich mit comments

---

###### Zusammenführung GUI und Backend

> Programmlogik

- [ ] Random Cycle Aufgaben richtig implementieren (siehe aufgabenlogik.py)

> GUI

- [ ] Buttons deaktivieren wenn geklickt (Frame_Generation_Class.py)
- [ ] Aufgabenbereich-Pick mit Bereichcheckbox.py (siehe ebenfalls GUI_New.py beereits implementiert
- [ ] Switch zu Frame_Generation_Class.py muss gemacht werden)
