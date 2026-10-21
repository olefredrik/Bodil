# Den låste modellen

Bodil fører etter en bevisst minimal, låst bokføringsmodell. Den dekker det et passivt holdingselskap faktisk har, og ingenting mer. Det er det som gjør at en bankeksport kan bli et korrekt regnskap nesten mekanisk.

## Hver transaksjon

| Hendelse i bankeksporten | Bokføres som |
|---|---|
| Penger inn fra eier | Lån fra aksjonær (gjeld). Flagges hvis beskrivelsen tyder på kapitalforhøyelse eller tilleggsinnbetaling |
| Utbytte mottatt fra datterselskap | Finansinntekt (utbytte fra datterselskap) |
| Penger ut til eier, opp til utestående avsatt utbytte | Reduserer avsatt utbytte (gjeld), ikke egenkapital. Flagges hvis selskapet også har lån fra aksjonær |
| Penger ut til eier, bekreftet som nedbetaling, opp til utestående lån fra aksjonær | Reduserer lån fra aksjonær (gjeld), ikke egenkapital |
| Penger ut til eier utover det | Flagges: nedbetaling av lån fra aksjonær, utbytte vedtatt i året, lån til aksjonær, eller tilbakebetaling av kapital |
| Renteinntekt fra banken | Andre finansinntekter (fullt skattepliktig) |
| Renter belastet av banken på kontoen (debetrenter) | Rentekostnader |
| Renter på lån i banken, til eier eller til Skatteetaten | Flagges: et lån i banken er utenfor modellen; ellers hvilket lån, og om renten er fradragsberettiget |
| Alle andre utbetalinger | Driftskostnad (typisk bankgebyrer) |
| Kjøp av eierpost | Finansielle anleggsmidler til kostpris (fra `selskap.yaml`): aksjer i datterselskap eller andre aksjer |
| Salg av eierpost | Kostprisen ut av balansen, differansen mot salgssummen er gevinst eller tap ved realisasjon av aksjer |
| Betaling av skatt til Skatteetaten | Reduserer betalbar skatt (gjeld), ikke en kostnad |

Ingen andre kontoer, ingen inntekter utover utbytte fra datterselskap, renter fra banken og gevinst ved salg av aksjer. Resultatet blir normalt et lite underskudd lik driftskostnadene minus bankrentene, med mindre det er mottatt utbytte.

## Datterselskap eller andre aksjer

Eierpostene står til kostpris, men på én av to linjer i balansen. Skillet er **kontroll**: et selskap er datterselskap når holdingselskapet har bestemmende innflytelse over det, og det har det alltid med flertallet av stemmene eller rett til å velge eller avsette flertallet av styret (regnskapsloven § 1-3, aksjeloven § 1-3 andre ledd). Bodil leser det av `eierandel_prosent` i `selskap.yaml`: over 50 % er datterselskap, under 50 % er andre aksjer. Avviker stemmene fra eierandelen, eller følger kontrollen av en avtale, setter du `datterselskap: true` eller `false` på eierposten. Ved nøyaktig 50 % flagger Bodil og spør.

Linjen er ikke bare kosmetikk. Wenche oppgir selskapet som morselskap i årsregnskapet når det har aksjer i datterselskap, så et heleid datterselskap ført som andre aksjer gir feil opplysning. Små foretak trenger likevel ikke konsernregnskap (regnskapsloven § 3-2), så datterselskapet står fortsatt bare til kostpris.

90 %-grensen hører til skatten, ikke balansen: den avgjør om utbytte er fullt skattefritt (se «Skatt» under).

## Utbytte

Utbytte er den ene posten som ikke kommer fra bankeksporten, fordi den er en beslutning og ikke en betaling. Bodil følger aksjelovens normalsti: styret foreslår utbyttet når regnskapet utarbeides, det står som **avsatt utbytte** (kortsiktig gjeld) per 31.12 og reduserer egenkapitalen i **det året det gjelder**. Generalforsamlingen vedtar avsetningen når den godkjenner årsregnskapet, og utbetalingen året etter gjør bare opp gjelden.

Det gjør protokollen til et ekte bilag: den vedtar noe som ennå ikke er utbetalt, og alt er datert når det faktisk skjer. Den gamle modellen, der utbyttet ble bokført når pengene forlot konto, tvang protokollen til å «vedta» en utdeling som hadde skjedd et år tidligere.

Datoen for generalforsamlingen i protokollen brukes igjen året etter. Når det avsatte utbyttet utbetales, rapporteres vedtaksdatoen i aksjonærregisteroppgaven, og `wenche-config` henter den fra fjorårets `protokoll.md`. Skriv derfor den faktiske møtedatoen i protokollen.

Går det likevel penger til eier uten en avsetning å dekke dem med, gjetter ikke Bodil. Den spør om det er en nedbetaling av lån fra aksjonær, et utbytte vedtatt i løpet av året på grunnlag av fjorårets godkjente regnskap (da kreves et bilag datert senest på betalingsdagen, og Bodil lager det ikke i ettertid), et lån til aksjonær, eller en tilbakebetaling av innbetalt kapital.

