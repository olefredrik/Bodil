#!/usr/bin/env python3
"""Tester for Folio-importørens rene logikk (ingen nettverk).

Dekker det som faktisk kan gå galt i mappingen fra Folios JSON til CSV-raden
bokforing leser: fortegn, beløpsparsing, beskrivelse-fallback, kontovalg, og at
pengeflytt-vakten faktisk nekter. HTTP-laget testes ikke her (det krever et ekte
Folio-svar, og bekreftes manuelt ved kjøring mot kontoen).

Exit 0 = alle tester passerer. Exit 1 = minst én feilet.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import scripts.folio_import as f  # noqa: E402


def test_fortegn_brukes_direkte() -> None:
    """transactionAmount.amount er allerede fortegnsatt, ut = negativt."""
    ut = {"transactionAmount": {"amount": "-1000.00"}, "bookingDate": "2026-06-03",
          "description": "Til: OFL Holding AS", "debtor": {"accountNumber": "36063364430"},
          "creditor": {}}
    r = f.til_rad(ut)
    assert r["belop"] == -1000.0, r
    assert r["dato"] == "2026-06-03"
    assert r["beskrivelse"] == "Til: OFL Holding AS"


def test_inn_er_positivt() -> None:
    inn = {"transactionAmount": {"amount": "1626.50"}, "bookingDate": "2026-06-01",
           "description": "Fra: Ofl Holding AS"}
    assert f.til_rad(inn)["belop"] == 1626.5


def test_tom_beskrivelse_faller_til_motpart() -> None:
    """Mangler description, brukes motpartens navn så bokforing har noe å lese."""
    tx = {"transactionAmount": {"amount": "500.00"}, "bookingDate": "2026-02-01",
          "description": "", "creditor": {"name": "Datterselskap AS"}, "debtor": {}}
    assert f.til_rad(tx)["beskrivelse"] == "Datterselskap AS"


def test_beskrivelse_whitespace_normaliseres() -> None:
    tx = {"transactionAmount": {"amount": "1.00"}, "bookingDate": "2026-01-01",
          "description": "Fra:   Ofl   Holding"}
    assert f.til_rad(tx)["beskrivelse"] == "Fra: Ofl Holding"


def test_til_belop_taaler_mellomrom_og_manglende() -> None:
    assert f.til_belop({"amount": "1 626.50"}) == 1626.5
    assert f.til_belop({}) == 0.0
    assert f.til_belop(None) == 0.0


def test_format_belop() -> None:
    assert f.format_belop(-1000.0) == "-1000"   # heltall uten desimaler
    assert f.format_belop(1626.5) == "1626.50"  # desimaler beholdes
    assert f.format_belop(-0.92) == "-0.92"


def test_velg_konto_paa_nummer_og_navn() -> None:
    kontoer = [
        {"accountNumber": "36063364430", "name": "Driftskonto", "type": "Operational"},
        {"accountNumber": "36063364449", "name": "Kort", "type": "Card"},
    ]
    assert f.velg_konto(kontoer, "36063364430")["name"] == "Driftskonto"
    assert f.velg_konto(kontoer, "Kort")["accountNumber"] == "36063364449"
    assert f.velg_konto([kontoer[0]], None)["name"] == "Driftskonto"  # én konto, intet valg


def test_velg_konto_flertydig_stopper() -> None:
    kontoer = [{"accountNumber": "1", "name": "A"}, {"accountNumber": "2", "name": "B"}]
    try:
        f.velg_konto(kontoer, None)
    except SystemExit:
        return
    raise AssertionError("velg_konto skulle stoppet ved flere kontoer uten --konto")


def test_pengeflytt_vakt_nekter() -> None:
    """hent() skal nekte alt som ser ut som en pengeflytt-ressurs."""
    for path in ("/payments", "/accounts/1/payment", "/transfer"):
        try:
            f.hent(path, "dummy-nokkel")
        except ValueError:
            continue
        raise AssertionError(f"hent() skulle nektet {path}")


def main() -> int:
    tester = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    feilet = 0
    for t in tester:
        try:
            t()
            print(f"  OK   {t.__name__}")
        except AssertionError as e:
            feilet += 1
            print(f"  FEIL {t.__name__}: {e}")
    print(f"\n{len(tester) - feilet}/{len(tester)} tester passerte.")
    return 1 if feilet else 0


if __name__ == "__main__":
    sys.exit(main())
