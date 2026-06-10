# Bodil og Wenche

Bodil og Wenche er to verktøy med hver sin jobb:

- **Bodil fører bøkene.** Den gjør en bankeksport om til et regnskap, en protokoll og en `config.yaml`.
- **Wenche sender inn.** Den tar tallene og rapporterer årsregnskap, skattemelding og aksjonærregisteroppgave til myndighetene.

Wenche kan brukes alene hvis du allerede har tallene. Trenger du å føre regnskapet først, kobler du på Bodil. Sammen dekker de hele løpet fra bankeksport til innsendt årsregnskap.

## `config.yaml` er broen

Det skjer ingen automatisk integrasjon mellom de to verktøyene. **`config.yaml`-fila er broen.** `wenche-config`-skillen skriver `<år>/config.yaml` med Wenches eksakte feltnavn, og Wenche leser den inn. Du flytter altså ikke tall manuelt, du gir Wenche fila.

Det er to måter å bruke Wenche på, og `config.yaml` fungerer likt i begge.

## Hostet Wenche (anbefalt)

Den enkleste veien er den hostede versjonen på **[wenche.cloud](https://wenche.cloud)**. Da slipper du å installere noe; oppsettet (Maskinporten) er gjort av operatøren.

1. Gå til [wenche.cloud](https://wenche.cloud) og koble selskapet til Altinn (én gang, med BankID).
2. Under **Tall** klikker du **Hent tall fra Bodil** og laster opp `<år>/config.yaml`.
3. Skjemaet forhåndsfylles. Du ser over, fyller noter i **Dokumenter**-fanen (antall ansatte, eventuelt lån til/fra nærstående; Wenche genererer selve notene), og sender inn.

!!! warning "Fødselsnummer forlater maskinen ved opplasting"
    `config.yaml` inneholder fødselsnummer. Laster du den opp til wenche.cloud, behandles den **kun i økten og lagres ikke i database**, men den sendes dit. Vil du at fødselsnummer aldri skal forlate maskinen, bruk self-hosted under.

## Self-hosted Wenche (lokalt)

Vil du kjøre alt på egen maskin, installerer du Wenche selv (`pipx install wenche`) og setter opp Maskinporten, se [Wenche-dokumentasjonen](https://olefredrik.github.io/Wenche/). Da starter du Wenche fra årsmappen, slik at den finner `config.yaml`:

```bash
cd 2026          # mappen som inneholder config.yaml
wenche           # åpner http://localhost:8080 og laster config.yaml herfra
```

Resten er likt: gå gjennom fanene, fyll noter i **Dokumenter**-fanen, kontroller, og send inn. Her forlater fødselsnummer aldri maskinen.

!!! note "Nøkler følger Wenche, ikke regnskapet"
    For self-hosted ligger Maskinporten-nøkkelen og `.env` i `~/.wenche/`, altså utenfor Bodil-repoet.

## Wenche-kompatibilitet

Siden `config.yaml` er broen, må Bodil holde tritt med Wenches feltnavn. Hver Bodil-versjon er verifisert mot en bestemt Wenche-versjon, oppgitt i [CHANGELOG](https://github.com/olefredrik/Bodil/blob/main/CHANGELOG.md).

Kompatibiliteten håndheves automatisk: en GitHub Action validerer et golden-fixture mot den pinnede Wenche-versjonen på hver PR, og kjører ukentlig mot nyeste Wenche for å varsle om kommende endringer. Bruker du en eldre Bodil-kopi mot en mye nyere Wenche, sjekk CHANGELOG.

Se [Wenche-dokumentasjonen](https://olefredrik.github.io/Wenche/) for installasjon, Maskinporten-oppsett og innsending.
