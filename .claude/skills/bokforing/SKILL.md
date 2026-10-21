---
name: bokforing
description: Bokfør et regnskapsår for et passivt holdingselskap. Leser bankeksport (CSV) og stamdata, kategoriserer hver transaksjon etter den låste modellen, og produserer <år>/regnskap.md med resultatregnskap, balanse og transaksjonslogg. Bruk når brukeren vil føre regnskapet for et år.
---

# Skill: bokforing

Fører ett regnskapsår for et passivt holdingselskap fra en bankeksport. Du produserer `<år>/regnskap.md`. Du sender ingenting.

## Input

- `selskap.yaml` (stamdata, åpningsbalanse, eierposter). Finnes bare `selskap.example.yaml`, be brukeren kopiere den til `selskap.yaml` først.
- `<år>/bankeksport.csv` med kolonnene `dato,beskrivelse,belop` (positivt = inn, negativt = ut). En ekstra kolonne `folio_id` (fra `folio_import.py --med-id`) er kjent: la den stå i fila og ignorer den. Ser eksporten ellers annerledes ut, spør hvilke kolonner som er dato/beskrivelse/beløp i stedet for å gjette.
- Forrige års `<år-1>/regnskap.md` hvis det finnes. Da brukes fjorårets utgående balanse som åpningsbalanse (overstyrer `aapningsbalanse` i `selskap.yaml`), og fjorårets tall fylles inn som sammenligningstall. Står en eierpost på en annen balanselinje i fjorårets fil enn den skal stå på i år, se «Overgang» under «Datterselskap eller andre aksjer».
- **Første år i Bodil for et eldre selskap** (fjorårets `regnskap.md` finnes ikke, men selskapet ble stiftet før regnskapsåret): fjorårets balanse per 31.12 er `aapningsbalanse` i `selskap.yaml` sammen med eierpostene til kostpris. Fjorårets resultatregnskap finnes ikke i noen fil. **Spør brukeren** om det, linje for linje, fra fjorårets innsendte årsregnskap (det finnes også i Regnskapsregisteret hos Brønnøysundregistrene). Ikke sett 0 uten at brukeren bekrefter det. Skriv tallene i sammenligningskolonnen, så `wenche-config` kan hente dem.

## Den låste modellen (gjelder hver transaksjon)

| Transaksjon | Konto |
|---|---|
| Penger inn fra eier | Lån fra aksjonær (øker gjeld). Se «Innbetaling fra eier» under |
| Utbytte mottatt fra datterselskap | Utbytte fra datterselskap (finansinntekt) |
| Penger ut til eier, opp til utestående avsatt utbytte | Reduserer avsatt utbytte (gjeld). Utbetalingen gjør opp en forpliktelse og rører ikke egenkapitalen. Har selskapet også utestående lån fra aksjonær, **spør** om det er utbytte eller nedbetaling, se «Utbytte eller nedbetaling» under |
| Penger ut til eier, bekreftet som nedbetaling, opp til utestående lån fra aksjonær | Reduserer lån fra aksjonær (gjeld). Rører verken resultat eller egenkapital |
| Penger ut til eier utover utestående avsatt utbytte | **Flagg og spør.** Se «Utbetaling uten avsetning» under |
| Renteinntekt fra banken (kreditrenter) | Andre finansinntekter. Fullt skattepliktig, verken fritaksmetode eller sjablon |
| Renter belastet av banken på kontoen (debetrenter) | Rentekostnader |
| Renter på lån i banken, renter betalt til eier (f.eks. på aksjonærlån) eller til Skatteetaten (rentetillegg, forsinkelsesrenter) | **Flagg og spør.** Et lån i banken er utenfor den låste modellen, renter til eier forutsetter en låneavtale, og renter til Skatteetaten kan blandes med skattebetalingen og har egne fradragsregler |
| Alle andre utbetalinger | Andre driftskostnader |
| Kjøp av eierpost | Aksjer i datterselskap eller andre aksjer (finansielt anleggsmiddel) til kostpris. Se «Datterselskap eller andre aksjer» under |
| Salg av eierpost | Kostprisen ut av balansen, differansen mot salgssummen er gevinst eller tap ved realisasjon av aksjer. Se «Salg av eierpost» under |
| Betaling av skatt til Skatteetaten | Reduserer betalbar skatt (gjeld), er ikke en kostnad |

