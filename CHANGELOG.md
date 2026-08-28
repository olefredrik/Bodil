# Endringslogg

Alle merkbare endringer i Bodil dokumenteres her. Formatet følger løst
[Keep a Changelog](https://keepachangelog.com/), og versjonene følger
[SemVer](https://semver.org/) tilpasset et template-prosjekt:

- **MAJOR** — den låste bokføringsmodellen endres, eller Wenche-kompatibilitet brytes
- **MINOR** — ny skill, ny håndtert hendelse, eller støtte for en ny Wenche-versjon
- **PATCH** — ordlyd, dokumentasjon, feilretting i en skill

Hver oppføring som rører grensesnittet mot Wenche oppgir hvilken Wenche-versjon
Bodil er testet mot. Den versjonen er også pinnet i CI
([wenche-kompatibilitet.yml](.github/workflows/wenche-kompatibilitet.yml)).

## [0.6.0]

- **Utbetalt utbytte får riktig kode hos Skatteetaten.** Wenche 1.4.0 har fått avklart
  at samleposten «andre negative endringer i egenkapital» ikke skal brukes ved utdeling
  av utbytte, og koder nå utbetalingen som `tilleggsutbytte`: utdeling i løpet av året
  basert på sist godkjente årsregnskap, som er nøyaktig det Bodils modell produserer.
  Golden-fixturet gikk fra `annenNegativEndringIEgenkapital` til `tilleggsutbytte` uten
  at en eneste linje i Bodils output endret seg. Alle som har delt ut utbytte fra et
  Bodil-ført regnskap har sendt inn med den avviste samleposten; det retter seg ved å
  bumpe pinnet Wenche, ingenting annet må gjøres.
- **Selskap stiftet ved tinginnskudd kan nå rapportere det.** Skytes aksjer i et annet
  selskap inn som aksjekapital, som er en vanlig måte å etablere en holdingstruktur på,
  rapporterte egenkapitalavstemmingen hele stiftelsesinnskuddet som kontantinnskudd i
  første regnskapsår. Det nye, valgfrie feltet `tinginnskudd_ved_stiftelse` i
  `selskap.yaml` oppgir tingdelen, og kontantinnskuddet blir resten. Feltet kan ikke
  utledes fra bankeksporten, siden et tinginnskudd aldri går gjennom bankkontoen, så
  `wenche-config` fører det opp i sjekklisten over manuelle poster. Det gjelder bare
  første regnskapsår; senere år ignorerer Wenche det med en advarsel.
- **Gaten dekker nå tre former** Bodil kan produsere: nytt fixture
  `tests/fixtures/config.tinginnskudd.yaml` for et delt stiftelsesinnskudd (25 000 som
  aksjer, 5 000 som penger), som tvinger både `tinginnskudd` og `kontantinnskudd` ut i
  avstemmingen.
- Pinnet Wenche bumpet fra 1.3.1 til 1.5.1. Ingen feltnavn Bodil bruker er fjernet eller
  døpt om. Wenche 1.5.0 la til `avsatt_utbytte` for utbytte som avsettes i regnskapet og
  utbetales året etter; Bodil bruker det ikke i denne versjonen, siden den låste modellen
  fører utbytte når pengene forlater konto.

**Testet mot Wenche ≥ 1.5.1.**

## [0.5.0]

- **Skattekostnad er nå en del av den låste modellen.** Bodil regnet årsresultatet
  som utbytte minus driftskostnader, altså implisitt skattekostnad 0. Det stemmer
  for et hvilende år, men et år med mottatt utbytte og eierandel under 90 % har en
  reell skattepliktig inntekt gjennom 3 %-sjablonen i fritaksmetoden (sktl. § 2-38
  sjette ledd), og regnskapsloven § 6-1 krever skattekostnaden som egen linje før
  årsresultatet. Årsresultatet ble dermed rapportert for høyt, og Wenche varslet
  «skatten er beregnet, men ikke ført». `bokforing` regner nå skatten etter samme
  regel som Wenche (skattepliktig del av utbyttet minus driftskostnader, minus
  fremført underskudd, ganget med 22 %), og fører `betalbar_skatt` som motpost i
  balansen. Golden-fixturet gikk fra ført 0 mot beregnet 55 kr til avvik 0.
- **Betaling av skatt har fått sin egen rad i modellen.** Uten den ville
  innbetalingen til Skatteetaten året etter blitt klassifisert som driftskostnad og
  dermed kostnadsført to ganger. Den reduserer nå betalbar skatt.
- **`regnskap.md` har en ny «Skattemessig»-seksjon** med skattepliktig inntekt,
  anvendt fremført underskudd og underskudd til fremføring neste år. Den er input
  til neste års bokføring og til `underskudd_til_fremfoering` i `wenche-config`,
  som tidligere måtte hentes manuelt fra RF-1028 hvert år.
- **`selskap.stiftelsesdato` tas nå med når den er kjent.** Uten den oppgir
  aksjonærregisteroppgaven 1. januar som stiftelsestidspunkt for de nyutstedte
  aksjene. Feltet er lagt til i `selskap.example.yaml` (hentes fra Enhetsregisteret).
- **Forlenget første regnskapsår støttes** via `regnskapsstart` og `regnskapsslutt`
  i `wenche-config`. Et selskap stiftet sent på året kan la første regnskapsår løpe
  i inntil 18 måneder (rskl. § 1-7 andre ledd); Bodil oppgav tidligere hele
  kalenderåret uansett.
- **Kompatibilitetsgaten dekker nå begge formene** Bodil kan produsere: nytt fixture
  `tests/fixtures/config.foerste-aar.yaml` for det forlengede første regnskapsåret,
  og både validering og feltnavn-lint kjører over alle fixtures i `tests/fixtures/`
  i stedet for bare golden-fixturet.
- Pinnet Wenche bumpet fra 0.31.2 til 1.3.1. Ingen feltnavn Bodil bruker er fjernet
  eller døpt om i 1.x; hele endringen over handler om felt Bodil ikke utnyttet.

**Testet mot Wenche ≥ 1.3.1.**

## [0.4.2]

- CI-workflowene (`docs.yml`, `wenche-kompatibilitet.yml`) kjører nå kun i
  Bodils eget repo (`if: github.repository == 'olefredrik/Bodil'`). Template-
  kopier som har hentet inn `.github/` får dem dermed hoppet over i stedet for å
  feile med e-postvarsel ved hver push.
- Oppdateringsoppskriften (`docs/oppdatere.md`) henter ikke lenger inn `.github`,
  og forklarer hvorfor Bodils CI ikke hører hjemme i en regnskapskopi (+ hvordan
  rydde hvis den allerede er hentet inn). Eksempelversjonen er oppdatert.

**Testet mot Wenche ≥ 0.31.2.**

## [0.4.1]

- Tydeligere veiledning for Folio-integrasjonen: `folio-import`-skillen og docs
  forklarer nå steg for steg hvordan API-nøkkelen lages (Lesetilgang på
  app.folio.no/til/api-tilgang) og legges i en `.env`-fil, og feilmeldingen ved
  manglende nøkkel er gjort handlingsrettet.
- Språk: «lese-only» erstattet med «kun lesing» i skill, skript og docs.

**Testet mot Wenche ≥ 0.31.2.**

## [0.4.0]

- Hostet Wenche ([wenche.cloud](https://wenche.cloud)) er nå den anbefalte
  innsendingsveien i dokumentasjon og skills: brukeren laster opp `config.yaml`
  via **Tall → Hent tall fra Bodil**, uten å installere noe. Self-hosted lokalt
  er fortsatt et likeverdig alternativ.
- `wenche-config` krever ikke lenger at Wenche er installert. Lokal validering
  (`wenche valider-aarsregnskap`) kjøres hvis kommandoen finnes, ellers skjer
  valideringen ved opplasting på wenche.cloud. Senker terskelen for web-brukere.
- Personvern-note: `config.yaml` inneholder fødselsnummer, som forlater maskinen
  ved opplasting til wenche.cloud (behandles kun i økten, ikke lagret).
- Release-badgen i README er nå statisk (`badge/release-vX.Y.Z`) i stedet for
  `github/v/release`, som intermitterende feilet med «Unable to select next
  GitHub token from pool» fra shields.io.
- Forenklet release-prosess: versjon og badge navngis nå i selve feature-PR-ene
  (entry under `## [X.Y.Z]`), så `/release` er bare en tag + GitHub Release,
  ingen egen versjons-bump-PR.

**Testet mot Wenche ≥ 0.31.2.**

## [0.3.0]

- Verifisert kompatibilitet med Wenche 0.31.2 og bumpet pinnet versjon fra 0.24.0.
  Feltnavnene i `config.yaml` og kommandoen `wenche valider-aarsregnskap` er
  uendret i 0.31.2; golden-fixturet validerer fortsatt grønt, så ingen
  skill-endring var nødvendig.
- Ny valgfri skill `folio-import`: henter et regnskapsårs transaksjoner fra
  Folio (api.folio.no/v2, lese-only) og skriver `<år>/bankeksport.csv`. Erstatter
  kun det manuelle CSV-nedlastingssteget; alt nedstrøms er uendret. Kun stdlib,
  kun GET-kall, aldri `/payments`, API-nøkkel fra `.env`.
- `scripts/sync-from-bodil`: synker verktøy-allowlisten (ikke data) til en privat
  kopi av malen, pinnet til en Bodil-tag, med en deny-list som nekter å røre
  `selskap.yaml`, `*/config.yaml`, `*/bankeksport.csv` og `*/bilag/`.
- Folio-importørens rene logikk dekkes av `tests/test_folio_import.py`, som kjører
  i CI-gaten sammen med Wenche-valideringen og feltnavn-linten.
- Kompatibilitets-gaten kjører nå også på push til main, så Actions-badgen i
  README reflekterer mains faktiske Wenche-kompatibilitet.
- README: badges (release, lisens, status, CI, Claude Code) og tydeliggjort at
  Bodil forutsetter tilgang til Claude (den eneste kostnaden; verktøyene er gratis).

**Testet mot Wenche ≥ 0.31.2.**

## [0.2.0]

- `/release` automatiserer nå tagging og release notes: henter noten fra
  CHANGELOG og kjører tag + GitHub Release etter én bekreftelse.
- CI feiler nå hvis `WENCHE_PINNET` ikke matcher «Testet mot Wenche ≥ …» i
  CHANGELOG, så de to kan ikke drifte fra hverandre.
- CLAUDE.md-regel: hver oppførselsendrende PR oppdaterer `[Ikke utgitt]`.
- Den ukentlige kjøringen mot nyeste Wenche oppretter nå en GitHub-issue ved
  brudd (med duplikat-vern), i stedet for bare en passiv annotering.

**Testet mot Wenche ≥ 0.24.0.**

## [0.1.0]

Første versjonerte utgave.

- Tre skills for bokføring, protokoll og Wenche-config for passive holdingselskaper.
- Automatisk kompatibilitetstest mot Wenche: golden-fixture valideres med
  `wenche valider-aarsregnskap`, og en feltnavn-lint sjekker at Bodils feltnavn
  finnes i Wenches datamodell. Kjører som PR-gate (pinnet) og ukentlig (nyeste).
- Rettet feltnavn i wenche-config: `eierandel_datterselskap` →
  `eierandel_for_fritaksmetoden` (Wenche leste aldri det gamle navnet, så
  eierandel under 90 % ble feilaktig behandlet som fullt skattefritt utbytte).

**Testet mot Wenche ≥ 0.24.0.**

[0.6.0]: https://github.com/olefredrik/Bodil/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/olefredrik/Bodil/compare/v0.4.2...v0.5.0
[0.4.2]: https://github.com/olefredrik/Bodil/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/olefredrik/Bodil/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/olefredrik/Bodil/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/olefredrik/Bodil/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/olefredrik/Bodil/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/olefredrik/Bodil/releases/tag/v0.1.0
