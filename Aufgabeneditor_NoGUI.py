#>> NOTIZEN / TO-DO'S <<
# Diese Anwendung soll später auf eine json-Datei die auf Github liegt zugreifen können, anstatt nur lokal zu funktionieren
# Folgende Sachen sollen mit der Terminalanwendung abänderbar und editierbar sein.
# - Die Möglichkeiten
# - Die Korrekte Antwort
# - Der Infotext
# - Die Übungsbeschreibung
# - [Die Übungs_ID soll automatisch erstellt werden]
#--------------------------------
# >>IDEEN UND GEDANKEN<<
# -> Technische Frage die sich stellt: IDs bleiben immer gleich, unabhängig davon ob hier ein Eintrag entfernt oder einer hinzugefügt wird, oder gibt es da einen intelligenteren Weg der keine redundanten Daten oder Verluste erstellt? 
# Vorschlag -> Neu Erstellte Aufgaben bekommen ihre ID anhand der ID der Vorgängeraufgabe innerhalb ihres Aufgabentypes zugewiesen
# Ideen zur Aktualisierung der json:
# - json auf GitHub hosten und von dort immer die Aktuelle Version ziehen
# - Einmal die Möglichkeit, als Öffentliches Projekt, oder aber Verknüpfung mit einem Account als private Repo (CopyRight)
#--------------------------------
# >>PROGRAMMVORGANG<<
# 1. Abfrage was soll gemacht werden...
#   1.1. Aufgabe bearbeiten
#       1.1.1. Abfrage Aufgaben-ID (sollte dann im GUI immer sichtbar und kopierbar sein, um Fehler schnell beheben zu können)
#              (Eventuell später mehr Filterung durch GUI Checkboxen möglich)
#           1.1.2. Welcher Teil ist Fehlerhaft? (Mehrfachauswahl möglich)
#                1.1.3. Anzeige der aktuellen Fehlerhaften Aufgabe 
#                   1.1.3.1. Anpassung der Anzahl der Möglichkeiten
#                       1.1.3.1.1. Auswahl welche Möglichkeiten gelöscht oder hinzugefügt werden sollen
#                       1.1.3.1.1..1 Die aktuell richtig markierte Antwort kann nicht gelöscht werden, hier eine Weiterleitung zu "Anpassung der Korrekten Antwort"
#                   1.1.3.2. Anpassung der Korrekten Antwort
#                   1.1.3.3. Anpassung Infotext
#                   1.1.3.4. Anpassung Übungsbeschreibung
#   1.2. Aufgabe hinzufügen
#       1.2.1 Zu Welchem Aufgabentyp / Titel?
#           1.2.2. Abfrage und Eingabe aller nötigen Einträge -> Ausgabe der erstellten Aufgabe mit entsprechender ID zur Eindeutigen Identifikation
#   1.3. Aufgabe entfernen
#       1.3.1 Aufgaben-ID eingeben
#           1.3.2. Zu löschende Aufgabe anzeigen und erneut nach Bestätigung fragen
#--------------------------------
#>> DONE <<#