**Flagg og spør, ikke gjett**, ved: en transaksjon som ikke entydig passer en rad over, uvanlig store beløp, eller innbetalinger du ikke kan knytte til verken eier eller datterselskap. Bruk beskrivelsen i CSV-en til å avgjøre, men vær eksplisitt om hva du antok.

Utbytte er den ene posten som **ikke** stammer fra bankeksporten. Det avsettes som gjeld i det året det gjelder, og utbetalingen året etter gjør bare opp gjelden. Se «Utbytte» under.

### Innbetaling fra eier

Penger inn fra eier føres som lån fra aksjonær. Tyder beskrivelsen på en **kapitalforhøyelse** eller en **tilleggsinnbetaling** (for eksempel «kapitalforhøyelse», «aksjeinnskudd», «emisjon», «tilskudd»), skal du flagge og spørre i stedet. En kapitalforhøyelse krever vedtak i generalforsamlingen og registrering i Foretaksregisteret (aksjeloven kapittel 10) og endrer aksjekapitalen, ikke gjelden. Begge deler er utenfor den låste modellen: be brukeren avklare med regnskapsfører.

### Utbytte eller nedbetaling

Har selskapet både utestående avsatt utbytte og utestående lån fra aksjonær, kan en utbetaling til eier være begge deler. **Ikke la avsetningen dekke den først automatisk.** Spør brukeren, selv om beskrivelsen peker én vei, og si hva beskrivelsen tydet på. Utbytte er skattepliktig for eieren og går i aksjonærregisteroppgaven, mens en nedbetaling av lån ikke gjør det, så en feil gjetning her slår ut hos eieren og ikke bare i selskapets regnskap. En utbetaling kan også deles mellom de to; før da hver del etter sin rad.

### Utbetaling uten avsetning

Går det penger til eier uten at det står en avsetning fra i fjor å dekke dem med, skal du **stoppe og spørre**, ikke føre det som utbytte. Det er fire mulige svar, og bare brukeren vet hvilket som gjelder:

1. **Nedbetaling av lån fra aksjonær**, opp til utestående lån (inngående lån + årets innskudd − det som allerede er nedbetalt). Reduserer `laan_fra_aksjonaer` og rører ikke egenkapitalen. Er utbetalingen større enn utestående lån, er resten ikke en nedbetaling: spør om resten på nytt.
2. **Utbytte vedtatt i løpet av året** på grunnlag av sist godkjente årsregnskap (aksjeloven § 8-2 andre ledd). Da føres beløpet som `utbytte_utbetalt` og reduserer egenkapitalen i utbetalingsåret. Krev at brukeren bekrefter at det finnes et vedtak datert senest på betalingsdagen. **Bodil lager ikke det bilaget:** protokollen for dette året skrives våren etter og kan ikke tilbakedatere et vedtak. Mangler bilaget, si det rett ut i stedet for å produsere et. **Krev dekning i sist godkjente balanse:** utdelingsgrunnlaget er balansen i sist godkjente årsregnskap, ikke årets (aksjeloven § 8-1). Fri egenkapital (`overkursfond + annen_egenkapital`) i fjorårets balanse per 31.12, minus andre utdelinger som allerede er vedtatt i år på grunnlag av samme balanse, må dekke beløpet. Årets resultat teller ikke med. Dekker den ikke, **stopp**: utdelingen kan være ulovlig (aksjeloven § 3-7), med mindre den bygger på en godkjent mellombalanse (§ 8-2 a). Be brukeren avklare med regnskapsfører.
3. **Lån til aksjonær.** Da er det en fordring, ikke en utdeling. Utenfor den låste modellen: flagg og be brukeren avklare med regnskapsfører.
4. **Tilbakebetaling av innbetalt kapital.** Også utenfor modellen. Flagg.

Dette er den vanligste situasjonen det året et selskap går over fra utbetalingsmodellen (Bodil ≤ 0.6.0) til avsetningsmodellen, siden det ikke finnes noen inngående avsetning å dekke utbetalingen med.

### Datterselskap eller andre aksjer

Hver eierpost i `selskap.yaml` står på én av to balanselinjer, og skillet er **kontroll**, ikke skattens 90 %-grense. Et selskap er datterselskap når holdingselskapet har bestemmende innflytelse over det, og det har det alltid med flertallet av stemmene eller rett til å velge eller avsette flertallet av styret (regnskapsloven § 1-3, aksjeloven § 1-3 andre ledd).

