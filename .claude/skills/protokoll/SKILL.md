---
name: protokoll
description: Lag generalforsamlingsprotokoll for et regnskapsår for et passivt holdingselskap. Leser <år>/regnskap.md og stamdata, og produserer <år>/protokoll.md som godkjenner årsregnskapet og vedtar utbytte eller dekning av underskudd. Fungerer også som utbytte-bilag. Bruk etter bokforing.
---

# Skill: protokoll

Lager den ordinære generalforsamlingsprotokollen for et regnskapsår. Den godkjenner årsregnskapet og vedtar disponeringen (utbytte eller dekning av underskudd). Protokollen er samtidig det lovpålagte bilaget for et eventuelt utbytte.

## Input

- `<år>/regnskap.md` (fra bokforing-skillen), særlig årsresultat, fri egenkapital og eventuelt utbytte.
- `selskap.yaml` (selskapsnavn, org.nr., daglig leder/styreleder, aksjonærer).

## Regler før du skriver

- **Utbytte krever dekning.** Vedta bare utbytte hvis det finnes fri egenkapital (`overkursfond + annen_egenkapital ≥ utbyttet`, jf. aksjeloven § 8-1). Hvis regnskapet viser et utbytte uten dekning, stopp og be brukeren avklare før du skriver protokollen.
- **Ved underskudd:** protokollen fastslår at årets underskudd dekkes av (føres mot) annen egenkapital, og at det ikke utdeles utbytte.
- **Revisjon:** små holdingselskaper er normalt fritatt for revisjonsplikt. Protokollen bekrefter at årsregnskapet er fastsatt uten revisjon. Er du i tvil om selskapet faktisk er fritatt, flagg det.
- Ikke skriv fullt fødselsnummer i protokollen (den versjoneres); bruk navn.

## Output: `<år>/protokoll.md`

```markdown
# Protokoll fra ordinær generalforsamling, <selskapsnavn>

**Org.nr.:** <org_nummer>
**Regnskapsår:** <år>
**Dato for generalforsamling:** <dato, settes av brukeren / dagens dato>
**Sted:** <forretningsadresse>

## 1. Åpning og konstituering
Generalforsamlingen ble åpnet av <styreleder>. Følgende aksjonærer var representert:
- <navn>, <antall_aksjer> aksjer

Innkalling og dagsorden ble godkjent.

## 2. Godkjenning av årsregnskapet
Årsregnskapet for <år> ble fremlagt, med et **årsresultat på <x> kr**. Generalforsamlingen vedtok å godkjenne resultatregnskapet og balansen.

## 3. Disponering av årsresultatet
<Ett av to:>
- Generalforsamlingen vedtok å utdele et utbytte på **<x> kr**, som belastes fri egenkapital. Etter utdelingen utgjør fri egenkapital <x> kr.
- Generalforsamlingen vedtok at årets underskudd på <x> kr dekkes av annen egenkapital. Det utdeles ikke utbytte.

## 4. Revisjon
Selskapet er fritatt for revisjonsplikt, og årsregnskapet er fastsatt uten revisor.

## 5. Avslutning
Det forelå ingen øvrige saker. Møtet ble hevet.

___________________________
<styreleder>, møteleder
```

## Neste steg

Kjør **wenche-config**-skillen for å generere `config.yaml` til Wenche.
