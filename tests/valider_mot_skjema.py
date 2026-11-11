#!/usr/bin/env python3
"""Skjemavalidering: fixturene i tests/fixtures/ mot JSON-skjemaet fra `wenche skjema`.

`wenche skjema` (Wenche 1.16.0 og nyere) skriver ut et JSON Schema generert fra Wenches
egen datamodell. Skjemaet avviser felt Wenche ikke kjenner, feil type, ugyldige valg og
manglende påkrevde felt, med sti til feltet. Validatoren (`wenche valider-aarsregnskap`)
sier bare om configen er gyldig, ikke om et felt Bodil skriver ble ignorert; denne sjekken
fanger at et felt er døpt om, fjernet eller har fått en annen type i Wenche.

Krever `wenche` (>= 1.16.0) og `jsonschema` installert.

Exit 0 = alle fixtures validerer. Exit 1 = minst ett avvik. Exit 2 = fikk ikke tak i skjemaet.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    print("FEIL: pakken 'jsonschema' er ikke installert. Kjør `pip install jsonschema`.")
    sys.exit(2)

FIXTURES = sorted((Path(__file__).parent / "fixtures").glob("config.*.yaml"))


def hent_skjema() -> dict:
    """Skjemaet fra den installerte Wenche-pakken, via CLI-en (det dokumenterte grensesnittet)."""
    try:
        resultat = subprocess.run(["wenche", "skjema"], capture_output=True, text=True, check=True)
    except FileNotFoundError:
        print("FEIL: fant ikke kommandoen 'wenche'. Kjør `pip install wenche`.")
        sys.exit(2)
    except subprocess.CalledProcessError as e:
        print("FEIL: `wenche skjema` feilet. Kommandoen krever Wenche 1.16.0 eller nyere.")
        print(e.stderr.strip())
        sys.exit(2)
    return json.loads(resultat.stdout)


def json_klar(obj: object) -> object:
    """YAML gir datoer som date-objekter; i JSON er de tekst (skjemaet sier `format: date`)."""
    return json.loads(json.dumps(obj, default=lambda o: o.isoformat()))


def sti(deler) -> str:
    """Feltsti som i Wenches egne meldinger: `aksjonaerer[0].navn`."""
    tekst = ""
    for del_ in deler:
        if isinstance(del_, int):
            tekst += f"[{del_}]"
        else:
            tekst += f".{del_}" if tekst else str(del_)
    return tekst or "(toppnivå)"


def main() -> int:
    if not FIXTURES:
        print("FEIL: fant ingen fixtures i tests/fixtures/.")
        return 2

    validator = Draft202012Validator(hent_skjema(), format_checker=FormatChecker())
    feilet = False

    for fixture in FIXTURES:
        with fixture.open(encoding="utf-8") as f:
            config = json_klar(yaml.safe_load(f))

        avvik = sorted(validator.iter_errors(config), key=lambda e: list(e.absolute_path))
        if avvik:
            feilet = True
            print(f"Skjemavalidering FEILET: {fixture.name}")
            for e in avvik:
                print(f"  - {sti(e.absolute_path)}: {e.message}")
        else:
            print(f"  {fixture.name}: validerer mot skjemaet.")

    if feilet:
        print(
            "\nWenche har sannsynligvis døpt om, fjernet eller endret typen på feltet. "
            "Oppdater wenche-config-skillen og fixturet."
        )
        return 1

    print(f"Skjemavalidering OK: {len(FIXTURES)} fixtures kontrollert mot `wenche skjema`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