- Har eierposten `datterselskap: true` eller `false`, bruk det. Feltet er valgfritt og overstyrer eierandelen, for tilfeller der stemmeandelen avviker fra eierandelen eller kontrollen følger av avtale.
- Ellers: `eierandel_prosent` over 50 gir `aksjer_i_datterselskap`, under 50 gir `andre_aksjer`.
- **Flagg og spør** når kontroll ikke kan avgjøres: eierandel på nøyaktig 50 %, manglende `eierandel_prosent`, eller flere aksjeklasser med ulik stemmerett. Spør om selskapet har flertallet av stemmene eller rett til å velge flertallet av styret, og be brukeren sette `datterselskap` på eierposten.

Linjen styrer mer enn plasseringen: Wenche oppgir selskapet som morselskap i årsregnskapet når `aksjer_i_datterselskap` er over 0. Et heleid datterselskap under `andre_aksjer` rapporterer derfor holdingselskapet som «ikke morselskap».

**Overgang fra Bodil 1.0.0 og eldre:** da sto alle eierposter under `andre_aksjer`. Er en eierpost datterselskap etter reglene over, og står den under «Andre aksjer» i fjorårets `regnskap.md`, skal du omklassifisere fjorårets beløp til «Aksjer i datterselskap» i sammenligningskolonnen. Da er linjene sammenlignbare (rskl. § 6-6). Summen eiendeler endres ikke. Skriv omklassifiseringen under Merknader, og ikke endre fjorårets `regnskap.md`.

### Salg av eierpost

Eierposten står til kostpris. Ved salg fjernes kostprisen fra balansen (`andre_aksjer`, eller `aksjer_i_datterselskap` hvis posten står der), og salgssummen kommer inn på bankkontoen. Differansen er et regnskapsmessig resultat:

- `gevinst_ved_realisasjon_av_aksjer` = salgssum − kostpris, når positiv
- `tap_ved_realisasjon_av_aksjer` = kostpris − salgssum, når positiv

Uten denne linjen går ikke balansen opp når salgssummen avviker fra kostprisen.

- **Delsalg:** fjern en forholdsmessig del av kostprisen (kostpris × solgte aksjer / aksjer i posten før salget). Er posten kjøpt i flere omganger til ulik pris, spør hvilken kostpris som gjelder i stedet for å velge.
- **`selskap.yaml` må oppdateres av brukeren:** be brukeren fjerne eierposten (helt salg) eller redusere `kostpris` og `eierandel_prosent` (delsalg), slik at `eierposter` viser beholdningen per 31.12. Regn balansen ut fra den oppdaterte fila, og bekreft at summen stemmer med inngående kostpris minus det som er solgt. Det samme gjelder ved kjøp: be brukeren legge til posten.
- **Kostpris, salgssum og dato** skal fremgå av bilag (avtale eller sluttseddel). Mangler salgssummen i bankeksporten, eller er den motregnet mot noe annet, flagg og spør.

## Beregning

1. Klassifiser hver rad og før den i en **transaksjonslogg**.
2. Summer:
   - `andre_driftskostnader` = sum av alle «andre utbetalinger»
   - `utbytte_fra_datterselskap` = sum mottatt utbytte fra datterselskap
   - `andre_finansinntekter` = sum renteinntekter fra banken
   - `rentekostnader` = sum renter belastet av banken
   - `utbytte_utbetalt` = sum utbetalt til eier som utbytte, ikke nedbetaling av lån fra aksjonær. Dette tallet er **bare** en kontantstrøm og en post i aksjonærregisteroppgaven; det reduserer ikke egenkapitalen med mindre steget over konkluderte med utbytte vedtatt i året
   - endring i `laan_fra_aksjonaer` = sum innskudd fra eier − sum nedbetalt lån til eier
