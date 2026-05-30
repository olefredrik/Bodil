#!/usr/bin/env python3
"""Feltnavn-lint: fanger Bodil-feltnavn som Wenche ikke lenger leser.

Validatoren (`wenche valider-aarsregnskap`) fanger alt som gjør en config
*ugyldig*, men ikke et stille feltnavn-bytte: døper Wenche om et felt og leser
det gamle navnet via `.get(navn, default)`, validerer configen fortsatt mens
Bodil-output egentlig er feil (verdien droppes, defaulten brukes).

Denne sjekken lukker det gapet. Den leser de gyldige feltnavnene rett fra
dataklassene i den *installerte* Wenche-pakken (sannhetskilden, ingen egen kopi
å vedlikeholde) og bekrefter at hver skalarnøkkel i golden-fixturet finnes der.

Bare skalarnøkler sjekkes: container-nøkler (dict/liste) som døpes om feiler
høylytt med KeyError og fanges allerede av validatoren. Det er bladfeltene som
leses med en default som kan forsvinne stille, og det er dem dette fanger.

Exit 0 = alle feltnavn kjent. Exit 1 = ukjent feltnavn (sannsynlig drift).
"""

from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

import yaml

try:
    from wenche import models
except ImportError:
    print("FEIL: pakken 'wenche' er ikke installert. Kjør `pip install wenche`.")
    sys.exit(2)

FIXTURE = Path(__file__).parent / "fixtures" / "config.golden.yaml"


def gyldige_feltnavn() -> set[str]:
    """Alle feltnavn på tvers av Wenches dataklasser."""
    navn: set[str] = set()
    for obj in vars(models).values():
        if dataclasses.is_dataclass(obj) and isinstance(obj, type):
            navn.update(f.name for f in dataclasses.fields(obj))
    return navn


def skalarnøkler(node: object) -> set[str]:
    """Nøkler i fixturet som peker på en skalar (ikke dict/liste)."""
    funnet: set[str] = set()
    if isinstance(node, dict):
        for nøkkel, verdi in node.items():
            if isinstance(verdi, (dict, list)):
                funnet |= skalarnøkler(verdi)
            else:
                funnet.add(nøkkel)
    elif isinstance(node, list):
        for element in node:
            funnet |= skalarnøkler(element)
    return funnet


def main() -> int:
    with FIXTURE.open(encoding="utf-8") as f:
        config = yaml.safe_load(f)

    gyldige = gyldige_feltnavn()
    brukte = skalarnøkler(config)
    ukjente = sorted(brukte - gyldige)

    if ukjente:
        print("Feltnavn-lint FEILET: golden-fixturet bruker felt Wenche ikke leser:")
        for navn in ukjente:
            print(f"  - {navn}")
        print(
            "\nWenche har sannsynligvis døpt om eller fjernet feltet. "
            "Oppdater wenche-config-skillen og golden-fixturet til det nye navnet."
        )
        return 1

    print(f"Feltnavn-lint OK: {len(brukte)} feltnavn, alle kjent av Wenche.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
