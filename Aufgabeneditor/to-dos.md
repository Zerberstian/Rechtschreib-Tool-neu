
# Aufgabeneditor

##  TO-DOs

- **Ziel**: Anwendung soll auf GitHub JSON zugreifen können (statt nur lokal)

- **Editierbare Felder**:
  - Möglichkeiten
  - Korrekte Antwort
  - Infotext
  - Übungsbeschreibung
  - `[Übungs-ID automatisch generieren]`

---

## Programmablauf

``` markdown
1. Hauptmenü: Was soll gemacht werden?
   ├── 1.1 Aufgabe bearbeiten
   │    ├── 1.1.1 Aufgaben-ID eingeben (immer sichtbar/kopierbar)
   │    ├── 1.1.2 Fehlerhafte Teile auswählen (Mehrfachauswahl)
   │    └── 1.1.3 Bearbeitung:
   │         ├── Anzahl Möglichkeiten ± (richtige Antwort nicht löschbar)
   │         ├── Korrekte Antwort ändern
   │         ├── Infotext ändern
   │         └── Übungsbeschreibung ändern
   ├── 1.2 Aufgabe hinzufügen
   │    ├── 1.2.1 Aufgabentyp/Titel wählen
   │    └── 1.2.2 Alle Felder eingeben → ID generieren + Vorschau
   └── 1.3 Aufgabe entfernen
        ├── 1.3.1 Aufgaben-ID eingeben
        └── 1.3.2 Bestätigung nach Anzeige
```

---

## Priorisierung

| Status | Aufgaben |
| --- | --- |
| **Muss** | Aufgabe bearbeiten + Änderungen anzeigen |
| **Soll** | Hinzufügen, Entfernen, GitHub-Integration |

---

### Unterschied zwischen lokaler und Remote Version

ETag löst dein Problem nicht vollständig. Er ist nur ein Identifikator für **genaue Inhaltsgleichheit** der Datei, aber keine zentrale Versionsnummer – bei jedem Download wird einfach `local_version + 1` gesetzt, was pro Benutzer inkrementell läuft.

> Keine standard HTTP-Header-Lösung

- GitHub stellt **keinen** Versions-Header wie `X-Version` oder `Content-Version` für Raw-Dateien bereit.
- Last-Modified (Datum der letzten Änderung) ist verfügbar, aber nur grob und nicht commit-genau.
- ETag ändert sich zwar bei Updates, ist aber ein Hash-String (z.B. `"a1b2c3d4"`), kein lesbarer Versionszähler.

> Lösung: Version in JSON einbetten

Direktes Einfügen eines `version`-Feldes in die `Aufgabenkatalog.json`:

```json
{
  "version": 42,
  "lastCommit": "abc1234",
  "data": [ ... ]
}
```

 Im Editor-Programm (GitHub Actions oder pre-commit-hook)

```python
# Bei jedem Commit automatisch erhöhen
import json
with open('Aufgabenkatalog.json', 'r+') as f:
    data = json.load(f)
    data['version'] = data.get('version', 0) + 1
    json.dump(data, f)
```

Dann im Client-Code:

```python
remote_data = response.json()
remote_version = remote_data.get('version', 0)
cache = {
    'version': remote_version,  # <- zentrale Version!
    'etag': remote_etag,
    'data': remote_data
}
```

> Vorteile

- Alle Benutzer haben **exakt dieselbe Versionsnummer** (z.B. v42)
- Fallback auf ETag bleibt für Integrität.
- Lesbar und erweiterbar (z.B. durch einen `changelog` ).

---

> Alternative: GitHub Releases/Tags

GitHub Releases erstellen und hole `latest release tag` via API:

```python
release_resp = requests.get("https://api.github.com/repos/orphcvs/Aufgabenkatalog/releases/latest")
remote_version = release_resp.json()['tag_name']  # z.B. "v1.2.3"
```

Aber das ist komplexer als JSON-Version.
[siehe Docs](https://docs.github.com/ja/rest/about-the-rest-api/api-versions)

---

#### Entscheidung

JSON-Feld + auto increment ist einfach und verwirrungsfrei.

---

### ID-Generierung, beim Hinzufügen von Aufgaben

>Problem:

IDs sollen stabil bleiben (auch bei Löschungen/Hinzufügungen)
>Lösung:

Neue Aufgaben bekommen ID basierend auf Vorgängeraufgabe desselben Typs

---

## DONE

- Automatisches Laden aktueller Aufgabenversion von GitHub (via Terminal)
