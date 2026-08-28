# Den låste modellen

Bodil fører etter en bevisst minimal, låst bokføringsmodell. Den dekker det et passivt holdingselskap faktisk har, og ingenting mer. Det er det som gjør at en bankeksport kan bli et korrekt regnskap nesten mekanisk.

## Hver transaksjon

| Hendelse i bankeksporten | Bokføres som |
|---|---|
| Penger inn fra eier | Lån fra aksjonær (gjeld) |
| Utbytte mottatt fra datterselskap | Finansinntekt (utbytte fra datterselskap) |
| Penger ut til eier, opp til utestående avsatt utbytte | Reduserer avsatt utbytte (gjeld), ikke egenkapital |
| Penger ut til eier utover det | Flagges: utbytte vedtatt i året, lån til aksjonær, eller tilbakebetaling av kapital |
| Alle andre utbetalinger | Driftskostnad (typisk bankgebyrer) |
| Kjøp/salg av eierposter | Finansielle anleggsmidler til kostpris (fra `selskap.yaml`) |
| Betaling av skatt til Skatteetaten | Reduserer betalbar skatt (gjeld), ikke en kostnad |

Ingen andre kontoer, ingen inntekter utover utbytte fra datterselskap. Resultatet blir et lite underskudd lik driftskostnadene, med mindre det er mottatt utbytte.

## Utbytte

Utbytte er den ene posten som ikke kommer fra bankeksporten, fordi den er en beslutning og ikke en betaling. Bodil følger aksjelovens normalsti: styret foreslår utbyttet når regnskapet utarbeides, det står som **avsatt utbytte** (kortsiktig gjeld) per 31.12 og reduserer egenkapitalen i **det året det gjelder**. Generalforsamlingen vedtar avsetningen når den godkjenner årsregnskapet, og utbetalingen året etter gjør bare opp gjelden.

Det gjør protokollen til et ekte bilag: den vedtar noe som ennå ikke er utbetalt, og alt er datert når det faktisk skjer. Den gamle modellen, der utbyttet ble bokført når pengene forlot konto, tvang protokollen til å «vedta» en utdeling som hadde skjedd et år tidligere.

Går det likevel penger til eier uten en avsetning å dekke dem med, gjetter ikke Bodil. Den spør om det er et utbytte vedtatt i løpet av året på grunnlag av fjorårets godkjente regnskap (da kreves et bilag datert senest på betalingsdagen, og Bodil lager det ikke i ettertid), et lån til aksjonær, eller en tilbakebetaling av innbetalt kapital.

## Skatt

Et hvilende år har ingen skattepliktig inntekt, og skattekostnaden er 0. Mottar selskapet utbytte og eierandelen er under 90 %, er 3 % av utbyttet skattepliktig (sjablonregelen i fritaksmetoden, sktl. § 2-38 sjette ledd). Da har selskapet en reell, liten skattekostnad, og regnskapsloven § 6-1 krever den som egen linje før årsresultatet. Bodil regner den etter samme regel som Wenche: skattepliktig del av utbyttet minus driftskostnadene, minus eventuelt fremført underskudd, ganget med 22 %.

Skatten fastsettes og betales året etter, så den står som **betalbar skatt** i balansen per 31.12. Betalingen året etter reduserer den gjelden og er ikke en ny kostnad. Ved eierandel på 90 % eller mer er utbyttet fullt skattefritt, og skattekostnaden blir 0.

## Flagg, ikke gjett

Alt som ikke entydig passer modellen blir **flagget, ikke gjettet**. Claude stopper og spør ved blant annet:

- transaksjoner som ikke passer en rad over,
- uvanlig store poster,
- utbytte uten dekning i fri egenkapital (jf. aksjeloven § 8-1), som gjelder en avsetning like fullt som en utbetaling,
- penger ut til eier uten en avsetning som dekker dem.

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
