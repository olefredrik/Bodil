---
name: bokforing
description: Bokfør et regnskapsår for et passivt holdingselskap. Leser bankeksport (CSV) og stamdata, kategoriserer hver transaksjon etter den låste modellen, og produserer <år>/regnskap.md med resultatregnskap, balanse og transaksjonslogg. Bruk når brukeren vil føre regnskapet for et år.
---

# Skill: bokforing

Fører ett regnskapsår for et passivt holdingselskap fra en bankeksport. Du produserer `<år>/regnskap.md`. Du sender ingenting.

## Input

- `selskap.yaml` (stamdata, åpningsbalanse, eierposter). Finnes bare `selskap.example.yaml`, be brukeren kopiere den til `selskap.yaml` først.
- `<år>/bankeksport.csv` med kolonnene `dato,beskrivelse,belop` (positivt = inn, negativt = ut). En ekstra kolonne `folio_id` (fra `folio_import.py --med-id`) er kjent: la den stå i fila og ignorer den. Ser eksporten ellers annerledes ut, spør hvilke kolonner som er dato/beskrivelse/beløp i stedet for å gjette.
- Forrige års `<år-1>/regnskap.md` hvis det finnes. Da brukes fjorårets utgående balanse som åpningsbalanse (overstyrer `aapningsbalanse` i `selskap.yaml`), og fjorårets tall fylles inn som sammenligningstall.

## Den låste modellen (gjelder hver transaksjon)

| Transaksjon | Konto |
|---|---|
| Penger inn fra eier | Lån fra aksjonær (øker gjeld) |
| Utbytte mottatt fra datterselskap | Utbytte fra datterselskap (finansinntekt) |
| Penger ut til eier, opp til utestående avsatt utbytte | Reduserer avsatt utbytte (gjeld). Utbetalingen gjør opp en forpliktelse og rører ikke egenkapitalen |
| Penger ut til eier utover utestående avsatt utbytte | **Flagg og spør.** Se «Utbetaling uten avsetning» under |
| Alle andre utbetalinger | Andre driftskostnader |
| Kjøp/salg av eierpost | Andre aksjer (finansielt anleggsmiddel), kostpris fra `selskap.yaml` |
| Betaling av skatt til Skatteetaten | Reduserer betalbar skatt (gjeld), er ikke en kostnad |

**Flagg og spør, ikke gjett**, ved: en transaksjon som ikke entydig passer en rad over, uvanlig store beløp, eller innbetalinger du ikke kan knytte til verken eier eller datterselskap. Bruk beskrivelsen i CSV-en til å avgjøre, men vær eksplisitt om hva du antok.

Utbytte er den ene posten som **ikke** stammer fra bankeksporten. Det avsettes som gjeld i det året det gjelder, og utbetalingen året etter gjør bare opp gjelden. Se «Utbytte» under.

### Utbetaling uten avsetning

Går det penger til eier uten at det står en avsetning fra i fjor å dekke dem med, skal du **stoppe og spørre**, ikke føre det som utbytte. Det er tre mulige svar, og bare brukeren vet hvilket som gjelder:

1. **Utbytte vedtatt i løpet av året** på grunnlag av sist godkjente årsregnskap (aksjeloven § 8-2 andre ledd). Da føres beløpet som `utbytte_utbetalt` og reduserer egenkapitalen i utbetalingsåret. Krev at brukeren bekrefter at det finnes et vedtak datert senest på betalingsdagen. **Bodil lager ikke det bilaget:** protokollen for dette året skrives våren etter og kan ikke tilbakedatere et vedtak. Mangler bilaget, si det rett ut i stedet for å produsere et.
2. **Lån til aksjonær.** Da er det en fordring, ikke en utdeling. Utenfor den låste modellen: flagg og be brukeren avklare med regnskapsfører.
3. **Tilbakebetaling av innbetalt kapital.** Også utenfor modellen. Flagg.

Dette er den vanligste situasjonen det året et selskap går over fra utbetalingsmodellen (Bodil ≤ 0.6.0) til avsetningsmodellen, siden det ikke finnes noen inngående avsetning å dekke utbetalingen med.

## Beregning

1. Klassifiser hver rad og før den i en **transaksjonslogg**.
2. Summer:
   - `andre_driftskostnader` = sum av alle «andre utbetalinger»
   - `utbytte_fra_datterselskap` = sum mottatt utbytte fra datterselskap
   - `utbytte_utbetalt` = sum utbetalt til eier. Dette tallet er **bare** en kontantstrøm og en post i aksjonærregisteroppgaven; det reduserer ikke egenkapitalen med mindre steget over konkluderte med utbytte vedtatt i året
   - endring i `laan_fra_aksjonaer` = sum innskudd fra eier
