# Bodil og Wenche

Bodil og Wenche er to verktøy med hver sin jobb:

- **Bodil fører bøkene.** Den gjør en bankeksport om til et regnskap, en protokoll og en `config.yaml`.
- **Wenche sender inn.** Den tar tallene og rapporterer årsregnskap, skattemelding og aksjonærregisteroppgave til myndighetene.

Wenche kan brukes alene hvis du allerede har tallene. Trenger du å føre regnskapet først, kobler du på Bodil. Sammen dekker de hele løpet fra bankeksport til innsendt årsregnskap.

## `config.yaml` er broen

Det skjer ingen automatisk integrasjon mellom de to verktøyene. **`config.yaml`-fila er broen.** `wenche-config`-skillen skriver `<år>/config.yaml` med Wenches eksakte feltnavn, og Wenche leser den fila inn. Du flytter altså ikke tall manuelt, du peker Wenche på riktig fil.

Wenche (både web-grensesnittet og CLI-kommandoene) ser etter en `config.yaml` i mappen du starter den fra. Den enkleste flyten er derfor å starte Wenche fra årsmappen:

```bash
cd 2026          # mappen som inneholder config.yaml
wenche           # åpner http://localhost:8080 og laster config.yaml herfra
```

I web-grensesnittet går du gjennom fanene, fyller inn noter i **Dokumenter**-fanen (antall ansatte, eventuelt lån til/fra nærstående; Wenche genererer selve notene), kontrollerer tallene, og sender inn.

!!! note "Nøkler følger Wenche, ikke regnskapet"
    Maskinporten-nøkkelen og `.env` ligger i `~/.wenche/`, altså utenfor Bodil-repoet. De berøres ikke av flyten over.

## Wenche-kompatibilitet

Siden `config.yaml` er broen, må Bodil holde tritt med Wenches feltnavn. Hver Bodil-versjon er verifisert mot en bestemt Wenche-versjon, oppgitt i [CHANGELOG](https://github.com/olefredrik/Bodil/blob/main/CHANGELOG.md).

Kompatibiliteten håndheves automatisk: en GitHub Action validerer et golden-fixture mot den pinnede Wenche-versjonen på hver PR, og kjører ukentlig mot nyeste Wenche for å varsle om kommende endringer. Bruker du en eldre Bodil-kopi mot en mye nyere Wenche, sjekk CHANGELOG.

Se [Wenche-dokumentasjonen](https://olefredrik.github.io/Wenche/) for installasjon, Maskinporten-oppsett og innsending.
