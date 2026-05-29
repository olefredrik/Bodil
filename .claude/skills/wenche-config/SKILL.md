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
  aksjekapital: <NOK>
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

balanse:
  eiendeler:
    anleggsmidler:
      aksjer_i_datterselskap: 0       # eierandel ≥ 90 % hører hjemme her; ellers andre_aksjer
      andre_aksjer: <sum kostpris eierposter>
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
      skyldige_offentlige_avgifter: 0
      annen_kortsiktig_gjeld: 0

foregaaende_aar:                       # fjorårets tall fra regnskap.md (sammenligningstall, rskl. § 6-6)
  resultatregnskap: { ... }            # samme struktur som over
  balanse: { ... }                     # utelat hele seksjonen hvis selskapet ble stiftet i år

skattemelding:
  underskudd_til_fremfoering: <fra fjorårets skattemelding, RF-1028>
  anvend_fritaksmetoden: true          # holdingselskap som eier aksjer
  eierandel_datterselskap: <prosent>   # ≥ 90 % gir fullt skattefritt utbytte; < 90 % gir 3 % sjablonbeskatning
  boersnotert: false
  formuesverdi_aksjer: <RF-1088S post 209, MÅ fylles inn manuelt>

aksjonaerer:
  - navn: "<navn>"
    fodselsnummer: "<11 siffer>"
    antall_aksjer: <n>
    aksjeklasse: "ordinære"
    utbytte_utbetalt: <fra regnskap.md>
    innbetalt_kapital_per_aksje: <aksjekapital / antall aksjer>
```

## Output 2: sjekkliste

Skriv ut en kort sjekkliste over det du IKKE kunne utlede fra bankeksporten og som brukeren må verifisere manuelt:

- [ ] `formuesverdi_aksjer` hentet fra aksjeoppgaven RF-1088S (post 209). Kan ikke utledes fra bankeksporten.
- [ ] `underskudd_til_fremfoering` hentet fra fjorårets skattemelding.
- [ ] `eierandel_datterselskap` riktig (avgjør om utbytte er fullt skattefritt eller 3 %-beskattet).
- [ ] Noter fylles i Wenches **Dokumenter-fane**: antall ansatte (normalt 0) og eventuelt lån fra aksjonær som lån til/fra nærstående. Wenche genererer selve notene, companion gjør det ikke.
- [ ] Balansen går opp (bekreftes også av valideringen under).
- [ ] Skatteberegningen sett over av regnskapsfører år 1.

## Output 3: kjør Wenches validering

Kjør, og rapporter exit-kode og output til brukeren:

```
wenche valider-aarsregnskap --config <år>/config.yaml
```

- Exit 0 = ingen blokkerende feil. Eventuelle `ADVARSEL`-linjer (f.eks. utbytte uten dekning) skal leses og avklares, men stopper ikke innsending.
- Exit 1 = blokkerende feil (typisk balanse som ikke går opp, eller ugyldig org.nr.). Rett i `regnskap.md`/`config.yaml` og kjør på nytt.

Krever at Wenche (≥ 0.23.0) er installert. Mangler kommandoen, be brukeren installere/oppdatere Wenche (`pipx install wenche` eller `pipx upgrade wenche`).

## Neste steg

Når valideringen er grønn: brukeren åpner Wenche (`wenche`), laster `<år>/config.yaml`, fyller noter i Dokumenter-fanen, kontrollerer, og sender inn.
