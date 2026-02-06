import json
import pprint

# JSON laden
with open("aufgaben_zu_formatieren.json", "r", encoding="utf-8") as f:
    daten = json.load(f)

# IDs vergeben
for bereich_index, bereich in enumerate(daten, start=1):
    # ID für Uebungsbereich
    bereich["Uebungsbereich_id"] = bereich_index

    # Unter-IDs für UebungenListe
    for uebung_index, uebung in enumerate(bereich.get("UebungenListe", []), start=1):
        uebung["uid"] = f"{bereich_index}.{uebung_index}"

# Ergebnis anzeigen
pprint.pp(daten)

# Optional: zurück in JSON speichern
with open("aufgaben_mit_ids.json", "w", encoding="utf-8") as f:
    json.dump(daten, f, ensure_ascii=False, indent=2)
