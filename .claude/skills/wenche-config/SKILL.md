---
name: wenche-config
description: Generer en config.yaml for Wenche fra et ferdig regnskap. Leser <år>/regnskap.md og stamdata, mapper mot Wenches eksakte feltnavn, skriver <år>/config.yaml, lager en sjekkliste over manuell verifisering, og kjører wenche valider-aarsregnskap. Bruk som siste steg før innsending.
---

# Skill: wenche-config

Mapper et ferdig regnskap til en `config.yaml` som Wenche konsumerer, og selv-verifiserer med Wenches egen validering. Du sender ingenting, det gjør brukeren i Wenche etterpå.

## Input

- `<år>/regnskap.md` (fra bokforing): alle tall til resultatregnskap og balanse, og fjorårets sammenligningstall.
- `selskap.yaml`: selskapsopplysninger (inkludert `kontakt_epost`) og aksjonærer (med fødselsnummer), eierposter.

## Output 1: `<år>/config.yaml`

Denne fila er gitignored og er det eneste stedet fødselsnummer skal skrives. Bruk Wenches eksakte feltnavn (bekreftet mot `config.example.yaml` i Wenche):

```yaml
selskap:
  navn: "<fra selskap.yaml>"
  org_nummer: "<9 siffer>"
  daglig_leder: "<navn>"
  styreleder: "<navn>"
  forretningsadresse: "<adresse>"
  stiftelsesaar: <år>
  stiftelsesdato: <ÅÅÅÅ-MM-DD>       # valgfri, men ta den med når den er kjent:
                                     # aksjonærregisteroppgaven oppgir ellers 1. januar
  aksjekapital: <NOK>
  tinginnskudd_ved_stiftelse: <NOK>  # valgfri, fra selskap.yaml. Ta den med KUN i selskapets
                                     # første regnskapsår, og bare hvis den er over 0: delen av
                                     # aksjekapitalen som ble skutt inn som aksjer i stedet for
                                     # penger. Uten den rapporterer egenkapitalavstemmingen hele
                                     # stiftelsesinnskuddet som kontantinnskudd. Kan aldri
                                     # overstige økningen i aksjekapital + overkursfond
  kontakt_epost: "<fra selskap.yaml>" # påkrevd for aksjonærregisteroppgaven. Mangler den i
                                     # selskap.yaml, spør brukeren og be dem legge den inn der

regnskapsaar: <år>

resultatregnskap:
  driftsinntekter:
    salgsinntekter: 0
    andre_driftsinntekter: 0
  driftskostnader:
    loennskostnader: 0
    avskrivninger: 0
    andre_driftskostnader: <fra regnskap.md>
  finansposter:
    utbytte_fra_datterselskap: <fra regnskap.md>
    andre_finansinntekter: <fra regnskap.md>   # renteinntekter fra banken, fullt skattepliktig
    rentekostnader: <fra regnskap.md>          # renter belastet av banken
    andre_finanskostnader: 0
    gevinst_ved_realisasjon_av_aksjer: <fra regnskap.md>   # salg av eierpost. Skattefri under
    tap_ved_realisasjon_av_aksjer: <fra regnskap.md>       # fritaksmetoden (tapet gir ikke fradrag),
                                       # så de skal IKKE i andre_finansinntekter/-kostnader, der
                                       # Wenche skattlegger dem fullt. 0 uten salg i året
  skattekostnad: <fra regnskap.md>     # egen linje før årsresultatet (rskl. § 6-1), 0 uten
                                       # skattepliktig inntekt

# regnskapsstart: <ÅÅÅÅ-MM-DD>       # UTELAT begge ved vanlig kalenderår. Tas bare med ved
# regnskapsslutt: <ÅÅÅÅ-MM-DD>       # forlenget første regnskapsår (rskl. § 1-7 andre ledd):
                                     # start = stiftelsesdato, slutt = 31.12, og
                                     # regnskapsaar over er året perioden AVSLUTTES

balanse:
  eiendeler:
    anleggsmidler:
      aksjer_i_datterselskap: <fra regnskap.md>   # eierposter selskapet har kontroll over (flertall
                                       # av stemmene, rskl. § 1-3). Over 0 gjør at Wenche oppgir
                                       # selskapet som morselskap i årsregnskapet
      andre_aksjer: <fra regnskap.md>  # øvrige eierposter
      langsiktige_fordringer: 0
    omloepmidler:
      kortsiktige_fordringer: 0
      bankinnskudd: <utgående saldo 31.12>
  egenkapital_og_gjeld:
    egenkapital:
      aksjekapital: <NOK>
      overkursfond: 0
      annen_egenkapital: <fra regnskap.md, kan være negativ>
    langsiktig_gjeld:
      laan_fra_aksjonaer: <fra regnskap.md>
      andre_langsiktige_laan: 0
    kortsiktig_gjeld:
      leverandoergjeld: 0
      betalbar_skatt: <fra regnskap.md>   # motposten til skattekostnaden, ubetalt skatt per 31.12
      skyldige_offentlige_avgifter: 0
      avsatt_utbytte: <fra «Utbytte» i regnskap.md>   # utestående avsatt utbytte 31.12 (konto
                                       # 2800). Reduserer egenkapitalen i avsetningsåret, ikke
                                       # i utbetalingsåret. 0 hvis ingenting er avsatt
      annen_kortsiktig_gjeld: 0

foregaaende_aar:                       # fjorårets tall fra sammenligningskolonnen i regnskap.md, med eventuell
                                       # omklassifisering av eierposter (sammenligningstall, rskl. § 6-6)
  resultatregnskap: { ... }            # samme felt som over. Mangler fjorårets resultat i regnskap.md
                                       # (og selskapet ble ikke stiftet i år), STOPP i stedet for å
                                       # utelate den: Wenche setter da fjorårets resultat stille til 0
  balanse: { ... }                     # samme felt som over
                                       # utelat hele foregaaende_aar bare hvis selskapet ble stiftet i år

skattemelding:
  underskudd_til_fremfoering: <«Fremførbart underskudd 01.01» fra «Skattemessig» i regnskap.md>
                                       # saldoen ved årets START. Wenche legger selv til årets
                                       # underskudd, så «Underskudd til fremføring neste år»
                                       # (saldoen 31.12) her ville telt det to ganger. Se under
  anvend_fritaksmetoden: true          # holdingselskap som eier aksjer
  eierandel_for_fritaksmetoden: <prosent>   # over 90 % gir fullt skattefritt utbytte; 90 % eller lavere gir 3 % sjablonbeskatning
  boersnotert: false
  formuesverdi_aksjer: <RF-1088S post 209, MÅ fylles inn manuelt>

aksjonaerer:
  - navn: "<navn>"
    fodselsnummer: "<11 siffer>"
    antall_aksjer: <n>
    aksjeklasse: "ordinære"
    utbytte_utbetalt: <fra «Utbytte» i regnskap.md: utbetalt mot fjorårets avsetning + eventuelt
                       # utbytte vedtatt og utbetalt i året. Dette er kontantstrømmen i året, ikke
                       # årets avsetning, og kan derfor avvike fra avsatt_utbytte over>
    innbetalt_kapital_per_aksje: <aksjekapital / antall aksjer>

utbytte_vedtaksdato: <ÅÅÅÅ-MM-DD>     # påkrevd når en aksjonær har utbytte_utbetalt > 0, ellers
                                     # utelat. Datoen generalforsamlingen vedtok utbyttet som ble
                                     # UTBETALT i år. Må ligge i regnskapsåret. Se under
```

