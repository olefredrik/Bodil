# Bodil

Bodil fører regnskap «i git» for et **passivt holdingselskap**, drevet av [Claude Code](https://claude.com/claude-code). Repoet gjør om en bankeksport (CSV) til et lesbart regnskap, en generalforsamlingsprotokoll og en ferdig `config.yaml` som [Wenche](https://github.com/olefredrik/Wenche) sender inn til myndighetene.

Tanken er enkel: et hvilende holdingselskap har likevel plikt til å føre og levere årsregnskap, men et fullt regnskapssystem gir liten verdi når det knapt er aktivitet. Bodil dekker bokføringen, Wenche dekker innsendingen, og sammen dekker de hele løpet fra bankeksport til innsendt årsregnskap.

## Hva gjør Bodil?

Du fører ett regnskapsår av gangen ved å snakke med Claude Code. For hvert år produserer Bodil:

- **`regnskap.md`** — resultatregnskap, balanse og en transaksjonslogg, ført etter en bevisst minimal, [låst modell](modellen.md).
- **`protokoll.md`** — generalforsamlingsprotokoll som godkjenner regnskapet og vedtar utbytte eller dekning av underskudd. Fungerer også som utbytte-bilag.
- **`config.yaml`** — input med Wenches eksakte feltnavn, broen som lar [Wenche](bodil-og-wenche.md) sende inn uten at du flytter tall manuelt.

Claude sender **ingenting** selv. Innsendingen gjør du i Wenche helt til slutt, og Claude stopper og spør hvis noe ikke passer modellen, i stedet for å gjette.

## Hvem passer det for?

Bodil er laget for **passive holdingselskaper**: selskaper som eier aksjer i andre selskaper og ellers bare har bankkostnader, og eventuelt mottar utbytte.

!!! warning "Bodil er ikke en regnskapsfører"
    Bodil er et hjelpeverktøy for bokføring og dokumentproduksjon, ikke en regnskapsfører, revisor eller juridisk rådgivning. Genererte dokumenter er utkast du må kontrollere før bruk. Driftsselskaper er utenfor scope. Les [Ansvar](ansvar.md) før du tar verktøyet i bruk.

## Kom i gang

[Kom i gang →](kom-i-gang.md){ .md-button .md-button--primary }
[Bodil og Wenche →](bodil-og-wenche.md){ .md-button }

Begge verktøyene er gratis og åpen kildekode. Den eneste kostnaden er at Bodil kjøres av Claude Code og derfor forutsetter at du har tilgang til Claude (et abonnement eller API-tilgang).
