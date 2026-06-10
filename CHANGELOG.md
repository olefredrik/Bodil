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

[0.4.0]: https://github.com/olefredrik/Bodil/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/olefredrik/Bodil/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/olefredrik/Bodil/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/olefredrik/Bodil/releases/tag/v0.1.0