3. **Skattekostnad.** Et år uten utbytte gir 0, men et år med mottatt utbytte har normalt en liten reell skattekostnad, og regnskapsloven § 6-1 krever den som egen linje før årsresultatet. Regn i denne rekkefølgen:
   - `skattepliktig_utbytte` = 0 hvis eierandelen er 90 % eller mer, ellers 3 % av mottatt utbytte rundet opp til nærmeste krone (fritaksmetoden, sktl. § 2-38 sjette ledd). Eierandelen står under `eierposter` i `selskap.yaml`. Har selskapet flere eierposter med ulik eierandel, flagg det og spør hvilken posten utbyttet kom fra i stedet for å velge selv.
   - `skattepliktig_inntekt` = `skattepliktig_utbytte − andre_driftskostnader`
   - Er `skattepliktig_inntekt` positiv, trekk fra fremført underskudd. Tallet står under «Skattemessig» i `<år-1>/regnskap.md`. Finnes ikke fjorårets fil (år 1, eller år ført utenfor Bodil), **spør brukeren** om underskudd til fremføring fra fjorårets RF-1028 i stedet for å anta 0.
   - `skattekostnad` = 22 % av det som står igjen, rundet opp. Er `skattepliktig_inntekt` 0 eller negativ etter fradrag, er skattekostnaden 0.
   - `underskudd_til_fremfoering` for neste år: er `skattepliktig_inntekt` negativ, øk fjorårets fremførte underskudd med hele det negative beløpet. Er den positiv, reduser fjorårets med det som faktisk ble brukt som fradrag.
4. **Årsresultat** = `utbytte_fra_datterselskap − andre_driftskostnader − skattekostnad`
5. **Utbytte for året.** Dette er en beslutning, ikke en transaksjon, så den kommer ikke fra bankeksporten. Spør brukeren om styret foreslår utbytte for dette regnskapsåret. Blir svaret ja:
   - `avsatt_utbytte_i_aar` = beløpet. Det avsettes som kortsiktig gjeld per 31.12 og reduserer egenkapitalen i **dette** året, ikke i året det utbetales (rskl. § 6-2, aksjeloven § 8-2 første ledd).
   - **Krev dekning.** `overkursfond + annen_egenkapital` etter avsetningen må være ≥ 0 (aksjeloven § 8-1). En avsetning er en utdeling og kan gjøre fri egenkapital negativ helt alene. Er den negativ, stopp og be brukeren redusere beløpet.
   - Generalforsamlingen vedtar avsetningen når den godkjenner årsregnskapet, altså i `protokoll`-skillen. Bodil foregriper ikke vedtaket, den fører styrets forslag.
6. **Balanse per 31.12:**
   - `bankinnskudd` = åpningssaldo + sum alle transaksjoner (skal stemme med faktisk saldo 31.12, sjekk mot bankutskrift)
   - `andre_aksjer` = sum kostpris for eierposter i `selskap.yaml`
   - `aksjekapital` = fra `selskap.yaml`
   - `annen_egenkapital` = inngående annen egenkapital + årsresultat − `avsatt_utbytte_i_aar` − eventuelt utbytte vedtatt og utbetalt i året (steget «Utbetaling uten avsetning»). Merk at et utbytte utbetalt i år som gjør opp fjorårets avsetning **ikke** står her: det traff egenkapitalen i fjor.
   - `avsatt_utbytte` = inngående avsatt utbytte − utbetalt i år mot den avsetningen + `avsatt_utbytte_i_aar`
   - `laan_fra_aksjonaer` = inngående lån + årets innskudd fra eier
   - `betalbar_skatt` = inngående betalbar skatt − skatt betalt i år + årets `skattekostnad`. Skatten fastsettes og betales året etter, så årets skattekostnad står normalt ubetalt i balansen per 31.12. Dette er motposten til skattekostnaden: uten den går ikke balansen opp, og Wenche varsler om en skattekostnad uten motpost.
7. **Kontroller at balansen går opp:** sum eiendeler = sum egenkapital og gjeld. Hvis ikke, finn årsaken (oftest en feilklassifisert transaksjon eller feil åpningssaldo) før du går videre.
8. **Utbytte uten dekning:** hvis `overkursfond + annen_egenkapital < 0` etter at avsetningen og et eventuelt utbytte vedtatt i året er trukket fra, flagg det tydelig: utbytte kan bare deles ut av fri egenkapital (aksjeloven § 8-1). Dette gjelder avsetningen like fullt som en utbetaling, siden begge er utdelinger etter § 8-1.

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
| Avsatt utbytte | <x> | ... |
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

## Utbytte
| Post | <år> |
|---|--:|
| Utestående avsatt utbytte 01.01 | <x> |
| Utbetalt i året mot den avsetningen | <x> |
| Utbytte vedtatt og utbetalt i året (uten forutgående avsetning) | <x> |
| Avsatt for året (styrets forslag, vedtas i protokollen) | <x> |
| **Utestående avsatt utbytte 31.12** | <x> |

Denne seksjonen er input til neste års bokføring, til `protokoll` og til `avsatt_utbytte` i `wenche-config`. De to midterste linjene er ulike ting: den første gjør opp en gjeldspost og rører ikke egenkapitalen, den andre reduserer egenkapitalen i år. Summen av dem er `utbytte_utbetalt` og går i aksjonærregisteroppgaven for dette året.

## Transaksjonslogg
| Dato | Beskrivelse | Beløp | Klassifisert som |
|---|---|--:|---|
| ... | ... | ... | ... |

## Merknader
- Balansekontroll: sum eiendeler = sum EK og gjeld (✓/avvik)
- Eventuelle flagg (utbytte uten dekning, utbetaling til eier uten avsetning, uklare transaksjoner, store poster)
```

Feltnavnene i tabellene er bevisst de samme som Wenche bruker, slik at `wenche-config`-skillen kan mappe dem nær mekanisk.

## Neste steg

Når `regnskap.md` er ferdig og balansen går opp: kjør **protokoll**-skillen, og deretter **wenche-config**.