## Lån fra aksjonær

Penger inn fra eier føres som lån fra aksjonær, og en nedbetaling av lånet reduserer gjelden igjen. Begge deler er bevegelser i en gjeldspost og rører verken resultat eller egenkapital. Nedbetalingen gjettes likevel ikke på når den kan forveksles med utbytte: har selskapet både utestående avsatt utbytte og lån fra aksjonær, er en utbetaling til eier tvetydig, og bare brukeren vet hva den var. Forskjellen betyr noe for eieren, fordi utbytte er skattepliktig og går i aksjonærregisteroppgaven, mens en nedbetaling av lån ikke er det. Derfor spør Bodil i stedet for å la avsetningen dekke utbetalingen først.

Er en innbetaling fra eier egentlig en kapitalforhøyelse, krever den vedtak i generalforsamlingen og registrering i Foretaksregisteret (aksjeloven kapittel 10), og den endrer aksjekapitalen i stedet for gjelden. Bodil fører innbetalinger som lån med mindre beskrivelsen tyder på noe annet, og flagger da i stedet for å gjette.

## Skatt

Renteinntekter fra banken er vanlig kapitalinntekt for selskapet. De omfattes ikke av fritaksmetoden og er fullt skattepliktige med 22 %. Rentekostnader er fradragsberettigede på samme måte som driftskostnadene. I et hvilende år er bankrentene som regel mindre enn gebyrene, så skattepliktig inntekt blir negativ og skattekostnaden 0. Mottar selskapet utbytte og eierandelen er 90 % eller lavere, er 3 % av utbyttet skattepliktig (sjablonregelen i fritaksmetoden, sktl. § 2-38 sjette ledd). Da har selskapet en reell, liten skattekostnad, og regnskapsloven § 6-1 krever den som egen linje før årsresultatet. Bodil regner den etter samme regel som Wenche: skattepliktig del av utbyttet pluss renteinntekter, minus driftskostnader og rentekostnader, minus eventuelt fremført underskudd, ganget med 22 %. Overstiger renteinntektene kostnadene, gir det en skattekostnad også uten utbytte.

Skatten fastsettes og betales året etter, så den står som **betalbar skatt** i balansen per 31.12. Betalingen året etter reduserer den gjelden og er ikke en ny kostnad. Ved eierandel over 90 % er utbyttet fullt skattefritt, og skattekostnaden blir 0. Grensen er *mer enn* 90 % (konsern etter sktl. § 10-4), så nøyaktig 90 % gir 3 %-sjablon. Grensen gjelder uavhengig av om eierposten er datterselskap i balansen.

Selges en eierpost, er gevinsten skattefri og tapet ikke fradragsberettiget under fritaksmetoden, og 3 %-sjablonen gjelder ikke gevinst. Gevinst og tap står derfor i resultatet, men holdes utenfor skatteberegningen. Er det solgte selskapet utenlandsk, flagger Bodil det. `wenche-config` fører beløpene til Wenches egne felt for gevinst og tap ved realisasjon av aksjer, og Wenche holder dem utenfor skatteberegningen på samme måte. Brukeren må selv fjerne eller redusere eierposten i `selskap.yaml`.

## Flagg, ikke gjett

Alt som ikke entydig passer modellen blir **flagget, ikke gjettet**. Claude stopper og spør ved blant annet:

- transaksjoner som ikke passer en rad over,
- uvanlig store poster,
- utbytte uten dekning i fri egenkapital (jf. aksjeloven § 8-1), som gjelder en avsetning like fullt som en utbetaling. Et utbytte vedtatt i løpet av året må ha dekning i sist godkjente årsregnskap, så årets resultat kan ikke dekke det,
- penger ut til eier uten en avsetning som dekker dem,
- penger ut til eier som kan være både utbytte og nedbetaling av lån fra aksjonær,
- penger inn fra eier som ser ut som en kapitalforhøyelse eller tilleggsinnbetaling.

Balansen skal alltid gå opp: sum eiendeler = sum egenkapital og gjeld. Gjør den ikke det, finner Claude årsaken før det går videre.

## Mappestruktur

```
selskap.yaml              dine stamdata (utenfor git)
<år>/
  bankeksport.csv         rådata fra banken (utenfor git som standard)
  bilag/                  avtaler, kvitteringer, verdioversikter (oppbevaringsplikt 5 år)
  regnskap.md             selve regnskapet (versjoneres)
  protokoll.md            generalforsamlingsprotokoll (versjoneres)
  config.yaml             input til Wenche (utenfor git)
```

Git-historikken til `regnskap.md` fungerer som et uforanderlig revisjonsspor. Selve bilagene må du likevel oppbevare i fem år. Git er arbeidsboka, ikke arkivet.

!!! note "Rekkefølge med én avhengighet"
    Utbytte må avgjøres før protokollen skrives, siden protokollen vedtar avsetningen. Ellers er årshjulet i [Bruk](bruk.md) rett frem.