3. **Skattekostnad.** Et år uten utbytte gir normalt 0, siden bankrentene sjelden overstiger gebyrene. Et år med mottatt utbytte, eller med renteinntekter større enn kostnadene, har en liten reell skattekostnad, og regnskapsloven § 6-1 krever den som egen linje før årsresultatet. Regn i denne rekkefølgen:
   - **Fremførbart underskudd 01.01** = «Underskudd til fremføring neste år» under «Skattemessig» i `<år-1>/regnskap.md`. Finnes ikke fjorårets fil (år 1, eller år ført utenfor Bodil), **spør brukeren** om fremførbart underskudd fra fjorårets skattemelding i stedet for å anta 0. Fastsett tallet hvert år, også når årets inntekt er negativ: det er dette tallet `wenche-config` skal sende til Wenche.
   - `skattepliktig_utbytte` = 0 hvis eierandelen er mer enn 90 %, ellers 3 % av mottatt utbytte rundet opp til nærmeste krone (fritaksmetoden, sktl. § 2-38 sjette ledd). Unntaket fra sjablonen gjelder konsern etter sktl. § 10-4, som krever *mer enn* 90 % av aksjene og stemmene, så nøyaktig 90 % gir 3 %. Eierandelen står under `eierposter` i `selskap.yaml`. Har selskapet flere eierposter med ulik eierandel, flagg det og spør hvilken posten utbyttet kom fra i stedet for å velge selv. Dette er en skattegrense og har ingenting med om eierposten er datterselskap å gjøre: en eierandel på 60 % er datterselskap i balansen, men utbyttet derfra er likevel 3 %-beskattet.
   - `skattepliktig_inntekt` = `skattepliktig_utbytte + andre_finansinntekter − andre_driftskostnader − rentekostnader`. Renteinntektene tas med fullt ut: fritaksmetoden gjelder bare utbytte. Gevinst og tap ved realisasjon av aksjer holdes utenfor: under fritaksmetoden er gevinsten skattefri og tapet ikke fradragsberettiget (sktl. § 2-38), og 3 %-sjablonen gjelder bare utbytte, ikke gevinst. Dette gjelder aksjer i norske aksjeselskaper. Er det solgte selskapet utenlandsk, **flagg og spør**: fritaksmetoden har egne vilkår for selskaper utenfor EØS og i lavskatteland (sktl. § 2-38), og Bodil avgjør ikke det.
   - Er `skattepliktig_inntekt` positiv, trekk fra fremførbart underskudd 01.01, høyst like mye som inntekten. Det som trekkes fra er «anvendt fremført underskudd».
   - `skattekostnad` = 22 % av det som står igjen, rundet opp. Er `skattepliktig_inntekt` 0 eller negativ etter fradrag, er skattekostnaden 0.
   - **Underskudd til fremføring neste år**: er `skattepliktig_inntekt` negativ, fremførbart underskudd 01.01 pluss hele det negative beløpet. Er den positiv, fremførbart underskudd 01.01 minus anvendt fremført underskudd. Dette er saldoen 31.12. Den blir neste års 01.01-tall og skal **ikke** til Wenche i år: Wenche legger selv til årets underskudd, så saldoen 31.12 i Wenches felt teller årets underskudd to ganger.
4. **Årsresultat** = `utbytte_fra_datterselskap + andre_finansinntekter + gevinst_ved_realisasjon_av_aksjer − tap_ved_realisasjon_av_aksjer − andre_driftskostnader − rentekostnader − skattekostnad`
5. **Utbytte for året.** Dette er en beslutning, ikke en transaksjon, så den kommer ikke fra bankeksporten. Spør brukeren om styret foreslår utbytte for dette regnskapsåret. Blir svaret ja:
   - `avsatt_utbytte_i_aar` = beløpet. Det avsettes som kortsiktig gjeld per 31.12 og reduserer egenkapitalen i **dette** året, ikke i året det utbetales (rskl. § 6-2, aksjeloven § 8-2 første ledd).
   - **Krev dekning.** `overkursfond + annen_egenkapital` etter avsetningen må være ≥ 0 (aksjeloven § 8-1). En avsetning er en utdeling og kan gjøre fri egenkapital negativ helt alene. Er den negativ, stopp og be brukeren redusere beløpet.
   - Generalforsamlingen vedtar avsetningen når den godkjenner årsregnskapet, altså i `protokoll`-skillen. Bodil foregriper ikke vedtaket, den fører styrets forslag.