### Fremførbart underskudd

`underskudd_til_fremfoering` er saldoen ved årets **start**. Hent den fra linjen «Fremførbart underskudd 01.01» under «Skattemessig» i `regnskap.md`.

Mangler linjen, er `regnskap.md` typisk ført med Bodil før 1.1.0. Bruk da **aldri** «Underskudd til fremføring neste år» fra samme fil, siden det er saldoen 31.12. Hent i stedet «Underskudd til fremføring neste år» fra `<år-1>/regnskap.md`. Finnes ikke den fila eller linjen, spør brukeren om fremførbart underskudd fra fjorårets skattemelding.

Kontroller tallet mot årets «Skattemessig»: fremførbart underskudd 01.01 pluss årets underskudd (eller minus anvendt fremført underskudd i et år med overskudd) skal gi «Underskudd til fremføring neste år». Stemmer det ikke, stopp og si fra.

### Vedtaksdato for utbytte

Wenche krever `utbytte_vedtaksdato` når det er utbetalt utbytte, og rapporterer den i aksjonærregisteroppgaven (RF-1086). Datoen gjelder utbyttet som ble **utbetalt** i år, ikke årets avsetning. Hent den slik, ut fra «Utbytte» i `regnskap.md`:

- **Utbetalt mot fjorårets avsetning:** vedtaket ble gjort på generalforsamlingen som godkjente fjorårets årsregnskap. Bruk «Dato for generalforsamling» i `<år-1>/protokoll.md`.
- **Utbytte vedtatt og utbetalt i året** (uten forutgående avsetning): Bodil har ikke laget det bilaget. **Spør brukeren** om datoen i vedtaket, og ikke gjett.
- **Begge deler i samme år, med ulik dato:** Wenche har bare ett datofelt. **Stopp og flagg**, og be brukeren avklare med regnskapsfører i stedet for å velge én av datoene.
- **Datoen er ikke en faktisk dato** (en plassholder som «settes av brukeren», eller den mangler): stopp og be brukeren fylle inn datoen generalforsamlingen faktisk ble holdt.
- **Datoen ligger utenfor regnskapsåret:** stopp. Wenche avviser den, og den tyder på at feil protokoll er brukt.

## Output 2: sjekkliste

Skriv ut en kort sjekkliste over det du IKKE kunne utlede fra bankeksporten og som brukeren må verifisere manuelt:

