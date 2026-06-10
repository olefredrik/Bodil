# Kom i gang

Engangsoppsett. Dette gjør du bare én gang.

## 1. Lag din egen private kopi

Det offentlige Bodil-repoet er **malen**, og inneholder kun verktøyet, aldri regnskapsdata. Trykk **«Use this template»** på [GitHub](https://github.com/olefredrik/Bodil) (eller klon repoet) til et eget repo. Det er der tallene dine havner.

!!! warning "Repoet må være privat"
    Velg **Private** når du oppretter ditt eget repo. Selv uten fødselsnummer er regnskapstall private. Se [Lokalt eller privat repo?](#lokalt-eller-privat-repo) under.

## 2. Installer Wenche

Wenche kreves for validering og innsending:

```bash
pipx install wenche      # krever Python ≥ 3.11
```

Sett opp Maskinporten som beskrevet i [Wenche-dokumentasjonen](https://olefredrik.github.io/Wenche/).

## 3. Åpne repoet i Claude Code

Åpne ditt private repo i [Claude Code](https://claude.com/claude-code). Skillene i `.claude/skills/` oppdages automatisk. Bodil drives av Claude Code, så dette forutsetter at du har tilgang til Claude (et abonnement eller API-tilgang). Det er den eneste kostnaden; selve verktøyene er gratis.

## 4. Fyll inn stamdata

Kopier `selskap.example.yaml` til `selskap.yaml` og fyll inn selskapet ditt: navn, org.nr., aksjekapital, aksjonærer, åpningsbalanse og eierposter.

```bash
cp selskap.example.yaml selskap.yaml
```

`selskap.yaml` holdes utenfor git fordi den inneholder fødselsnummer.

---

Deretter fører du regnskapet ett år av gangen. Les [Bruk](bruk.md) og følg årshjulet.

!!! tip "Allerede en kopi fra før?"
    Har du laget kopien din tidligere og vil hente inn nyere verktøy (som Folio-integrasjonen), se [Oppdatere Bodil](oppdatere.md).

## Personvern

Fødselsnummer og nøkler skal aldri i git. `selskap.yaml`, `<år>/config.yaml`, `*.pem` og bilag er gitignored fra start. Bankeksporten ignoreres også som standard; fjern linjen i `.gitignore` hvis du heller vil ha full kilde-i-git.

## Lokalt eller privat repo?

**Anbefalingen er et privat remote-repo** (f.eks. en privat GitHub-repo), ikke bare en lokal mappe. Du får da to ting:

- **Sikkerhetskopi utenfor maskinen.** Git-historikken til `regnskap.md` og `protokoll.md` er ditt revisjonsspor; en lokal-bare-mappe taper alt ved diskkrasj.
- **Uforanderlig historikk.** Hver commit datostempler hva regnskapet sa på et gitt tidspunkt.

Det er trygt fordi alt sensitivt holdes utenfor git fra start. To absolutte krav hvis du pusher:

1. **Repoet må være privat.** Selv uten fødselsnummer er regnskapstall private. Aldri offentlig.
2. **Behold `.gitignore` som den er.** Den holder fødselsnummer og nøkler ute. «Privat» er ikke det samme som «sikkert», og historikken er permanent. Sjekk med `git status` før første push at `selskap.yaml` og `config.yaml` ikke er med.

Vil du holde alt på maskinen, fungerer et rent lokalt repo også, men du mister sikkerhetskopien. Uansett valg: **bilagene må oppbevares lokalt i fem år** (de er gitignored). Git er arbeidsboka, ikke arkivet.
