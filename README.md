# Bodil

**Regnskap for holdingselskap, følgeverktøy til [Wenche](https://github.com/olefredrik/Wenche).**

Bokføring «i git» for et **passivt holdingselskap**, drevet av Claude Code. Repoet gjør om en bankeksport (CSV) til et lesbart regnskap, en generalforsamlingsprotokoll, og en ferdig `config.yaml` som [Wenche](https://github.com/olefredrik/Wenche) sender inn til myndighetene.

Bodil og Wenche er to verktøy med hver sin jobb: Bodil fører bøkene, Wenche sender inn og rapporterer til myndighetene. Wenche kan brukes alene hvis du allerede har tallene; trenger du å føre regnskapet først, kobler du på Bodil.

Tanken er enkel: et hvilende holdingselskap har likevel plikt til å føre og levere årsregnskap, men et fullt regnskapssystem gir liten verdi når det knapt er aktivitet. Dette repoet dekker bokføringen, Wenche dekker innsendingen, og sammen blir det en komplett, nesten gratis tjeneste.

## Hva dette er, og ikke er

- **Er:** et hjelpeverktøy for bokføring og dokumentproduksjon for passive holdingselskaper.
- **Er ikke:** en regnskapsfører, og ikke et innsendingsverktøy. Innsendingen gjør du med Wenche. Kontroller alltid tallene før du sender, og få gjerne en regnskapsfører til å se over det første året.

Driftsselskaper er utenfor scope, akkurat som i Wenche.

## Bokføringsmodellen

Modellen er bevisst minimal og dekker det et passivt holdingselskap har:

| Hendelse i bankeksporten | Bokføres som |
|---|---|
| Penger inn fra eier | Lån fra aksjonær (gjeld) |
| Utbytte mottatt fra datterselskap | Finansinntekt |
| Penger ut til eier | Utbytte (reduserer egenkapital) |
| Alle andre utbetalinger | Driftskostnad (typisk bankgebyrer) |
| Eierposter i andre selskap | Finansielle anleggsmidler til kostpris |

Alt som ikke passer denne modellen blir flagget, ikke gjettet.

## Kom i gang (engangsoppsett)

Dette gjør du bare én gang:

1. **Lag din egen private kopi.** Dette offentlige repoet er malen og inneholder kun verktøyet, aldri regnskapsdata. Bruk «Use this template» på GitHub (eller klon repoet) til et **privat** repo. Det er der tallene dine havner.
2. **Installer Wenche** (kreves for validering og innsending): `pipx install wenche` (krever Python ≥ 3.11). Sett opp Maskinporten som beskrevet i [Wenche-dokumentasjonen](https://github.com/olefredrik/Wenche).
3. **Åpne ditt private repo i Claude Code.** De tre skillene i `.claude/skills/` oppdages automatisk.
4. **Fyll inn stamdata:** kopier `selskap.example.yaml` til `selskap.yaml` og fyll inn selskapet ditt. (`selskap.yaml` holdes utenfor git fordi den inneholder fødselsnummer.)

Deretter fører du regnskapet ett år av gangen. Les «Slik kjører du skillene» under, og følg «Årshjul».

## Slik kjører du skillene

Det er ingen app å installere og starte, og ingen nettside. Du «kjører» dette repoet ved å snakke med Claude Code: skillene ligger i `.claude/skills/` og oppdages automatisk når du åpner repoet i Claude Code.

Du starter en skill på én av to måter:

- **Skråstrek-kommando** (eksplisitt): skriv `/bokforing` i chatten. En liste dukker opp når du taster `/`, og du skal se `bokforing`, `protokoll` og `wenche-config` der. Tilsvarende `/protokoll` og `/wenche-config`.
- **Vanlige ord** (la Claude velge): be om det rett ut, f.eks. «før regnskapet for 2026», så starter Claude riktig skill selv.

Du kjører én skill av gangen, ser på resultatet, og går videre til neste. Claude sender **ingenting** selv. Innsendingen gjør du i Wenche helt til slutt. Og Claude stopper og spør hvis noe ikke passer den låste bokføringsmodellen, i stedet for å gjette.

## Årshjul

For hvert regnskapsår, kjør skillene slik. Bytt ut `<år>` med året, f.eks. legg bankeksporten i `2026/bankeksport.csv`:

1. `/bokforing` → lager `<år>/regnskap.md` (resultatregnskap + balanse + transaksjonslogg)
2. **Avgjør utbytte** sammen med Claude (kun hvis det er fri egenkapital å dele ut)
3. `/protokoll` → lager `<år>/protokoll.md` (godkjenner regnskapet og vedtar utbytte, fungerer også som utbytte-bilag)
4. `/wenche-config` → lager `<år>/config.yaml` + en sjekkliste, og kjører `wenche valider-aarsregnskap` for deg
5. **Overfør til Wenche og send inn** (se «Overføring til Wenche» rett under)

**Frister:** aksjonærregisteroppgave 31. januar · skattemelding 31. mai · årsregnskap 31. juli. Merk: det manuelle skjemaet for aksjonærregisteroppgaven fases ut, så fra januar 2027 må også den gå via Wenche.

## Overføring til Wenche

Det skjer ingen automatisk integrasjon mellom dette repoet og Wenche: **`config.yaml`-fila er broen**. `wenche-config`-skillen skriver `<år>/config.yaml` med Wenches eksakte feltnavn, og Wenche leser den fila inn. Du flytter altså ikke tall manuelt; du peker Wenche på riktig fil.

Wenche (både web-grensesnittet og CLI-kommandoene) ser etter en `config.yaml` **i mappen du starter den fra**. Den enkleste flyten er derfor å starte Wenche fra årsmappen:

```bash
cd 2026          # mappen som inneholder config.yaml
wenche           # åpner http://localhost:8080 og laster config.yaml herfra
```

I web-grensesnittet går du gjennom fanene, fyller inn noter i **Dokumenter**-fanen (antall ansatte, eventuelt lån til/fra nærstående; Wenche genererer selve notene), kontrollerer tallene, og sender inn. Klikker du **Lagre konfigurasjon** skriver Wenche tilbake til samme `<år>/config.yaml` (den er gitignored, så det er trygt).

> **Merk om nøkler:** Maskinporten-nøkkelen og `.env` ligger i `~/.wenche/`, altså utenfor dette repoet. De følger Wenche, ikke regnskapet, og berøres ikke av flyten over.

### Wenche-kompatibilitet

`config.yaml`-fila er broen mellom verktøyene, så Bodil må holde tritt med Wenches feltnavn. Denne Bodil-versjonen er testet mot **Wenche ≥ 0.24.0**. Hvilken Wenche-versjon hver Bodil-versjon er verifisert mot står i [CHANGELOG.md](CHANGELOG.md).

Kompatibiliteten håndheves automatisk: en GitHub Action ([wenche-kompatibilitet.yml](.github/workflows/wenche-kompatibilitet.yml)) validerer et golden-fixture mot den pinnede Wenche-versjonen på hver PR, og kjører ukentlig mot nyeste Wenche for å varsle om kommende endringer. Bruker du en eldre Bodil-kopi mot en mye nyere Wenche, sjekk CHANGELOG-en.

## Mappestruktur

```
selskap.yaml              dine stamdata (utenfor git)
<år>/
  bankeksport.csv         rådata fra banken
  bilag/                  avtaler, kvitteringer, verdioversikter (oppbevaringsplikt 5 år)
  regnskap.md             selve regnskapet (versjoneres)
  protokoll.md            generalforsamlingsprotokoll (versjoneres)
  config.yaml             input til Wenche (utenfor git)
```

Git-historikken til `regnskap.md` fungerer som et uforanderlig revisjonsspor. Selve bilagene må du likevel oppbevare i fem år, git er arbeidsboka, ikke arkivet.

## Personvern

Fødselsnummer og nøkler skal aldri i git. `selskap.yaml`, `<år>/config.yaml`, `*.pem` og bilag er gitignored fra start. Bankeksporten ignoreres også som standard, fjern linjen i `.gitignore` hvis du heller vil ha full kilde-i-git.

## Lokalt eller privat repo?

**Anbefalingen er et privat remote-repo** (f.eks. en privat GitHub-repo), ikke bare en lokal mappe. Du får da to ting:

- **Sikkerhetskopi utenfor maskinen.** Git-historikken til `regnskap.md` og `protokoll.md` er ditt revisjonsspor; en lokal-bare-mappe taper alt ved diskkrasj.
- **Uforanderlig historikk.** Hver commit datostempler hva regnskapet sa på et gitt tidspunkt.

Det er trygt fordi alt sensitivt holdes utenfor git fra start: fødselsnummer (`selskap.yaml`, `config.yaml`), nøkler (`*.pem`, `.env`) og bilag pushes aldri. Det som havner på remote er regnskap og protokoll i markdown, uten personnummer.

To absolutte krav hvis du pusher:

1. **Repoet må være privat.** Selv uten fødselsnummer er regnskapstall private. Aldri offentlig.
2. **Behold `.gitignore` som den er.** Den holder sensitive filer ute. Dette gjelder også private repoer: fødselsnummer skal aldri i git, fordi historikken er permanent, «privat» ikke er det samme som «sikkert», og fødselsnummer er personopplysninger (ofte om andre aksjonærer). Sjekk med `git status` før første push at `selskap.yaml` og `config.yaml` ikke er med.

Vil du holde alt på maskinen, fungerer et rent lokalt repo også, men du mister sikkerhetskopien. Uansett valg: **bilagene må oppbevares lokalt i fem år** (de er gitignored). Git er arbeidsboka, ikke arkivet.

## Ansvar

**All bruk av dette verktøyet skjer på eget ansvar.** Dette er et hjelpeverktøy for bokføring og dokumentproduksjon, ikke en regnskapsfører, en revisor eller juridisk rådgivning.

Du har selv det fulle ansvaret for at det du sender inn til myndighetene er korrekt og fullstendig. Verktøyet kan ta feil: en transaksjon kan bli feilklassifisert, modellen kan passe dårlig for nettopp ditt selskap, eller en regel kan ha endret seg siden dette ble skrevet. Genererte dokumenter (`regnskap.md`, `protokoll.md`, `config.yaml`) er utkast som du må kontrollere før de brukes.

Konkret betyr det:

- **Kontroller alle tall og dokumenter** før du sender noe inn via Wenche.
- **Få en regnskapsfører eller revisor til å se over det første året**, særlig skatteberegningen. Da har du en verifisert mal for årene etter.
- **Sørg for at selskapet ditt faktisk passer modellen** (passivt holdingselskap). Driftsselskaper er utenfor scope.
- **Du, ikke verktøyet, er ansvarlig** overfor Skatteetaten, Brønnøysundregistrene og andre myndigheter.

Verktøyet leveres «som det er», uten noen form for garanti. Se lisensen under.

## Lisens

Utgitt under MIT-lisensen. Se [LICENSE](LICENSE) for fullstendig tekst. MIT betyr at du fritt kan bruke, endre og dele koden, men at den leveres uten garanti og uten ansvar for utfallet av bruken.
