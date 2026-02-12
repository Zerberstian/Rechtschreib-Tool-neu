# TO-DO's

> Übergeordnete Sachen

- [x] Änderung To-Do's zu einer .md
- [x] Ordnerstruktur anpassen
- [x] Github Recherche ETag / Header
- [x] Festhalten der nötigen Zwischenschritte

> Aktuelles Ziel: Globale Versionierung

- [x] Anwendung soll auf GitHub JSON zugreifen können (statt nur lokal)
- [x] Anwendung soll einen Update Check beim Start machen
- [ ] Version soll auf GitHub ebenfalls automatisch inkrementiert werden

  `Dafür notwendig ist der Editor, der zulässt das folgende Änderungen gemacht werden können:`
  - [ ] Anzeigen der Aufgabe mit der eingebenen ID
  - [ ] Anpassen der Antwortmöglichkeiten
  - [ ] Anpassen der korrekten Antwort
  - [ ] Bearbeiten des Infotextes
  - [ ] Anpassen der Übungsbeschreibung
  - [ ] Übungs-ID automatisch generieren
  - [ ] Automatischer Github Commit
    - [ ] Verschlüsselung der Accountcredentials

---

work in progress:
- nur probleme mit "file-lock", seitens Windows, welches zu hochfrequente Updateraten erschwert ✅
-> eventueller Workaround mit process kill -> jedoch nur alles bis auf explorer.exe da das den Benutzer verwirren könnte
[Recherche dazu- treten dabei eventuell Probleme auf, welche zbsp. die json zerstören etc. - gilt auszutesten]
-> Idee Temp-Repo-Files-> hier müssen dann immer die ältesten gelöscht werden um nicht irgendwann Die Ordner zuzuspammen [es werden Temp-Repos verwendet, jedoch ältere noch nicht automatisch gelöscht]
-> Hinzugefügt werden müssen die Temp Repos auch zur .gitignore ✅

- bei den temp repos muss noch automatisches clean up stattfinden - welches die älteren löscht

ausstehend:
- Hinzufügen [hier fehlt noch die automatische Inkrementierung der Aufgaben-ID, welche aktuell noch händisch eingeben werden muss] und Entfernen neuer Aufgaben [noch komplett ausstehend]

- Verschlüsselung Accountcredentials

- Aufgaben sollen nun nicht mehr durch die Aufzählung - sprich die Stelle an der sie sich befinden, sondern durch die ID identifiziert und angewählt werden zum Bearbeiten
- Diese ID soll dementsprechend auch immer automatisch erstellt werden, und sich danach nie wieder ändern
- Dennoch ist die "Position" weiterhin wichtig und kann beibehalten werden, da hierdurch ja ausgezählt wird wie viele Aufgaben in welchem Bereich vorhanden sind

- kleines GUI für den Aufgabeneditor

- gitignore umfassend in der Parent-folder machen, sodass keine unnötigen Caches initial runtergeladen werden, und auch nicht das repo vollmüllen

- requirements.txt
(pip install requirements.txt)