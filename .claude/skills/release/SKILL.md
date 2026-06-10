---
name: release
description: Publiser en ny versjon av Bodil-verktøyet. Verifiserer kompatibilitet mot Wenche, henter release-noten automatisk fra CHANGELOG-seksjonen som allerede er navngitt i PR-ene, og tagger + oppretter GitHub Release etter én bekreftelse. Ingen PyPI. Bruk etter at en PR er merget til main.
---

# /release — Publiser ny versjon av Bodil

Bodil distribueres ikke som en pakke; en release er en **git-tag + GitHub Release**
som markerer en verifisert tilstand av verktøyet (skills + kompatibilitet med en
gitt Wenche-versjon). Taggen *er* versjonen, det finnes ingen versjonsfil.

Versjonen navngis i selve feature-PR-ene (se «Versjonering og CHANGELOG» i
`CLAUDE.md`): hver oppførsels-PR skriver entryen sin under en `## [X.Y.Z]`-
overskrift, og PR-en som oppretter overskriften legger til «Testet mot Wenche»-
linjen, compare/tag-lenkene og bumper release-badgen i README. **Derfor er
release bare en tag:** når du kommer hit er CHANGELOG og badge allerede klare på
main, og det eneste som gjenstår er å tagge og publisere. Ingen egen prep-PR.

Du **utfører** tagging og release selv (via `git` og `gh`), men tag + release er
utadrettet på et offentlig repo, så du gjør det først **etter én eksplisitt
bekreftelse** der du viser hva som publiseres. Aldri uten den bekreftelsen.

## 1. Forutsetninger

- `git branch --show-current`. Release skjer fra `main`. Bytt til main og
  `git pull` hvis du står på en feature-branch (PR-en skal være merget først).
- `git fetch && git status`. Bekreft at main er à jour med `origin/main` og at
  arbeidstreet er rent. Er det umergede endringer: stopp og avklar.

## 2. Les versjonen CHANGELOG navngir

Den øverste `## [X.Y.Z]`-seksjonen i `CHANGELOG.md` som ennå ikke er tagget, er
versjonen du skal slippe. Den ble valgt og navngitt i feature-PR-ene. Les den,
og la brukeren bekrefte at det er denne som skal ut.

Til kontroll av at nivået er riktig (SemVer, tilpasset template-prosjektet):

- **MAJOR** — den låste bokføringsmodellen endret seg, eller Wenche-kompatibilitet brytes
- **MINOR** — ny skill, ny håndtert hendelse, eller støtte for en ny Wenche-versjon
- **PATCH** — ordlyd, dokumentasjon, feilretting

> Mens avviket om rentebærende aksjonærlån er uavklart, hold deg på `0.x`.

## 3. Verifiser Wenche-kompatibilitet

Kjernen i en Bodil-release. En release uten grønn kompatibilitetstest er ikke gyldig.

- Les `env.WENCHE_PINNET` i `.github/workflows/wenche-kompatibilitet.yml` og
  «Testet mot Wenche ≥ …»-linjen i `[X.Y.Z]`-seksjonen. **De må matche**, ellers stopp.
- Bekreft at gaten er grønn på main HEAD (`gh run list --branch main --workflow wenche-kompatibilitet.yml --limit 1`).
- Kjør gjerne lokalt hvis Wenche er installert; begge må gi exit 0:
  - `wenche valider-aarsregnskap --config tests/fixtures/config.golden.yaml`
  - `python tests/check_field_names.py`

## 4. Bekreft at alt er klart for tag

Siden navngivingen skjer i PR-ene, skal dette allerede stemme på main. Sjekk:

- CHANGELOG har en `## [X.Y.Z]`-seksjon med innhold og «Testet mot Wenche»-linjen.
- Release-badgen i `README.md` er `img.shields.io/badge/release-vX.Y.Z-blue`.
- Lenkeblokken nederst i CHANGELOG har `[X.Y.Z]: …/compare/vFORRIGE...vX.Y.Z`.

**Faller noe ut** (en PR glemte å navngi versjonen eller bumpe badgen): rett det
i en liten PR først (`docs: klargjør vX.Y.Z`), siden rulesettet krever PR til
main. Merg den, og fortsett. Dette er unntaket, ikke regelen.

## 5. Bekreft og publiser

Hent noten og vis et sammendrag:

```bash
# Hent release-noten for X.Y.Z fra CHANGELOG (stopper ved neste seksjon/lenkeblokk)
awk '/^## \[X\.Y\.Z\]/{f=1; next} f&&(/^## \[/||/^\[.*\]:/){exit} f{print}' CHANGELOG.md
```

Vis brukeren: versjonsnummer, hvilken commit taggen settes på (`git log -1 --oneline`),
noten over, og at release-en blir **offentlig**. Spør om å gå videre.

Etter ja:

```bash
git checkout main && git pull
git tag -a vX.Y.Z -m "vX.Y.Z" && git push origin vX.Y.Z
gh release create vX.Y.Z --title "vX.Y.Z" \
  --notes-file <(awk '/^## \[X\.Y\.Z\]/{f=1; next} f&&(/^## \[/||/^\[.*\]:/){exit} f{print}' CHANGELOG.md)
```

Bekreft at taggen er på remote (`git ls-remote --tags origin vX.Y.Z`) og at
release-en ble opprettet (lenken `gh` returnerer).

## 6. Oppdater minnet

Oppdater `bodil-versjon`-minnet med ny utgitt versjon og hvilken Wenche-versjon
den er testet mot.

## Viktige prinsipper

- **Aldri** tagg eller opprett release uten brukerens bekreftelse i steg 5.
- En release uten grønn kompatibilitetstest er ikke gyldig. Stopp hvis testen feiler.
- Navngiving (CHANGELOG + badge) skjer i feature-PR-ene, ikke her. Release er en
  ren tag. Tagger er ikke beskyttet av branch-rulesettet, så de settes direkte.
- Ingen PyPI, ingen build. Taggen markerer en verifisert tilstand.
