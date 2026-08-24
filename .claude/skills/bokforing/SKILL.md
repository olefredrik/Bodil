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
| Betaling av skatt til Skatteetaten | Reduserer betalbar skatt (gjeld), er ikke en kostnad |

**Flagg og spør, ikke gjett**, ved: en transaksjon som ikke entydig passer en rad over, uvanlig store beløp, eller innbetalinger du ikke kan knytte til verken eier eller datterselskap. Bruk beskrivelsen i CSV-en til å avgjøre, men vær eksplisitt om hva du antok.

## Beregning

1. Klassifiser hver rad og før den i en **transaksjonslogg**.
2. Summer:
   - `andre_driftskostnader` = sum av alle «andre utbetalinger»
   - `utbytte_fra_datterselskap` = sum mottatt utbytte fra datterselskap
   - `utbytte_utbetalt` = sum utbetalt til eier
   - endring i `laan_fra_aksjonaer` = sum innskudd fra eier
3. **Skattekostnad.** Et år uten utbytte gir 0, men et år med mottatt utbytte har normalt en liten reell skattekostnad, og regnskapsloven § 6-1 krever den som egen linje før årsresultatet. Regn i denne rekkefølgen:
   - `skattepliktig_utbytte` = 0 hvis eierandelen er 90 % eller mer, ellers 3 % av mottatt utbytte rundet opp til nærmeste krone (fritaksmetoden, sktl. § 2-38 sjette ledd). Eierandelen står under `eierposter` i `selskap.yaml`. Har selskapet flere eierposter med ulik eierandel, flagg det og spør hvilken posten utbyttet kom fra i stedet for å velge selv.
   - `skattepliktig_inntekt` = `skattepliktig_utbytte − andre_driftskostnader`
   - Er `skattepliktig_inntekt` positiv, trekk fra fremført underskudd. Tallet står under «Skattemessig» i `<år-1>/regnskap.md`. Finnes ikke fjorårets fil (år 1, eller år ført utenfor Bodil), **spør brukeren** om underskudd til fremføring fra fjorårets RF-1028 i stedet for å anta 0.
   - `skattekostnad` = 22 % av det som står igjen, rundet opp. Er `skattepliktig_inntekt` 0 eller negativ etter fradrag, er skattekostnaden 0.
   - `underskudd_til_fremfoering` for neste år: er `skattepliktig_inntekt` negativ, øk fjorårets fremførte underskudd med hele det negative beløpet. Er den positiv, reduser fjorårets med det som faktisk ble brukt som fradrag.
4. **Årsresultat** = `utbytte_fra_datterselskap − andre_driftskostnader − skattekostnad`
5. **Balanse per 31.12:**
   - `bankinnskudd` = åpningssaldo + sum alle transaksjoner (skal stemme med faktisk saldo 31.12, sjekk mot bankutskrift)
   - `andre_aksjer` = sum kostpris for eierposter i `selskap.yaml`
   - `aksjekapital` = fra `selskap.yaml`
   - `annen_egenkapital` = inngående annen egenkapital + årsresultat − utbytte_utbetalt
   - `laan_fra_aksjonaer` = inngående lån + årets innskudd fra eier
   - `betalbar_skatt` = inngående betalbar skatt − skatt betalt i år + årets `skattekostnad`. Skatten fastsettes og betales året etter, så årets skattekostnad står normalt ubetalt i balansen per 31.12. Dette er motposten til skattekostnaden: uten den går ikke balansen opp, og Wenche varsler om en skattekostnad uten motpost.
6. **Kontroller at balansen går opp:** sum eiendeler = sum egenkapital og gjeld. Hvis ikke, finn årsaken (oftest en feilklassifisert transaksjon eller feil åpningssaldo) før du går videre.
7. **Utbytte uten dekning:** hvis `utbytte_utbetalt > 0` og `overkursfond + annen_egenkapital < 0` etter utdelingen, flagg det tydelig: utbytte kan bare deles ut av fri egenkapital (aksjeloven § 8-1). Be brukeren bekrefte om utbetalingen virkelig er utbytte, eller om den heller er lån til aksjonær eller tilbakebetaling av innbetalt kapital.

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
| Skattekostnad | <x> | ... |
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
| Betalbar skatt | <x> | ... |
| Skyldige offentlige avgifter | 0 | ... |
| Annen kortsiktig gjeld | 0 | ... |
| **Sum egenkapital og gjeld** | <x> | ... |

## Skattemessig
| Post | <år> |
|---|--:|
| Mottatt utbytte | <x> |
| Skattepliktig del av utbyttet (3 %-sjablon, 0 ved eierandel ≥ 90 %) | <x> |
| Skattepliktig inntekt før fradrag | <x> |
| Anvendt fremført underskudd | <x> |
| Skattepliktig inntekt | <x> |
| Beregnet skatt (22 %) | <x> |
| **Underskudd til fremføring neste år** | <x> |

Denne seksjonen er input til neste års bokføring og til `underskudd_til_fremfoering` i `wenche-config`. Uten den må tallet hentes manuelt fra RF-1028 hvert år.

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