- [ ] `foregaaende_aar` stemmer med fjorårets innsendte årsregnskap. Første år i Bodil for et eldre selskap: resultatet er tallene brukeren oppga, og balansen er `aapningsbalanse` med eierpostene.
- [ ] `formuesverdi_aksjer` hentet fra aksjeoppgaven RF-1088S (post 209). Kan ikke utledes fra bankeksporten.
- [ ] `underskudd_til_fremfoering` er «Fremførbart underskudd 01.01» fra «Skattemessig» i `regnskap.md` (år 1: fra fjorårets skattemelding; mangler linjen, se «Fremførbart underskudd»). Underskuddet til fremføring som Wenche beregner, skal være lik «Underskudd til fremføring neste år» i `regnskap.md`.
- [ ] `andre_finansinntekter` og `rentekostnader` stemmer med rentelinjene i bankeksporten (eller årsoppgaven fra banken).
- [ ] `skattekostnad` og `betalbar_skatt` stemmer med hverandre og med Wenches egen beregning. Sier Wenche at skatten er beregnet men ikke ført, mangler linjen i `regnskap.md`.
- [ ] `avsatt_utbytte` stemmer med «Utbytte»-seksjonen i `regnskap.md` og med det protokollen faktisk vedtok.
- [ ] Er det utbetalt utbytte, er `utbytte_vedtaksdato` datoen for vedtaket om det utbetalte utbyttet (normalt generalforsamlingen i `<år-1>/protokoll.md`), og den ligger i regnskapsåret.
- [ ] `avsatt_utbytte` og `utbytte_utbetalt` er ikke forvekslet: den første er årets avsetning per 31.12, den andre er kontanter ut i året. Er fjorårets avsetning betalt i år og et nytt utbytte avsatt, er begge ulik null.
- [ ] `tinginnskudd_ved_stiftelse` stemmer med stiftelsesdokumentene (kun år 1, og bare hvis selskapet ble stiftet ved tinginnskudd). Kan ikke utledes fra bankeksporten: et tinginnskudd går aldri gjennom bankkontoen.
- [ ] Ved salg av eierpost: `gevinst_ved_realisasjon_av_aksjer` eller `tap_ved_realisasjon_av_aksjer` stemmer med «Salg av eierpost» i `regnskap.md`, og ingen del av beløpet står i `andre_finansinntekter`/`andre_finanskostnader`. `andre_aksjer` stemmer med `eierposter` i oppdatert `selskap.yaml`.
- [ ] `eierandel_for_fritaksmetoden` riktig (avgjør om utbytte er fullt skattefritt eller 3 %-beskattet).
- [ ] Eierpostene står på riktig linje: datterselskap (kontroll, normalt over 50 % av stemmene) under `aksjer_i_datterselskap`, resten under `andre_aksjer`. 90 %-grensen gjelder bare fritaksmetoden, ikke denne linjen.
- [ ] Noter fylles i Wenches **Dokumenter-fane**: antall ansatte (normalt 0) og eventuelt lån fra aksjonær som lån til/fra nærstående. Wenche genererer selve notene, Bodil gjør det ikke.
- [ ] Balansen går opp (bekreftes også av valideringen under).
- [ ] Skatteberegningen sett over av regnskapsfører år 1.

## Output 3: valider (valgfritt)

Validering er valgfri. Er `wenche`-kommandoen tilgjengelig lokalt, kjør den og rapporter exit-kode og output til brukeren:

```
wenche valider-aarsregnskap --config <år>/config.yaml
```

- Exit 0 = ingen blokkerende feil. Eventuelle `ADVARSEL`-linjer (f.eks. utbytte uten dekning) skal leses og avklares, men stopper ikke innsending.
- Exit 1 = blokkerende feil (typisk balanse som ikke går opp, eller ugyldig org.nr.). Rett i `regnskap.md`/`config.yaml` og kjør på nytt.

Er ikke `wenche` installert, **ikke be brukeren installere det kun for dette**. Si at `config.yaml` er klar, og at valideringen skjer ved opplasting på wenche.cloud (se «Neste steg»). Vil brukeren likevel validere lokalt først, kan validatoren installeres alene med `pipx install wenche` (krever ikke Maskinporten-oppsett).

## Neste steg

Brukeren sender inn på én av to måter, avhengig av hvilken Wenche de bruker:

- **Hostet ([wenche.cloud](https://wenche.cloud), anbefalt):** brukeren kobler selskapet til Altinn, og under **Tall** klikker **Hent tall fra Bodil** og laster opp `<år>/config.yaml`. Skjemaet forhåndsfylles; brukeren ser over, fyller noter i Dokumenter-fanen, og sender inn.
- **Self-hosted (lokalt):** brukeren kjører `cd <år> && wenche`, som laster `config.yaml` fra mappen, og sender inn derfra.

**Personvern:** `config.yaml` inneholder fødselsnummer. Lokalt forlater det aldri maskinen; ved opplasting til wenche.cloud sendes det dit (behandles kun i økten, ikke lagret i database). Nevn dette hvis brukeren er usikker på hvilken vei de skal velge.
