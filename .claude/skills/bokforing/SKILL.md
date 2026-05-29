---
name: bokforing
description: Bokfør et regnskapsår for et passivt holdingselskap. Leser bankeksport (CSV) og stamdata, kategoriserer hver transaksjon etter den låste modellen, og produserer <år>/regnskap.md med resultatregnskap, balanse og transaksjonslogg. Bruk når brukeren vil føre regnskapet for et år.
---

# Skill: bokforing

Fører ett regnskapsår for et passivt holdingselskap fra en bankeksport. Du produserer `<år>/regnskap.md`. Du sender ingenting.

## Input

- `selskap.yaml` (stamdata, åpningsbalanse, eierposter). Finnes bare `selskap.example.yaml`, be brukeren kopiere den til `selskap.yaml` først.
- `<år>/bankeksport.csv` med kolonnene `dato,beskrivelse,belop` (positivt = inn, negativt = ut). Ser eksporten annerledes ut, spør hvilke kolonner som er dato/beskrivelse/beløp i stedet for å gjette.
- Forrige års `<år-1>/regnskap.md` hvis det finnes. Da brukes fjorårets utgående balanse som åpningsbalanse (overstyrer `aapningsbalanse` i `selskap.yaml`), og fjorårets tall fylles inn som sammenligningstall.

## Den låste modellen (gjelder hver transaksjon)

| Transaksjon | Konto |
|---|---|
| Penger inn fra eier | Lån fra aksjonær (øker gjeld) |
| Utbytte mottatt fra datterselskap | Utbytte fra datterselskap (finansinntekt) |
| Penger ut til eier | Utbytte (reduserer egenkapital, er ikke en kostnad) |
| Alle andre utbetalinger | Andre driftskostnader |
| Kjøp/salg av eierpost | Andre aksjer (finansielt anleggsmiddel), kostpris fra `selskap.yaml` |

**Flagg og spør, ikke gjett**, ved: en transaksjon som ikke entydig passer en rad over, uvanlig store beløp, eller innbetalinger du ikke kan knytte til verken eier eller datterselskap. Bruk beskrivelsen i CSV-en til å avgjøre, men vær eksplisitt om hva du antok.

## Beregning

1. Klassifiser hver rad og før den i en **transaksjonslogg**.
2. Summer:
   - `andre_driftskostnader` = sum av alle «andre utbetalinger»
   - `utbytte_fra_datterselskap` = sum mottatt utbytte fra datterselskap
   - `utbytte_utbetalt` = sum utbetalt til eier
   - endring i `laan_fra_aksjonaer` = sum innskudd fra eier
3. **Årsresultat** = `utbytte_fra_datterselskap − andre_driftskostnader` (ingen skatt for et holdingselskap uten skattbar inntekt; utbytte fra datterselskap er normalt skattefritt under fritaksmetoden).
4. **Balanse per 31.12:**
   - `bankinnskudd` = åpningssaldo + sum alle transaksjoner (skal stemme med faktisk saldo 31.12, sjekk mot bankutskrift)
   - `andre_aksjer` = sum kostpris for eierposter i `selskap.yaml`
   - `aksjekapital` = fra `selskap.yaml`
   - `annen_egenkapital` = inngående annen egenkapital + årsresultat − utbytte_utbetalt
   - `laan_fra_aksjonaer` = inngående lån + årets innskudd fra eier
5. **Kontroller at balansen går opp:** sum eiendeler = sum egenkapital og gjeld. Hvis ikke, finn årsaken (oftest en feilklassifisert transaksjon eller feil åpningssaldo) før du går videre.
6. **Utbytte uten dekning:** hvis `utbytte_utbetalt > 0` og `overkursfond + annen_egenkapital < 0` etter utdelingen, flagg det tydelig: utbytte kan bare deles ut av fri egenkapital (aksjeloven § 8-1). Be brukeren bekrefte om utbetalingen virkelig er utbytte, eller om den heller er lån til aksjonær eller tilbakebetaling av innbetalt kapital.

## Output: `<år>/regnskap.md`

Skriv en lesbar markdown-fil med disse seksjonene (ikke skriv fødselsnummer i denne fila, den versjoneres):

```markdown
# Regnskap <år>, <selskapsnavn>

## Resultatregnskap
| Post | <år> | <år-1> |
|---|--:|--:|
| Salgsinntekter | 0 | ... |
| Andre driftsinntekter | 0 | ... |
| Lønnskostnader | 0 | ... |
| Avskrivninger | 0 | ... |
| Andre driftskostnader | <x> | ... |
| Utbytte fra datterselskap | <x> | ... |
| Andre finansinntekter | 0 | ... |
| Rentekostnader | 0 | ... |
| Andre finanskostnader | 0 | ... |
| **Årsresultat** | <x> | ... |

## Balanse per 31.12
### Eiendeler
| Post | <år> | <år-1> |
|---|--:|--:|
| Aksjer i datterselskap | 0 | ... |
| Andre aksjer | <x> | ... |
| Langsiktige fordringer | 0 | ... |
| Kortsiktige fordringer | 0 | ... |
| Bankinnskudd | <x> | ... |
| **Sum eiendeler** | <x> | ... |

### Egenkapital og gjeld
| Post | <år> | <år-1> |
|---|--:|--:|
| Aksjekapital | <x> | ... |
| Overkursfond | 0 | ... |
| Annen egenkapital | <x> | ... |
| Lån fra aksjonær | <x> | ... |
| Andre langsiktige lån | 0 | ... |
| Leverandørgjeld | 0 | ... |
| Skyldige offentlige avgifter | 0 | ... |
| Annen kortsiktig gjeld | 0 | ... |
| **Sum egenkapital og gjeld** | <x> | ... |

## Transaksjonslogg
| Dato | Beskrivelse | Beløp | Klassifisert som |
|---|---|--:|---|
| ... | ... | ... | ... |

## Merknader
- Balansekontroll: sum eiendeler = sum EK og gjeld (✓/avvik)
- Eventuelle flagg (utbytte uten dekning, uklare transaksjoner, store poster)
```

Feltnavnene i tabellene er bevisst de samme som Wenche bruker, slik at `wenche-config`-skillen kan mappe dem nær mekanisk.

## Neste steg

Når `regnskap.md` er ferdig og balansen går opp: kjør **protokoll**-skillen, og deretter **wenche-config**.
