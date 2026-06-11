# Bodil

[![Release](https://img.shields.io/badge/release-v0.4.2-blue)](https://github.com/olefredrik/Bodil/releases)
[![Lisens: MIT](https://img.shields.io/badge/lisens-MIT-blue)](LICENSE)
[![Status: aktiv](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Wenche-kompatibilitet](https://github.com/olefredrik/Bodil/actions/workflows/wenche-kompatibilitet.yml/badge.svg)](https://github.com/olefredrik/Bodil/actions/workflows/wenche-kompatibilitet.yml)
[![Dokumentasjon](https://img.shields.io/badge/docs-olefredrik.github.io%2FBodil-teal)](https://olefredrik.github.io/Bodil/)
[![Drevet av Claude Code](https://img.shields.io/badge/drevet%20av-Claude%20Code-d97757)](https://claude.com/claude-code)

**Regnskap for holdingselskap, følgeverktøy til [Wenche](https://github.com/olefredrik/Wenche).**

Bodil fører regnskap «i git» for et **passivt holdingselskap**, drevet av [Claude Code](https://claude.com/claude-code). Repoet gjør om en bankeksport (CSV) til et lesbart regnskap, en generalforsamlingsprotokoll og en ferdig `config.yaml` som Wenche sender inn til myndighetene.

Bodil og Wenche er to verktøy med hver sin jobb: Bodil fører bøkene, Wenche sender inn. Wenche kan brukes alene hvis du allerede har tallene; trenger du å føre regnskapet først, kobler du på Bodil. Begge er gratis og åpen kildekode. Den eneste kostnaden er at Bodil kjøres av Claude Code og derfor forutsetter tilgang til Claude.

> **Bodil er et hjelpeverktøy, ikke en regnskapsfører.** Genererte dokumenter er utkast du må kontrollere før innsending. Driftsselskaper er utenfor scope. Se [Ansvar](https://olefredrik.github.io/Bodil/ansvar/).

## 📖 Dokumentasjon

Full dokumentasjon: **[olefredrik.github.io/Bodil](https://olefredrik.github.io/Bodil/)**

- [Hva er Bodil?](https://olefredrik.github.io/Bodil/)
- [Bodil og Wenche](https://olefredrik.github.io/Bodil/bodil-og-wenche/)
- [Kom i gang](https://olefredrik.github.io/Bodil/kom-i-gang/)
- [Bruk (samtale eller skills) og årshjul](https://olefredrik.github.io/Bodil/bruk/)
- [Den låste modellen](https://olefredrik.github.io/Bodil/modellen/)
- [Folio-integrasjon](https://olefredrik.github.io/Bodil/folio/)
- [Oppdatere en eksisterende kopi](https://olefredrik.github.io/Bodil/oppdatere/)

## Kom i gang

Engangsoppsett (detaljer i [dokumentasjonen](https://olefredrik.github.io/Bodil/kom-i-gang/)):

1. **Lag din egen private kopi.** Dette offentlige repoet er malen og inneholder kun verktøyet, aldri regnskapsdata. Bruk «Use this template» på GitHub til et **privat** repo.
2. **Åpne ditt private repo i [Claude Code](https://claude.com/claude-code).** Skillene i `.claude/skills/` oppdages automatisk.
3. **Fyll inn stamdata:** `cp selskap.example.yaml selskap.yaml` og fyll inn selskapet ditt (`selskap.yaml` er gitignored, den inneholder fødselsnummer).

Deretter fører du regnskapet ett år av gangen: `/bokforing` → avgjør utbytte → `/protokoll` → `/wenche-config`. Innsending skjer i **Wenche**, enklest på hostet [wenche.cloud](https://wenche.cloud) (last opp `config.yaml`, ingenting å installere), eller self-hosted lokalt. Se [Bruk](https://olefredrik.github.io/Bodil/bruk/) og [Bodil og Wenche](https://olefredrik.github.io/Bodil/bodil-og-wenche/).

## Personvern

Fødselsnummer og nøkler skal aldri i git. `selskap.yaml`, `<år>/config.yaml`, `*.pem`, `.env` og bilag er gitignored fra start, og bankeksporten ignoreres som standard. Pusher du til et remote-repo: hold det **privat** og behold `.gitignore` som den er.

## Lisens

Utgitt under [MIT-lisensen](LICENSE). Leveres «som det er», uten garanti.
