---
name: release
description: Publiser en ny versjon av Bodil-verktøyet. Verifiserer at vi er på main med siste endringer, at Wenche-kompatibilitetslinjen i CHANGELOG matcher den pinnede versjonen i CI, oppdaterer CHANGELOG, og presenterer kommandoene for å tagge og lage en GitHub Release. Ingen PyPI. Bruk etter at en PR er merget til main.
---

# /release — Publiser ny versjon av Bodil

Bodil distribueres ikke som en pakke; en release er en **git-tag + GitHub Release**
som markerer en verifisert tilstand av verktøyet (skills + kompatibilitet med en
gitt Wenche-versjon). Taggen *er* versjonen, det finnes ingen versjonsfil.

Følg stegene i rekkefølge. Du **tagger ikke selv** og lager ikke release-en
automatisk; du presenterer kommandoene brukeren kjører.

## 1. Forutsetninger

- Kjør `git branch --show-current`. Release skjer fra `main`. Står du på en
  feature-branch: stopp og be brukeren merge PR-en først.
- Kjør `git fetch && git status`. Bekreft at main er à jour med `origin/main`
  og at arbeidstreet er rent. Er det umergede endringer: stopp og avklar.

## 2. Bestem versjonsnummeret

Les `## [Ikke utgitt]` i `CHANGELOG.md` og avgjør bump etter SemVer slik den er
definert øverst i CHANGELOG:

- **MAJOR** — den låste bokføringsmodellen endret seg, eller Wenche-kompatibilitet brytes
- **MINOR** — ny skill, ny håndtert hendelse, eller støtte for en ny Wenche-versjon
- **PATCH** — ordlyd, dokumentasjon, feilretting

Foreslå versjonsnummeret og begrunn bumpen kort. La brukeren bekrefte før du går videre.

> Mens avviket om rentebærende aksjonærlån er uavklart, hold deg på `0.x`.

## 3. Verifiser Wenche-kompatibilitet

Dette er kjernen i en Bodil-release. Sjekk at påstanden om kompatibilitet faktisk stemmer:

- Les `env.WENCHE_PINNET` i `.github/workflows/wenche-kompatibilitet.yml`.
- Les «Testet mot Wenche ≥ …»-linjen i `CHANGELOG.md`.
- **De to må matche.** Gjør de ikke det, stopp og avklar hvilken som er riktig før release.
- Kjør kompatibilitetstesten lokalt hvis Wenche er installert:
  `wenche valider-aarsregnskap --config tests/fixtures/config.golden.yaml` og
  `python tests/check_field_names.py`. Begge må gi exit 0.

## 4. Oppdater CHANGELOG

- Gi `## [Ikke utgitt]`-seksjonen det nye versjonsnummeret og legg til en ny, tom
  `## [Ikke utgitt]` over.
- Oppdater lenkene nederst (`compare`-lenken og en ny `releases/tag`-lenke).
- Bekreft at versjonsseksjonen oppgir hvilken Wenche-versjon den er testet mot.
- Commit dette med Conventional Commits, f.eks. `docs: klargjør CHANGELOG for vX.Y.Z`,
  og push til main (eller via PR hvis ruleset krever det).

## 5. Presenter tag- og release-kommandoene

Gi brukeren kommandoene å kjøre selv. Inkluder alltid checkout og pull først, så
taggen settes på riktig commit:

```bash
git checkout main && git pull
git tag vX.Y.Z && git push origin vX.Y.Z
gh release create vX.Y.Z --title "vX.Y.Z" --notes-file <(sed -n '/## \[X.Y.Z\]/,/## \[/p' CHANGELOG.md)
```

Tilpass `vX.Y.Z`. Release-noten hentes fra CHANGELOG-seksjonen for versjonen.
Alternativt kan brukeren lime inn noten manuelt i GitHubs release-grensesnitt.

## 6. Oppdater minnet

Noter den nye versjonen og hvilken Wenche-versjon den er kompatibel med i
prosjektminnet, så det er lett å finne neste gang.

## Viktige prinsipper

- **Ikke** push tagger eller opprett release-en automatisk uten brukerens godkjenning.
- En release uten en grønn kompatibilitetstest er ikke gyldig. Stopp hvis testen feiler.
- Ingen PyPI, ingen build. Bodil er et template-repo; taggen markerer en verifisert tilstand.
