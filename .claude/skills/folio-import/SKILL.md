---
name: folio-import
description: Valgfri, lese-only importør som henter et regnskapsårs banktransaksjoner fra Folio (api.folio.no/v2) og skriver dem som <år>/bankeksport.csv med kolonnene dato,beskrivelse,belop. Erstatter kun det manuelle «last ned CSV fra banken»-steget før bokforing. Bruk når selskapets bank er Folio og brukeren vil slippe å laste ned CSV manuelt.
---

# Skill: folio-import

Henter ett regnskapsårs transaksjoner fra Folio og skriver dem som
`<år>/bankeksport.csv`. Dette er **det eneste** skillen gjør. Alt nedstrøms
(bokforing -> regnskap.md -> wenche-config -> config.yaml) er uendret og bryr
seg ikke om at filen kom fra Folio i stedet for en manuell nedlasting.

Skillen er **valgfri**. Bruker selskapet en annen bank, eller vil brukeren laste
ned CSV-en selv, hopper du rett til **bokforing** som før.

## Sikkerhet (les dette)

- **Lese-only.** Skriptet gjør kun GET-kall. Det rører aldri `/payments` eller
  noe som flytter penger. En innebygd vakt nekter å treffe ruter med «payment»
  eller «transfer» i stien.
- **Skriver kun til `<år>/bankeksport.csv`**, som allerede er gitignored. En
  kjøring kan ikke skitne til committet historikk.
- **API-nøkkelen leses fra `.env`** (`FOLIO_API_NOKKEL`), aldri fra
  kommandolinjen og aldri inn i git. `.env` er gitignored.

## Forutsetninger

- Selskapets bank er Folio, og brukeren har laget en API-nøkkel på
  `https://app.folio.no/til/api-tilgang`. Dette er en dyplenke som ofte ikke
  ligger i den vanlige bankmenyen, gå rett til URL-en mens du er innlogget.
  Krever trolig admin-/eierrolle på bedriftskontoen.
- Nøkkelen ligger i `.env` i repo-roten:
  ```
  FOLIO_API_NOKKEL=...
  ```
  Mangler `.env` eller nøkkelen, be brukeren legge den inn først.
- Python 3 (skriptet bruker kun stdlib, ingen `pip install`).

## Slik kjører du

```bash
# Trygg førstegangstest: skriv til skjerm, ikke fil
python scripts/folio_import.py <år> --vis

# Når output ser riktig ut: skriv <år>/bankeksport.csv
python scripts/folio_import.py <år>

# Har selskapet flere Folio-kontoer, velg én:
python scripts/folio_import.py <år> --konto <konto-id>
```

Skriptet:
1. `GET /accounts` og velger kontoen (stopper og ber om `--konto` hvis flere).
2. `GET /accounts/{accountNumber}/transactions?startDate=&endDate=` for hele
   året, og mapper hver transaksjon til `dato,beskrivelse,belop`.
3. `GET /accounts/{accountNumber}/balance/<år>-01-01` og `.../<år>-12-31` for å
   krysse inngående + netto mot utgående saldo.
4. Skriver `<år>/bankeksport.csv` og en oppsummering (antall, inn, ut, netto,
   saldokontroll) til kontroll.

**Fortegn:** Folios `transactionAmount.amount` er allerede fortegnsatt sett fra
kontoen vi spør på (negativ = ut, positiv = inn), så vi bruker beløpet direkte.

## Kontroll før du går videre

- **Krysskontroll saldo:** inngående saldo 1.1 + netto endring skal bli utgående
  saldo 31.12. Skriptet regner dette ut og skriver `OK` eller `AVVIK`. Et avvik
  betyr at en transaksjon fikk feil fortegn eller mangler.
- **Se over beskrivelsene:** bokforing klassifiserer ut fra teksten (innskudd fra
  eier, utbytte fra datterselskap, utbytte til eier, driftskostnad). Er en tekst
  tom eller kryptisk, blir klassifiseringen et gjettverk, rett den i CSV-en.
- **Flagg det uventede.** Passer noe ikke den låste modellen, stopp og spør,
  ikke gjett (samme regel som bokforing).

## Om API-formen

Skrevet mot Folios OpenAPI v2 (`https://api.folio.no/v2/api.yml`). Endrer Folio
kontrakten, fanges det av saldokontrollen og de rå-dumpede feltene under `--vis`.

(v2 senere, ikke nå: berike radene med Folios `ledgerCategory` via
`GET /categories/{id}`, som gir NS4102-konto og SAF-T mva-kode for en rikere
bokføring.)

## Neste steg

Når `<år>/bankeksport.csv` ser riktig ut og saldoen krysser: kjør **bokforing**
som vanlig.
