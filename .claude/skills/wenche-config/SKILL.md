---
name: wenche-config
description: Generer en config.yaml for Wenche fra et ferdig regnskap. Leser <år>/regnskap.md og stamdata, mapper mot Wenches eksakte feltnavn, skriver <år>/config.yaml, lager en sjekkliste over manuell verifisering, og kjører wenche valider-aarsregnskap. Bruk som siste steg før innsending.
---

# Skill: wenche-config

Mapper et ferdig regnskap til en `config.yaml` som Wenche konsumerer, og selv-verifiserer med Wenches egen validering. Du sender ingenting, det gjør brukeren i Wenche etterpå.

## Input

- `<år>/regnskap.md` (fra bokforing): alle tall til resultatregnskap og balanse, og fjorårets sammenligningstall.
- `selskap.yaml`: selskapsopplysninger og aksjonærer (med fødselsnummer), eierposter.

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
  kontakt_epost: "<e-post>"          # påkrevd for aksjonærregisteroppgave

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
    andre_finansinntekter: 0
    rentekostnader: 0
    andre_finanskostnader: 0
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

foregaaende_aar:                       # fjorårets tall fra regnskap.md (sammenligningstall, rskl. § 6-6)
  resultatregnskap: { ... }            # samme struktur som over
  balanse: { ... }                     # utelat hele seksjonen hvis selskapet ble stiftet i år

skattemelding:
  underskudd_til_fremfoering: <fra «Skattemessig» i regnskap.md, ellers fjorårets RF-1028>
  anvend_fritaksmetoden: true          # holdingselskap som eier aksjer
  eierandel_for_fritaksmetoden: <prosent>   # ≥ 90 % gir fullt skattefritt utbytte; < 90 % gir 3 % sjablonbeskatning
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
```

## Output 2: sjekkliste

Skriv ut en kort sjekkliste over det du IKKE kunne utlede fra bankeksporten og som brukeren må verifisere manuelt:

- [ ] `formuesverdi_aksjer` hentet fra aksjeoppgaven RF-1088S (post 209). Kan ikke utledes fra bankeksporten.
- [ ] `underskudd_til_fremfoering` stemmer med «Skattemessig» i `regnskap.md` (år 1: hentet fra fjorårets RF-1028).
- [ ] `skattekostnad` og `betalbar_skatt` stemmer med hverandre og med Wenches egen beregning. Sier Wenche at skatten er beregnet men ikke ført, mangler linjen i `regnskap.md`.
- [ ] `avsatt_utbytte` stemmer med «Utbytte»-seksjonen i `regnskap.md` og med det protokollen faktisk vedtok.
- [ ] `avsatt_utbytte` og `utbytte_utbetalt` er ikke forvekslet: den første er årets avsetning per 31.12, den andre er kontanter ut i året. Er fjorårets avsetning betalt i år og et nytt utbytte avsatt, er begge ulik null.
- [ ] `tinginnskudd_ved_stiftelse` stemmer med stiftelsesdokumentene (kun år 1, og bare hvis selskapet ble stiftet ved tinginnskudd). Kan ikke utledes fra bankeksporten: et tinginnskudd går aldri gjennom bankkontoen.
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
