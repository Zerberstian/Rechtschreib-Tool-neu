
##### TO-DO's Projekt Rechtschreibtool

###### Übergeordnete Sachen

> Übersichtlichkeit und Struktur

- [ ] gitignore umfassend in der Parent-folder
- [ ] requirements.txt
- [ ] Executable erstellen
- [ ] Ordner aufräumen und files richtig benennen
- [ ] imports überall auf die gleiche weise und verständlich mit comments
- [ ] Clean Code - Complete Overhaul

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
- [ ] Komplett falsche oder veraltete Aufgaben löschen
- [ ] Die Reihenfolge beim Hinzufügen anpassen, sodass sie wie überall auch in der JSON ist (rein optisch, funktioniert trotzdem)

> Technisches

- [ ] Verschlüsselung der Accountcredentials

---

###### Zusammenführung GUI und Backend

> Programmlogik

- [x] Random Cycle Aufgaben richtig implementieren (siehe aufgabenlogik.py)
- [ ] Anzeige wiederholter und falsch beantworteter Aufgaben
- [ ] Komplette Statistik - Anzeigen bzw. abspeichern falsch beantworteter Fragen

> GUI

- [ ] Buttons deaktivieren wenn geklickt (Frame_Generation_Class.py)
- [ ] Immernoch funktionierende Button Highlights für falsch und richtig, auch mit dynamischer Frame Gen
- [ ] Aufgabenbereich-Pick mit Bereichcheckbox.py (siehe ebenfalls GUI_New.py bereits implementiert)
- [ ] Switch zu Frame_Generation_Class.py muss gemacht werden

---

###### Dokumentation

> Readme

- [ ] Readme mit Instruktionen
- [ ] Readme - Teil für Developer
- [ ] Readme - Teil für Benutzer

> Learnings

- [ ] Kurze Anpassungen
