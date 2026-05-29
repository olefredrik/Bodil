# Wenche-regnskap: driftsregler for Claude

Dette repoet fører regnskap «i git» for et **passivt holdingselskap** og produserer det Wenche trenger for å sende inn til myndighetene. Du (Claude) gjør bokføringen via de tre skillene i `.claude/skills/`. Du sender **ingenting** selv, det gjør Wenche.

## Scope

Kun passive holdingselskaper: selskaper som eier aksjer i andre selskaper og ellers bare har bankkostnader (og eventuelt mottar utbytte). Driftsselskaper er utenfor scope. Møter du noe som ikke passer den låste modellen under, **flagg det og spør** i stedet for å gjette.

## Låst bokføringsmodell

| Hendelse i bankeksporten | Bokføres som |
|---|---|
| Penger inn fra eier | Lån fra aksjonær (gjeld) |
| Utbytte mottatt fra datterselskap | Finansinntekt (utbytte fra datterselskap) |
| Penger ut til eier | Utbytte (reduserer egenkapital) |
| Alle andre utbetalinger | Driftskostnad |
| Kjøp/salg av eierposter | Finansielle anleggsmidler til kostpris (fra `selskap.yaml`) |

Ingen andre kontoer. Ingen inntekter utover utbytte fra datterselskap. Resultatet blir et lite underskudd lik driftskostnadene, med mindre det er mottatt utbytte.

## Faste regler

- **Stamdata leses fra `selskap.yaml`** (navn, org.nr., aksjekapital, aksjonærer med fødselsnummer, åpningsbalanse, eierposter). Finnes bare `selskap.example.yaml`, be brukeren kopiere den til `selskap.yaml` først.
- **Fødselsnummer og nøkler skal aldri i git.** `selskap.yaml` og `<år>/config.yaml` er gitignored. Ikke skriv fødselsnummer inn i `regnskap.md` eller `protokoll.md` (de versjoneres).
- **Flagg, ikke gjett.** Stopp på: transaksjoner som ikke passer modellen, uvanlig store poster, og utbytte uten dekning i fri egenkapital (`overkursfond + annen_egenkapital < 0` etter utdeling, jf. aksjeloven § 8-1).
- **Balansen skal gå opp.** Sum eiendeler = sum egenkapital og gjeld. Hvis ikke, finn årsaken før du går videre.

## Rekkefølge per regnskapsår (én avhengighet: utbytte må avgjøres før protokoll)

1. **bokforing** → `<år>/regnskap.md` (resultat + balanse + transaksjonslogg)
2. Avgjør utbytte (kun ved dekning i fri egenkapital) → oppdater balansen
3. **protokoll** → `<år>/protokoll.md` (godkjenner regnskapet, vedtar utbytte)
4. **wenche-config** → `<år>/config.yaml` + sjekkliste, og kjør `wenche valider-aarsregnskap --config <år>/config.yaml`
5. Brukeren åpner Wenche (`wenche`), laster `config.yaml`, fyller noter i Dokumenter-fanen, og sender

## Arbeidsdeling mot Wenche

- Wenche eier innsending og datamodellen. Companion produserer `config.yaml` mot Wenches feltnavn og selv-verifiserer med `wenche valider-aarsregnskap`.
- Wenche genererer de fire pålagte notene selv. Companion lager dem **ikke**. Note-input (antall ansatte = 0, lån til nærstående) fylles i Wenches Dokumenter-fane, ikke her.
- `formuesverdi_aksjer` (RF-1088S post 209) kan ikke utledes fra bankeksporten. wenche-config flagger dette som manuelt input.

## Ansvar

Dette er et hjelpeverktøy, ikke en regnskapsfører. Genererte dokumenter må kontrolleres før innsending. Få en regnskapsfører til å se over år 1, særlig skatteberegningen, så har du en verifisert mal for resten.
