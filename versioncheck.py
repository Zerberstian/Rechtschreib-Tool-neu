# >> NOTIZEN / TO-DO'S <<
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
# >>PRIORISIERUNG<<
#   Muss:
#	    - Bearbeiten von Aufgaben, Anzeigen der Änderungen	
#	Soll:
#	    - Alles andere
#--------------------------------
# >> DONE <<
#
#
#
#
#--------------------------------

# Aktuell müssen die Aufgaben [https://github.com/orphcvs/Aufgabenkatalog/tree/main]
# Manuell noch geändert und gepushed werden, da der Editor noch nicht gecoded wurde
# Der Versionscheck, und das Autoupdate beim Programmstart funktioniert jedoch, wenn Änderungen vorgenommen werden

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
    
    print("🌐 Prüfe auf neue Aufgabenversion...")
    
    try:
        response = requests.head(RAW_URL)
        remote_etag = response.headers.get('ETag', '')
        print(f"🌐 Remote ETag: {remote_etag[:20]}...")
    except:
        print("🔴 Netzwerkfehler")
        return load_local_cache()

# Lokaler Cache wird geladen, um mit einer neuen Version verglichen zu werden, oder aber als Fallback für einen Netzausfall zu funktionieren. Die "eigentliche" Aufgaben.json befindet sich nur auf GitHub.
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
            print(f"⚪ Lokal vorhandene Aufgabenversion: v{local_version} ({count_aufgaben(local_data)} Aufgaben)")
        except:
            print("🟠 Cache kaputt, oder nicht gefunden")
    
# Githubversion mit lokal vorhandener Version abgleichen
    if remote_etag == local_etag and local_data:
        aufgaben_anzahl = count_aufgaben(local_data)
        print(f"🟣 {aufgaben_anzahl} Aufgaben geladen")
        return local_data
    
# Updaten der Version, und Überspeicherung der Cache, wenn neue Version vorhanden
    print("🧭 Neue Aufgabenversion gefunden, Lade herunter...")
    try:
        response = requests.get(RAW_URL, timeout=10)
        remote_data = response.json()
        
        remote_version = local_version + 1
        aufgaben_anzahl = count_aufgaben(remote_data)
        file_size = len(response.content)
        
        cache = {
            'version': remote_version,
            'lastUpdated': datetime.now().isoformat(), # Die Update Zeit ebenfalls in der GitHub json festhalten, damit es auch hier wieder keine Abweichungen von Benutzer zu Benutzer gibt
            'etag': remote_etag,
            'totalAufgaben': aufgaben_anzahl,
            'size': file_size,
            'data': remote_data
        }
        
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
        
        print(f"🟢 Neue Aufgabenversion: v{remote_version}")
        print(f"🟣 {aufgaben_anzahl} Aufgaben ({file_size} Bytes)")
        print(f"🕙 {cache['lastUpdated'][:19]}")
        
        return remote_data
        
    except Exception as e:
        print(f"🔴 Download-Fehler: {e}")
        return local_data

# Mithilfe der Cache kann immer auch die Offlineversion geladen werden, welche anschließend geupdated wird, wenn das Programm mit Netzwerkzugriff gestartet wird
# Initial ist dieser erforderlich um die json herunterzuladen
def load_local_cache():
    cache_file = "json_cache.json"
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache = json.load(f)
            data = cache.get('data', [])
            anzahl = count_aufgaben(data)
            print(f"⚪ Vorhandene Offline-Aufgabenversion: v{cache.get('version', 0)} ({anzahl} Aufgaben)")
            return data
    return []

if __name__ == "__main__":
    print("═" * 60); print("Aufgabeneditor".center(60)); print("═" * 60+"\n")
    aufgaben_data = check_json_version()
    total_aufgaben = count_aufgaben(aufgaben_data)
    
    print("\n" + "=" * 60)
    print(f"🟢 Verfügbare Aufgaben: {total_aufgaben} insgesamt")
    
# Zugriff auf Daten:
# aufgaben_data[0]['Teilgebiet'][0]['UebungenListe'][0]  -> Erste Aufgabe
    print(f"🔵 {len(aufgaben_data)} Übungsbereiche"+"\n"+ "=" * 60 +"\n")
    input("Drücke Enter zum Beenden...")

# WICHTIG: Die Versionierung ist aktuell lokal. Bedeutet die Erstellung der Cache bestimmt die Version, so kann es dazu kommmen, das zwei unterschiedliche Leute zwar die exakt selben Aufgaben haben, es aber als unterschiedliche Version angezeigt wird
# ==> Das kann gefixed werden indem Die Version auch immer automatisch mit dazugeschrieben wird bei einem Commit über den Editor. So wird immer die tatsächliche Version auch angezeigt, und steht auch auf GitHub drinnen