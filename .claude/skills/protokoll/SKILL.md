---
name: protokoll
description: Lag generalforsamlingsprotokoll for et regnskapsår for et passivt holdingselskap. Leser <år>/regnskap.md og stamdata, og produserer <år>/protokoll.md som godkjenner årsregnskapet og vedtar avsetning av utbytte eller dekning av underskudd. Er bilag for utbytte den selv vedtar, ikke for utbytte som allerede er utbetalt i året. Bruk etter bokforing.
---

# Skill: protokoll

Lager den ordinære generalforsamlingsprotokollen for et regnskapsår. Den godkjenner årsregnskapet og vedtar disponeringen: avsetning av utbytte, eller dekning av underskudd. Protokollen er bilaget for et utbytte den selv vedtar, altså en avsetning. Den er **ikke** bilag for et utbytte som allerede er utbetalt i løpet av regnskapsåret; det vedtaket ble truffet før denne protokollen ble skrevet.

## Input

- `<år>/regnskap.md` (fra bokforing-skillen), særlig årsresultat, fri egenkapital og «Utbytte»-seksjonen.
- `selskap.yaml` (selskapsnavn, org.nr., daglig leder/styreleder, aksjonærer).

## Regler før du skriver

- **Protokollen vedtar avsetningen, ikke en utbetaling.** Utbytte for regnskapsåret står som `avsatt utbytte` i balansen per 31.12: styret har foreslått det, og generalforsamlingen vedtar det når den godkjenner årsregnskapet. Utbetalingen skjer etterpå og gjør bare opp gjeldsposten.
- **Utbytte krever dekning.** Vedta bare avsetningen hvis fri egenkapital (`overkursfond + annen_egenkapital`) er ≥ 0 etter at den er trukket fra, jf. aksjeloven § 8-1. Er den negativ, stopp og be brukeren avklare før du skriver protokollen.
- **Utbytte som allerede er utbetalt i regnskapsåret skal ikke vedtas her.** Viser «Utbytte»-seksjonen et beløp under «vedtatt og utbetalt i året», ble det besluttet i løpet av året på grunnlag av fjorårets godkjente årsregnskap. Denne protokollen skrives etter at pengene forlot konto og kan ikke vedta dem i ettertid. Omtal utdelingen som et faktum, ikke som en beslutning, og bruk formuleringen i punkt 3 under. **Tilbakedater aldri** et vedtak, og ikke skriv en protokoll som gir inntrykk av å være bilaget for det. Mangler bilaget, si det til brukeren.
- **Ved underskudd:** protokollen fastslår at årets underskudd dekkes av (føres mot) annen egenkapital, og at det ikke avsettes utbytte.
- **Ved overskudd uten utbytte:** protokollen fastslår at årets overskudd overføres til annen egenkapital, og at det ikke avsettes utbytte.
- **Ved avsetning:** si også hva som skjer med resten av årsresultatet. Er årsresultatet større enn avsetningen, overføres differansen til annen egenkapital. Er det mindre, dekkes differansen av annen egenkapital.
- **Utbytte utbetalt i år mot fjorårets avsetning** ble vedtatt på fjorårets generalforsamling og skal ikke omtales i punkt 3. Utbetalingen gjorde bare opp en gjeldspost.
- **Revisjon:** små holdingselskaper er normalt fritatt for revisjonsplikt. Protokollen bekrefter at årsregnskapet er fastsatt uten revisjon. Er du i tvil om selskapet faktisk er fritatt, flagg det.
- **Datoen for generalforsamlingen skal være den faktiske møtedatoen.** Spør brukeren om den hvis den ikke er kjent, og skriv den som ÅÅÅÅ-MM-DD. Den blir `utbytte_vedtaksdato` i aksjonærregisteroppgaven neste år, når det avsatte utbyttet utbetales.
- Ikke skriv fullt fødselsnummer i protokollen (den versjoneres); bruk navn.

## Output: `<år>/protokoll.md`

```markdown
# Protokoll fra ordinær generalforsamling, <selskapsnavn>

**Org.nr.:** <org_nummer>
**Regnskapsår:** <år>
**Dato for generalforsamling:** <den faktiske møtedatoen, ÅÅÅÅ-MM-DD>
**Sted:** <forretningsadresse>

## 1. Åpning og konstituering
Generalforsamlingen ble åpnet av <styreleder>. Følgende aksjonærer var representert:
- <navn>, <antall_aksjer> aksjer

Innkalling og dagsorden ble godkjent.

## 2. Godkjenning av årsregnskapet
Årsregnskapet for <år> ble fremlagt, med et **årsresultat på <x> kr**. Generalforsamlingen vedtok å godkjenne resultatregnskapet og balansen.

## 3. Disponering av årsresultatet
<Velg det som passer. De to første utelukker ikke hverandre: et selskap kan ha utdelt tilleggsutbytte i året OG avsette nytt utbytte for året. Uten avsetning brukes en av de to siste, etter om årsresultatet er positivt eller negativt.>
- Generalforsamlingen vedtok styrets forslag om et utbytte på **<x> kr**, avsatt i årsregnskapet per 31.12.<år> og oppført som kortsiktig gjeld. Utbyttet belastes fri egenkapital, som etter avsetningen utgjør <x> kr. Utbetaling skjer i <år+1>. <Resten av årsresultatet, <x> kr, overføres til annen egenkapital. / Differansen mellom avsetningen og årsresultatet, <x> kr, dekkes av annen egenkapital.>
- Det ble i løpet av regnskapsåret utdelt et utbytte på <x> kr, vedtatt <dato> på grunnlag av det godkjente årsregnskapet for <år-1>. Utdelingen framgår av årsregnskapet som nå godkjennes. Denne protokollen er ikke bilaget for det vedtaket.
- Generalforsamlingen vedtok at årets overskudd på <x> kr overføres til annen egenkapital. Det avsettes ikke utbytte.
- Generalforsamlingen vedtok at årets underskudd på <x> kr dekkes av annen egenkapital. Det avsettes ikke utbytte.

## 4. Revisjon
Selskapet er fritatt for revisjonsplikt, og årsregnskapet er fastsatt uten revisor.

## 5. Avslutning
Det forelå ingen øvrige saker. Møtet ble hevet.

___________________________
<styreleder>, møteleder
```

## Neste steg

Kjør **wenche-config**-skillen for å generere `config.yaml` til Wenche.
