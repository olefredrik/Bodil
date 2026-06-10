#!/usr/bin/env python3
"""Folio-import: henter et regnskapsårs banktransaksjoner fra Folio og skriver
dem som `<år>/bankeksport.csv` med nøyaktig kolonnene `dato,beskrivelse,belop`.

Dette er en valgfri importør som kun leser. Den erstatter kun det manuelle steget
«last ned CSV fra banken». Alt nedstrøms (bokforing -> regnskap.md ->
wenche-config -> config.yaml) er uendret og vet ikke at filen kom fra Folio.

Designprinsipper (jf. CLAUDE.md og avtalt design):
  * Kun stdlib (urllib). Ingen ny avhengighet.
  * Kun GET-kall. Aldri /payments eller noe som flytter penger.
  * API-nøkkel leses fra .env (FOLIO_API_NOKKEL), aldri fra kommandolinjen.
  * Skriver kun til `<år>/bankeksport.csv`, som allerede er gitignored, så en
    kjøring kan aldri skitne til committet historikk.

Skrevet mot Folios OpenAPI v2 (api.folio.no/v2/api.yml), justert mot ekte data.
Viktige trekk ved API-et som styrer logikken under:
  * `transactionAmount.amount` er en fortegnsatt desimalstreng i kroner sett fra
    kontoen vi spør på (kontoscopet endepunkt): negativ = ut, positiv = inn.
    (OpenAPI-skjemaet antyder kun positive tall, men ekte svar har fortegn, så vi
    bruker beløpet direkte og utleder ikke retning fra debtor/creditor.)
  * Transaksjonslisten ligger nestet i `transactions.booked`.
  * Saldo-endepunktet gir `incomingBalance` (start på dagen) og `outgoingBalance`
    (slutt på dagen), begge desimalstrenger. Mangler for datoer der kontoen ikke
    var åpen, eller som ikke har passert ennå.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASIS_URL = "https://api.folio.no/v2"
NOKKEL_NAVN = "FOLIO_API_NOKKEL"


# --- HTTP (kun GET) ----------------------------------------------------------

def les_api_nokkel(env_sti: Path) -> str:
    """Leser FOLIO_API_NOKKEL fra miljøet eller fra .env. Aldri fra argv."""
    nokkel = os.environ.get(NOKKEL_NAVN)
    if nokkel:
        return nokkel.strip()

    if env_sti.exists():
        for linje in env_sti.read_text(encoding="utf-8").splitlines():
            linje = linje.strip()
            if not linje or linje.startswith("#") or "=" not in linje:
                continue
            navn, _, verdi = linje.partition("=")
            if navn.strip() == NOKKEL_NAVN:
                return verdi.strip().strip('"').strip("'")

    sys.exit(
        f"Fant ingen {NOKKEL_NAVN}. Slik fikser du det:\n"
        f"  1. Lag en API-nøkkel med Lesetilgang på "
        f"https://app.folio.no/til/api-tilgang\n"
        f"  2. Opprett en .env-fil i repo-roten (hvis den ikke finnes) med linjen:\n"
        f"       {NOKKEL_NAVN}=din-nøkkel\n"
        f"     (uten anførselstegn eller mellomrom rundt =, .env er gitignored)"
    )


def hent(path: str, nokkel: str, params: dict | None = None) -> object:
    """Ett GET-kall mot Folio. Reiser ved alt annet enn 2xx.

    Sikkerhetsvakt: nekter å treffe noe som ser ut som en pengeflytt-ressurs.
    Skriptet skal kun lese.
    """
    if re.search(r"payment|transfer", path, re.IGNORECASE):
        raise ValueError(f"Nektet: {path} ser ut som en pengeflytt-ressurs. "
                         "Folio-import skal kun lese.")

    url = f"{BASIS_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {nokkel}")
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as svar:
            return json.loads(svar.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        kropp = e.read().decode("utf-8", "replace")[:500]
        sys.exit(f"Folio svarte {e.code} på GET {path}: {kropp}")
    except urllib.error.URLError as e:
        sys.exit(f"Fikk ikke kontakt med Folio ({BASIS_URL}): {e.reason}")


# --- Hjelpere ----------------------------------------------------------------

def kun_siffer(s: object) -> str:
    """Normaliserer et kontonummer til kun siffer, for sammenligning."""
    return re.sub(r"\D", "", str(s or ""))


def samme_konto(a: str, b: str) -> bool:
    """Sant hvis to normaliserte kontonummer er samme konto. Tåler at BBAN og
    IBAN/utvidet form ikke er tegn-for-tegn like ved å tillate suffiks-match."""
    if not a or not b:
        return False
    return a == b or a.endswith(b) or b.endswith(a)


def til_belop(transaction_amount: dict) -> float:
    """`transactionAmount.amount` er en fortegnsatt desimalstreng i kroner."""
    if not isinstance(transaction_amount, dict):
        return 0.0
    return float(str(transaction_amount.get("amount", "0")).replace(" ", ""))


def format_belop(b: float) -> str:
    """Heltall uten desimaler (som eksempel-CSV), ellers to desimaler."""
    if abs(b - round(b)) < 0.005:
        return str(int(round(b)))
    return f"{b:.2f}"


# --- Forretningslogikk -------------------------------------------------------

def velg_konto(kontoer: list, valgt: str | None) -> dict:
    """Velger kontoen vi skal eksportere. Flagger og stopper hvis flertydig."""
    if not kontoer:
        sys.exit("Folio returnerte ingen kontoer for denne nøkkelen.")
    if valgt:
        n = kun_siffer(valgt)
        for k in kontoer:
            if valgt == k.get("name") or samme_konto(kun_siffer(k.get("accountNumber")), n):
                return k
        sys.exit(f"Fant ingen konto som matcher --konto {valgt!r}.")
    if len(kontoer) == 1:
        return kontoer[0]
    linjer = [f"  {k.get('accountNumber')}  {k.get('name','')} ({k.get('type','')})"
              for k in kontoer]
    sys.exit("Flere kontoer funnet. Velg én med --konto <accountNumber>:\n"
             + "\n".join(linjer))


def til_rad(tx: dict) -> dict:
    """Mapper én Folio-transaksjon til {dato, beskrivelse, belop}.

    `transactionAmount.amount` er allerede fortegnsatt sett fra kontoen vi spør
    på (kontoscopet endepunkt): negativ = ut, positiv = inn. Vi bruker det
    direkte. Mangler `description`, fall tilbake på motpartens navn.
    """
    belop = til_belop(tx.get("transactionAmount") or {})
    motpart = ((tx.get("creditor") or {}).get("name")
               or (tx.get("debtor") or {}).get("name") or "")
    beskrivelse = (tx.get("description") or "").strip() or motpart
    return {
        "dato": str(tx.get("bookingDate", ""))[:10],
        "beskrivelse": " ".join(str(beskrivelse).split()),
        "belop": belop,
    }


def hent_saldo(konto_nr: str, dato: str, nokkel: str, felt: str) -> float | None:
    """`incomingBalance` (start på dagen) eller `outgoingBalance` (slutt)."""
    try:
        svar = hent(f"/accounts/{konto_nr}/balance/{dato}", nokkel)
    except SystemExit:
        return None  # saldo er en hyggelig kontroll, ikke kritisk
    if isinstance(svar, dict) and svar.get(felt) is not None:
        return float(str(svar[felt]).replace(" ", ""))
    return None


# --- Hovedflyt ---------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(
        description="Hent et regnskapsårs Folio-transaksjoner til "
                    "<år>/bankeksport.csv (kun lesing).")
    p.add_argument("aar", type=int, help="Regnskapsåret, f.eks. 2025")
    p.add_argument("--konto", help="accountNumber eller navn hvis du har flere kontoer")
    p.add_argument("--env", default=".env", help="Sti til .env (standard: .env)")
    p.add_argument("--vis", action="store_true",
                   help="Skriv til stdout i stedet for fil (trygg førstegangstest)")
    args = p.parse_args()

    aar = args.aar
    fra, til = f"{aar}-01-01", f"{aar}-12-31"
    nokkel = les_api_nokkel(Path(args.env))

    # 1) Finn kontoen.
    kontoer = (hent("/accounts", nokkel) or {}).get("accounts", [])
    konto = velg_konto(kontoer, args.konto)
    konto_nr = konto.get("accountNumber")
    print(f"Konto: {konto_nr}  {konto.get('name','')} ({konto.get('type','')})",
          file=sys.stderr)

    # 2) Hent årets transaksjoner (kontoscopet endepunkt: kjent retningskontekst).
    svar = hent(f"/accounts/{konto_nr}/transactions", nokkel,
                {"startDate": fra, "endDate": til})
    booked = ((svar or {}).get("transactions") or {}).get("booked", [])

    if args.vis and booked:
        # Dump den første rå-transaksjonen så feltformene kan bekreftes mot
        # ekte data (kontonummer-format, debtor/creditor, beløp).
        print("Rå første transaksjon (til feltkontroll):", file=sys.stderr)
        print(json.dumps(booked[0], indent=2, ensure_ascii=False), file=sys.stderr)

    rader = [til_rad(tx) for tx in booked]
    rader = [r for r in rader if r["dato"][:4] == str(aar)]
    rader.sort(key=lambda r: r["dato"])

    if not rader:
        print(f"ADVARSEL: ingen transaksjoner funnet for {aar}.", file=sys.stderr)

    sum_inn = sum(r["belop"] for r in rader if r["belop"] > 0)
    sum_ut = sum(r["belop"] for r in rader if r["belop"] < 0)
    netto = sum_inn + sum_ut

    # 3) Krysskontroll: inngående saldo 1.1 + netto skal bli utgående saldo 31.12.
    inngaaende = hent_saldo(konto_nr, fra, nokkel, "incomingBalance")
    utgaaende = hent_saldo(konto_nr, til, nokkel, "outgoingBalance")

    # 4) Skriv ut eller lagre.
    def skriv(writer):
        writer.writerow(["dato", "beskrivelse", "belop"])
        for r in rader:
            writer.writerow([r["dato"], r["beskrivelse"], format_belop(r["belop"])])

    if args.vis:
        skriv(csv.writer(sys.stdout))
    else:
        ut = Path(str(aar)) / "bankeksport.csv"
        ut.parent.mkdir(parents=True, exist_ok=True)
        with ut.open("w", encoding="utf-8", newline="") as f:
            skriv(csv.writer(f))
        print(f"Skrev {len(rader)} transaksjoner til {ut}", file=sys.stderr)

    # Oppsummering til kontroll (stderr, så --vis kan pipes rent).
    print(f"\nOppsummering {aar}:", file=sys.stderr)
    print(f"  Transaksjoner : {len(rader)}", file=sys.stderr)
    print(f"  Inn           : {format_belop(sum_inn)}", file=sys.stderr)
    print(f"  Ut            : {format_belop(sum_ut)}", file=sys.stderr)
    print(f"  Netto endring : {format_belop(netto)}", file=sys.stderr)

    if inngaaende is not None and utgaaende is not None:
        forventet = inngaaende + netto
        avvik = forventet - utgaaende
        status = "OK" if abs(avvik) < 0.005 else f"AVVIK {format_belop(avvik)}"
        print(f"  Saldo 1.1     : {format_belop(inngaaende)}", file=sys.stderr)
        print(f"  Saldo 31.12   : {format_belop(utgaaende)} "
              f"(inngående + netto = {format_belop(forventet)}) -> {status}",
              file=sys.stderr)
        if abs(avvik) >= 0.005:
            print("  -> Avvik betyr at en eller flere transaksjoner mangler "
                  "eller har uventet beløp.", file=sys.stderr)
    else:
        print("  Saldo: ikke tilgjengelig (kontoen var ikke åpen på datoen, eller "
              "året er ikke ferdig). Kontroller mot bankutskrift manuelt.",
              file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
