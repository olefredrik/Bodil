# Oppdatere Bodil

Lagde du din egen kopi med «Use this template» og har ført regnskap i den en stund? Da vil du fra tid til annen hente inn nyere Bodil-verktøy, for eksempel [Folio-integrasjonen](folio.md), oppdaterte skills eller en ny Wenche-kompatibilitet.

En template-kopi deler **ikke** git-historikk med Bodil, så du kan ikke `git pull` fra malen. I stedet legger du Bodil til som en ekstra remote og henter inn kun verktøy-stiene ved den versjonen du vil ha. Dette rører aldri regnskapsdataene dine.

!!! danger "Rør aldri data"
    Oppskriften under lister kun **verktøy-stier**. Ta aldri med `selskap.yaml`, årsmappene (`2025/`, `2026/` …) eller `.env` i kommandoen, det er der tallene dine bor. Kjør `git status` og se over før du committer.

## 1. Legg Bodil til som remote (én gang)

```bash
git remote add bodil https://github.com/olefredrik/Bodil.git
```

## 2. Hent inn verktøyet ved ønsket versjon

Pinn til en utgitt versjon (se [utgivelsene](https://github.com/olefredrik/Bodil/releases)) for et forutsigbart resultat:

```bash
git fetch bodil --tags

git checkout v0.4.2 -- \
  .claude scripts tests \
  CLAUDE.md .gitignore selskap.example.yaml bankeksport.example.csv

git status                       # bekreft at kun verktøy er endret, ingen data
git commit -m "chore: oppdater Bodil-verktøy til v0.4.2"
```

`git checkout <tag> -- <stier>` kopierer akkurat de stiene fra Bodil-versjonen inn i kopien din og legger dem klar til commit. Stier som ikke står i listen (som `selskap.yaml` og årsmappene) berøres ikke.

!!! warning "Ikke hent inn `.github/`"
    Mappen `.github/` inneholder Bodils egne CI-workflows (dokumentasjonsbygg og Wenche-kompatibilitet). De er laget for å **utvikle** Bodil, ikke for å **bruke** det, og vil feile i regnskapskopien din (mangler `mkdocs.yml`, GitHub Pages osv.) — med feil-e-post ved hver push. Derfor står `.github` bevisst ikke i listen over. Hentet du den inn i en tidligere oppdatering? Slett `.github/workflows/` og commit det. (Fra v0.4.2 er workflowene dessuten guardet til kun å kjøre i Bodils eget repo, så nyere kopier rammes ikke uansett.)

!!! note "Vil du også ha docs-siten i din private kopi?"
    Listen over er det funksjonelle verktøyet. Vil du i tillegg ha dokumentasjonen og README med, legg til `README.md CHANGELOG.md docs mkdocs.yml` i samme kommando. Det er valgfritt og rent kosmetisk for en privat regnskapskopi.

## Godt å vite

- **Egne endringer overskrives.** Har du tilpasset en verktøyfil (f.eks. `CLAUDE.md` eller `.gitignore`), overskriver oppdateringen den. Se over `git diff --staged` før du committer hvis du er usikker.
- **Slettede filer henger igjen.** Har en nyere Bodil fjernet en verktøyfil, blir den ikke fjernet i kopien din automatisk; `git checkout` legger bare til og oppdaterer. Det er sjelden et problem.
- **Sjekk CHANGELOG.** [CHANGELOG](https://github.com/olefredrik/Bodil/blob/main/CHANGELOG.md) forteller hva som er nytt i hver versjon, og hvilken Wenche-versjon den er testet mot.
