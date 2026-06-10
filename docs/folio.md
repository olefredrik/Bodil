# Folio-integrasjon

Bruker selskapet [Folio](https://folio.no) som bank, kan Bodil hente årets transaksjoner rett fra Folio i stedet for at du laster ned CSV-en manuelt. Det er den eneste forskjellen: importøren skriver `<år>/bankeksport.csv`, og resten av [årshjulet](bruk.md) er helt likt.

Integrasjonen er **valgfri**. Bruker du en annen bank, eller vil laste ned CSV-en selv, hopper du rett til `/bokforing`.

!!! info "Kun lesing"
    Importøren gjør kun `GET`-kall og rører aldri `/payments` eller noe som flytter penger. Den skriver bare til `<år>/bankeksport.csv`, som allerede er gitignored, så en kjøring kan ikke skitne til committet historikk.

## Forutsetninger

1. **Lag en API-nøkkel hos Folio.** Gå til [app.folio.no/til/api-tilgang](https://app.folio.no/til/api-tilgang) mens du er innlogget. Dette er en dyplenke som ofte ikke ligger i den vanlige bankmenyen, gå rett til URL-en (krever trolig admin-/eierrolle). Velg **Lesetilgang** (det smaleste som dekker behovet), gi nøkkelen et navn, og kopier verdien med en gang, den vises gjerne bare én gang.
2. **Legg nøkkelen i en `.env`-fil.** Opprett `.env` i repo-roten hvis den ikke finnes fra før, og legg til linjen:
   ```
   FOLIO_API_NOKKEL=din-nøkkel
   ```
   Uten anførselstegn eller mellomrom rundt `=`. `.env` er gitignored, så nøkkelen havner aldri i git.
3. **Python 3** (skriptet bruker kun standardbiblioteket, ingen `pip install`).

## Slik kjører du

```bash
# Trygg førstegangstest: skriv til skjerm, ikke fil
python3 scripts/folio_import.py <år> --vis

# Når output ser riktig ut: skriv <år>/bankeksport.csv
python3 scripts/folio_import.py <år>

# Har selskapet flere Folio-kontoer, velg én:
python3 scripts/folio_import.py <år> --konto <accountNumber>
```

Du kan også be Claude om det med `/folio-import` eller vanlige ord («hent Folio-transaksjonene for 2026»).

## Kontroll før du går videre

- **Krysskontroll saldo:** skriptet henter inngående saldo 1.1 og utgående saldo 31.12 fra Folio og bekrefter at inngående + netto endring stemmer. Står det `OK`, henger tallene sammen. Et avvik betyr at en transaksjon mangler eller har uventet beløp.
- **Se over beskrivelsene:** `/bokforing` klassifiserer ut fra teksten i hver transaksjon. Er en tekst tom eller kryptisk, rett den i CSV-en før du fører.
- **Fortegn:** Folio oppgir beløp fortegnsatt fra kontoens perspektiv (negativ = ut, positiv = inn), og importøren bruker det direkte.

Når `<år>/bankeksport.csv` ser riktig ut, kjører du `/bokforing` som vanlig.

!!! note "Hva integrasjonen ikke gjør (ennå)"
    Importøren gjengir transaksjonene trofast; den klassifiserer dem ikke. En senere versjon kan berike radene med Folios `ledgerCategory` (NS4102-konto og SAF-T mva-kode) for en rikere bokføring.
