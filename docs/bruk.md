# Bruk

Det er ingen app å installere og starte, og ingen nettside. Du «kjører» Bodil ved å snakke med Claude Code: skillene ligger i `.claude/skills/` og oppdages automatisk når du åpner repoet.

## Samtalebasert eller kommandobasert?

Du starter en skill på én av to måter, og kan blande dem fritt:

- **Kommandobasert (eksplisitt):** skriv en skråstrek-kommando i chatten. Når du taster `/` dukker en liste opp, og du skal se `/bokforing`, `/protokoll`, `/wenche-config` og (valgfritt) `/folio-import` der.
- **Samtalebasert (la Claude velge):** be om det med vanlige ord, f.eks. «før regnskapet for 2026», så starter Claude riktig skill selv.

Begge gjør det samme. Skråstrek gir deg eksplisitt kontroll; vanlige ord er ofte nok når du vet hva du vil ha gjort.

!!! note "Én skill av gangen"
    Du kjører én skill, ser på resultatet, og går videre til neste. Claude sender **ingenting** selv. Innsendingen gjør du i Wenche helt til slutt. Og Claude stopper og spør hvis noe ikke passer den [låste modellen](modellen.md), i stedet for å gjette.

## Årshjul

For hvert regnskapsår kjører du skillene slik. Bytt ut `<år>` med året, f.eks. legg bankeksporten i `2026/bankeksport.csv`:

1. **`/bokforing`** → lager `<år>/regnskap.md` (resultatregnskap + balanse + transaksjonslogg).
2. **Avgjør utbytte** sammen med Claude (kun hvis det er fri egenkapital å dele ut).
3. **`/protokoll`** → lager `<år>/protokoll.md` (godkjenner regnskapet og vedtar utbytte, fungerer også som utbytte-bilag).
4. **`/wenche-config`** → lager `<år>/config.yaml` + en sjekkliste, og kjører `wenche valider-aarsregnskap` for deg.
5. **Overfør til Wenche og send inn** (se under).

Bruker selskapet Folio som bank, kan du la [Folio-integrasjonen](folio.md) hente bankeksporten automatisk før steg 1. Ellers laster du ned CSV-en fra banken selv.

!!! info "Frister"
    Aksjonærregisteroppgave 31. januar · skattemelding 31. mai · årsregnskap 31. juli. Merk: det manuelle skjemaet for aksjonærregisteroppgaven fases ut, så fra januar 2027 må også den gå via Wenche.

## Overfør til Wenche og send inn

Start Wenche fra årsmappen, slik at den finner riktig `config.yaml`:

```bash
cd 2026
wenche
```

Gå gjennom fanene i web-grensesnittet, fyll inn noter i **Dokumenter**-fanen, kontroller tallene, og send inn. Detaljene står i [Bodil og Wenche](bodil-og-wenche.md).
