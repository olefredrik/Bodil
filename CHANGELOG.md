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

## [Ikke utgitt]

- CI feiler nå hvis `WENCHE_PINNET` ikke matcher «Testet mot Wenche ≥ …» i
  CHANGELOG, så de to kan ikke drifte fra hverandre.
- CLAUDE.md-regel: hver oppførselsendrende PR oppdaterer `[Ikke utgitt]`.

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

[Ikke utgitt]: https://github.com/olefredrik/Bodil/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/olefredrik/Bodil/releases/tag/v0.1.0
