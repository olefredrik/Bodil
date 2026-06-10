# Den låste modellen

Bodil fører etter en bevisst minimal, låst bokføringsmodell. Den dekker det et passivt holdingselskap faktisk har, og ingenting mer. Det er det som gjør at en bankeksport kan bli et korrekt regnskap nesten mekanisk.

## Hver transaksjon

| Hendelse i bankeksporten | Bokføres som |
|---|---|
| Penger inn fra eier | Lån fra aksjonær (gjeld) |
| Utbytte mottatt fra datterselskap | Finansinntekt (utbytte fra datterselskap) |
| Penger ut til eier | Utbytte (reduserer egenkapital) |
| Alle andre utbetalinger | Driftskostnad (typisk bankgebyrer) |
| Kjøp/salg av eierposter | Finansielle anleggsmidler til kostpris (fra `selskap.yaml`) |

Ingen andre kontoer, ingen inntekter utover utbytte fra datterselskap. Resultatet blir et lite underskudd lik driftskostnadene, med mindre det er mottatt utbytte.

## Flagg, ikke gjett

Alt som ikke entydig passer modellen blir **flagget, ikke gjettet**. Claude stopper og spør ved blant annet:

- transaksjoner som ikke passer en rad over,
- uvanlig store poster,
- utbytte uten dekning i fri egenkapital (jf. aksjeloven § 8-1).

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
    Utbytte må avgjøres før protokollen skrives, siden protokollen vedtar det. Ellers er årshjulet i [Bruk](bruk.md) rett frem.