6. **Balanse per 31.12:**
   - `bankinnskudd` = åpningssaldo + sum alle transaksjoner (skal stemme med faktisk saldo 31.12, sjekk mot bankutskrift)
   - `aksjer_i_datterselskap` = sum kostpris for eierposter som er datterselskap (se «Datterselskap eller andre aksjer») per 31.12, etter eventuelle kjøp og salg i året (se «Salg av eierpost»)
   - `andre_aksjer` = sum kostpris for øvrige eierposter per 31.12
   - `aksjekapital` = fra `selskap.yaml`
   - `annen_egenkapital` = inngående annen egenkapital + årsresultat − `avsatt_utbytte_i_aar` − eventuelt utbytte vedtatt og utbetalt i året (steget «Utbetaling uten avsetning»). Merk at et utbytte utbetalt i år som gjør opp fjorårets avsetning **ikke** står her: det traff egenkapitalen i fjor.
   - `avsatt_utbytte` = inngående avsatt utbytte − utbetalt i år mot den avsetningen + `avsatt_utbytte_i_aar`
   - `laan_fra_aksjonaer` = inngående lån + årets innskudd fra eier − årets nedbetaling. Kan ikke bli negativ: da er noe feilklassifisert
   - `betalbar_skatt` = inngående betalbar skatt − skatt betalt i år + årets `skattekostnad`. Skatten fastsettes og betales året etter, så årets skattekostnad står normalt ubetalt i balansen per 31.12. Dette er motposten til skattekostnaden: uten den går ikke balansen opp, og Wenche varsler om en skattekostnad uten motpost.
7. **Kontroller at balansen går opp:** sum eiendeler = sum egenkapital og gjeld. Hvis ikke, finn årsaken (oftest en feilklassifisert transaksjon eller feil åpningssaldo) før du går videre.
8. **Utbytte uten dekning:** hvis `overkursfond + annen_egenkapital < 0` per 31.12 etter at avsetningen og et eventuelt utbytte vedtatt i året er trukket fra, **stopp**: utbytte kan bare deles ut av fri egenkapital (aksjeloven § 8-1). Dette gjelder avsetningen like fullt som en utbetaling, siden begge er utdelinger etter § 8-1. Kontrollen her gjelder årets balanse. Et utbytte vedtatt i året skal i tillegg ha dekning i sist godkjente balanse (valg 2 i «Utbetaling uten avsetning»), og at årets resultat dekker det, er ikke nok.

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
| Gevinst ved realisasjon av aksjer | <x> | ... |
| Andre finansinntekter (renteinntekter) | <x> | ... |
| Rentekostnader | <x> | ... |
| Tap ved realisasjon av aksjer | <x> | ... |
| Andre finanskostnader | 0 | ... |
| Skattekostnad | <x> | ... |
| **Årsresultat** | <x> | ... |

## Balanse per 31.12
### Eiendeler
| Post | <år> | <år-1> |
|---|--:|--:|
| Aksjer i datterselskap | <x> | ... |
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
| Fremførbart underskudd 01.01 (fjorårets «Underskudd til fremføring neste år», eller fjorårets skattemelding) | <x> |
| Mottatt utbytte | <x> |
| Skattepliktig del av utbyttet (3 %-sjablon, 0 ved eierandel over 90 %) | <x> |
| Renteinntekter (fullt skattepliktig) | <x> |
| Driftskostnader og rentekostnader (fradrag) | <x> |
| Gevinst (+) / tap (−) ved realisasjon av aksjer, holdt utenfor (fritaksmetoden) | <x> |
| Skattepliktig inntekt før fradrag | <x> |
| Anvendt fremført underskudd | <x> |
| Skattepliktig inntekt | <x> |
| Beregnet skatt (22 %) | <x> |
| **Underskudd til fremføring neste år** | <x> |

«Fremførbart underskudd 01.01» er input til `underskudd_til_fremfoering` i `wenche-config`. «Underskudd til fremføring neste år» er saldoen 31.12 og blir neste års 01.01-tall. Uten seksjonen må tallet hentes manuelt fra fjorårets skattemelding hvert år.

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
- Eventuelle flagg (salg av eierpost, utbytte uten dekning, utbetaling til eier uten avsetning, utbytte eller nedbetaling av lån, mulig kapitalforhøyelse, renter til eier, Skatteetaten eller på lån i banken, uklare transaksjoner, store poster)
```

Feltnavnene i tabellene er bevisst de samme som Wenche bruker, slik at `wenche-config`-skillen kan mappe dem nær mekanisk.

## Neste steg

Når `regnskap.md` er ferdig og balansen går opp: kjør **protokoll**-skillen, og deretter **wenche-config**.
