---
name: release
description: Publiser en ny versjon av Bodil-verktøyet. Verifiserer kompatibilitet mot Wenche, henter release-noten automatisk fra CHANGELOG, og tagger + oppretter GitHub Release etter én bekreftelse. Håndterer CHANGELOG-bump via PR når rulesettet krever det. Ingen PyPI. Bruk etter at en PR er merget til main.
---

# /release — Publiser ny versjon av Bodil

Bodil distribueres ikke som en pakke; en release er en **git-tag + GitHub Release**
som markerer en verifisert tilstand av verktøyet (skills + kompatibilitet med en
gitt Wenche-versjon). Taggen *er* versjonen, det finnes ingen versjonsfil.

Du **utfører** tagging og release selv (via `git` og `gh`), men tag + release er
utadrettet på et offentlig repo, så du gjør det først **etter én eksplisitt
bekreftelse** der du viser hva som publiseres. Aldri uten den bekreftelsen.

## 1. Forutsetninger

- `git branch --show-current`. Release skjer fra `main`. Bytt til main og
  `git pull` hvis du står på en feature-branch (PR-en skal være merget først).
- `git fetch && git status`. Bekreft at main er à jour med `origin/main` og at
  arbeidstreet er rent. Er det umergede endringer: stopp og avklar.

## 2. Bestem versjonsnummeret

Dette er det eneste steget som alltid krever brukeren: versjonsnummeret er en
skjønnsvurdering. Les `## [Ikke utgitt]` i `CHANGELOG.md`, foreslå bump og
begrunn kort. La brukeren bekrefte før du går videre.

- **MAJOR** — den låste bokføringsmodellen endret seg, eller Wenche-kompatibilitet brytes
- **MINOR** — ny skill, ny håndtert hendelse, eller støtte for en ny Wenche-versjon
- **PATCH** — ordlyd, dokumentasjon, feilretting

> Mens avviket om rentebærende aksjonærlån er uavklart, hold deg på `0.x`.

## 3. Verifiser Wenche-kompatibilitet

Kjernen i en Bodil-release. En release uten grønn kompatibilitetstest er ikke gyldig.

- Les `env.WENCHE_PINNET` i `.github/workflows/wenche-kompatibilitet.yml` og
  «Testet mot Wenche ≥ …»-linjen i `CHANGELOG.md`. **De må matche**, ellers stopp.
- Kjør lokalt hvis Wenche er installert; begge må gi exit 0:
  - `wenche valider-aarsregnskap --config tests/fixtures/config.golden.yaml`
  - `python tests/check_field_names.py`

## 4. Sørg for at CHANGELOG navngir versjonen

Release-noten hentes automatisk fra CHANGELOG-seksjonen for versjonen, så den må
finnes som `## [X.Y.Z]` før du tagger.

- **Navngir CHANGELOG allerede `## [X.Y.Z]`** (intet uutgitt innhold igjen):
  ingenting å gjøre, gå videre.
- **Ligger innholdet fortsatt under `## [Ikke utgitt]`:** det må navngis i en
  PR, fordi rulesettet krever PR til main. Lag en release-prep-PR:
  1. Ny branch, f.eks. `release/vX.Y.Z`.
  2. Gi `## [Ikke utgitt]` versjonsnummeret, legg til en ny tom `## [Ikke utgitt]`
     over, oppdater `compare`-lenken og legg til en `releases/tag`-lenke nederst.
  3. Bekreft at seksjonen har «Testet mot Wenche ≥ …»-linjen.
  4. Commit (`docs: klargjør CHANGELOG for vX.Y.Z`), push, og **stopp her** med
     PR-tittel/beskrivelse til brukeren. Be brukeren merge og kjøre `/release`
     på nytt. Du kan ikke tagge før navngivingen er på main.

## 5. Bekreft og publiser

Når CHANGELOG navngir versjonen på main, hent noten og vis et sammendrag:

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
- CHANGELOG-navngiving går alltid via PR (rulesettet beskytter main). Tag og
  release gjør du direkte, siden tagger ikke beskyttes av branch-rulesettet.
- Ingen PyPI, ingen build. Taggen markerer en verifisert tilstand.
