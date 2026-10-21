# Endringslogg

Alle merkbare endringer i Bodil dokumenteres her. Formatet følger løst
[Keep a Changelog](https://keepachangelog.com/), og versjonene følger
[SemVer](https://semver.org/) tilpasset et template-prosjekt:

- **MAJOR** — den låste bokføringsmodellen endres, eller Wenche-kompatibilitet brytes
- **MINOR** — ny skill, ny håndtert hendelse, eller støtte for en ny Wenche-versjon
- **PATCH** — ordlyd, dokumentasjon, feilretting i en skill

Hver oppføring som rører grensesnittet mot Wenche oppgir hvilken Wenche-versjon
Bodil er testet mot. Den versjonen er også pinnet i CI
([wenche-kompatibilitet.yml](.github/workflows/wenche-kompatibilitet.yml)).

## [1.2.0]

- **Utbytte fra eierposter under 20 % føres som utbytte fra andre aksjer.** Bodil førte alt mottatt utbytte som `utbytte_fra_datterselskap`, og Wenche sendte det til Brønnøysund som «Inntekt på investering i datterselskap og tilknyttet selskap». Fra en eierpost under 20 % er selskapet verken datterselskap eller tilknyttet selskap. `bokforing` velger nå linje etter eierandelen, og `wenche-config` mapper til `utbytte_fra_andre_aksjer`, som Wenche har fra 1.8.0. Skatten er den samme: utbytte fra andre aksjer får alltid 3 %-sjablonen. Nytt fixture `config.andre-aksjer.yaml` (#30). **Feltet krever Wenche 1.8.0 eller nyere.** Eldre Wenche ignorerer det uten varsel, så utbyttet forsvinner fra resultatet. Hostet Wenche er oppdatert. Kjører du Wenche lokalt, oppgrader med `pipx upgrade wenche`. `wenche-config` sjekker versjonen og stopper hvis den er for gammel.
- **Ubetalte regninger per 31.12 føres som leverandørgjeld.** Bodil førte bare det som hadde gått gjennom bankkontoen, så en regning for regnskapsåret som ble betalt etter årsskiftet, havnet i feil år. `bokforing` spør nå om ubetalte regninger per 31.12 og fører dem som kostnad med `leverandoergjeld` som motpost, og betalingen året etter reduserer gjelden i stedet for å bli en ny kostnad. `selskap.example.yaml` har fått `leverandoergjeld` under `aapningsbalanse`, og `wenche-config` mapper feltet. Nytt fixture `config.leverandoergjeld.yaml` (#31).

**Overgang:** står utbytte fra en eierpost under 20 % som utbytte fra datterselskap i fjorårets `regnskap.md`, flytter `bokforing` fjorårets beløp til «Utbytte fra andre aksjer» i sammenligningstallene. Årsresultatet endres ikke, og ingenting må sendes inn på nytt.

**Testet mot Wenche ≥ 1.8.0.**

## [1.1.0]

- **`folio_import.py --med-id`** legger til kolonnen `folio_id` med Folios transaksjons-id, så et annet system kan skille to like transaksjoner fra en duplikat ved gjentatt import. Uten flagget er CSV-en uendret. Mangler en transaksjon id, stopper skriptet.
- **Nedbetaling av lån fra aksjonær er en egen rad i den låste modellen.** Lånet kunne bare øke, så en nedbetaling ble flagget med svaralternativer som ikke passet. Nå reduserer en bekreftet nedbetaling `laan_fra_aksjonaer` opp til utestående lån, og den er første svaralternativ i «Utbetaling uten avsetning». Har selskapet både avsatt utbytte og lån fra aksjonær, spør Bodil om utbetalingen er utbytte eller nedbetaling i stedet for å la avsetningen dekke den først, siden svaret avgjør hva eieren skattlegges for. Nedbetalinger holdes utenfor `utbytte_utbetalt`. Innbetaling fra eier flagges hvis beskrivelsen tyder på kapitalforhøyelse eller tilleggsinnbetaling (aksjeloven kapittel 10), ellers føres den som lån som før.
- **Salg av eierpost gir nå et regnskap som går opp.** Kostprisen tas ut av balansen, og differansen mot salgssummen føres som gevinst eller tap ved realisasjon av aksjer. `bokforing` holder gevinst og tap utenfor skatteberegningen (fritaksmetoden: gevinst skattefri, tap ikke fradragsberettiget), flagger utenlandske selskaper og ber brukeren oppdatere `eierposter` i `selskap.yaml`. Delsalg tar ut forholdsmessig kostpris. `wenche-config` fører beløpene til `gevinst_ved_realisasjon_av_aksjer` og `tap_ved_realisasjon_av_aksjer`, som Wenche har hatt siden 1.6.0 og holder utenfor skatten på samme måte. I `andre_finansinntekter` ville gevinsten blitt skattlagt fullt (#29).
- **Fullt skattefritt utbytte krever eierandel over 90 %.** Bodil regnet nøyaktig 90 % som fritatt, men unntaket fra 3 %-sjablonen i fritaksmetoden gjelder konsern etter sktl. § 10-4, som krever *mer enn* 90 % av aksjene og stemmene. Ved nøyaktig 90 % førte Bodil derfor skattekostnad 0, mens Wenche (fra 1.6.1) beregner skatt og varsler om at den ikke er ført (#27).
- **`underskudd_til_fremfoering` er nå saldoen ved årets start.** Wenche leser feltet som fremførbart underskudd fra tidligere år og legger selv til årets underskudd, men `wenche-config` hentet «Underskudd til fremføring neste år», altså saldoen 31.12. Årets underskudd ble dermed telt to ganger: et år med 2 896 i kostnader og intet underskudd fra før ga 5 792 i underskudd til fremføring hos Wenche. I et år med overskudd ble det brukte underskuddet trukket fra to ganger. «Skattemessig» i `regnskap.md` har fått linjen «Fremførbart underskudd 01.01», som `wenche-config` nå sender, og `bokforing` fastsetter den hvert år. Mangler linjen (`regnskap.md` ført med eldre Bodil), henter `wenche-config` fjorårets «Underskudd til fremføring neste år» i stedet. Nytt fixture `config.fremfoert-underskudd.yaml`. Feilen kom inn i 0.5.0. **Har du levert skattemelding med Bodil 0.5.0 eller nyere, kontroller underskudd til fremføring** i den innleverte skattemeldingen og send endret skattemelding hvis det er feil (#26).
- **`wenche-config` skriver `utbytte_vedtaksdato`.** Wenche krever datoen fra 1.7.0 når det er utbetalt utbytte, og uten den stoppet aksjonærregisteroppgaven på valideringen. Er utbyttet betalt mot fjorårets avsetning, hentes datoen fra generalforsamlingen i `<år-1>/protokoll.md`. Er det vedtatt og utbetalt i året, spør Bodil brukeren. Bodil stopper hvis begge deler skjer med ulik dato (Wenche har ett datofelt), og hvis protokollen ikke har en faktisk dato. `protokoll` ber nå om den faktiske møtedatoen. CI validerer også aksjonærregisteroppgaven for hvert fixture (`wenche send-aksjonaerregister --dry-run`), og fixturene bruker syntetiske fødselsnumre med gyldige kontrollsifre. XML-filene Wenche skriver ut for oppgaven inneholder fødselsnummer og er lagt i `.gitignore` (#28).
- **Eierposter selskapet har kontroll over føres nå som `aksjer_i_datterselskap`, ikke `andre_aksjer`.** Bodil førte alle eierposter som andre aksjer, og wenche-config brukte 90 % som grense. Men 90 % er skattens grense (fritaksmetoden, konsern etter sktl. § 10-4); regnskapsmessig er et selskap datterselskap ved bestemmende innflytelse, normalt flertallet av stemmene (rskl. § 1-3, asl. § 1-3 andre ledd). Wenche oppgir selskapet som morselskap når `aksjer_i_datterselskap` er over 0, så et heleid holdingselskap ble rapportert som «ikke morselskap». Grensen leses av `eierandel_prosent` (over 50 %), med valgfritt `datterselskap: true|false` per eierpost som overstyring. Nøyaktig 50 % flagges. 90 %-grensen gjelder bare fritaksmetoden (#27). Nytt fixture `config.datterselskap.yaml`.
- **Bankrenter er nå en del av den låste modellen.** Renteinntekt fra banken føres som `andre_finansinntekter` og er fullt skattepliktig (22 %, verken fritaksmetode eller sjablon). Debetrenter på kontoen føres som `rentekostnader`. Renter på lån i banken, til eier eller til Skatteetaten flagges, siden et lån i banken er utenfor modellen. Skatteberegningen i `bokforing` tar med begge, med samme formel som Wenches `beregn_skatt`, og `wenche-config` mapper dem i stedet for å skrive 0.
- **`protokoll` har formulering for overskudd uten utbytte.** Malen dekket bare avsetning, utbytte utdelt i året og underskudd. Nå fastslår den også at et overskudd uten utbytte overføres til annen egenkapital, og ved avsetning hva som skjer med resten av årsresultatet. Utbytte utbetalt mot fjorårets avsetning omtales ikke som et vedtak (#33).
- **`kontakt_epost` ligger i `selskap.yaml`.** Feltet er påkrevd for aksjonærregisteroppgaven, men hadde ingen kilde. `selskap.example.yaml` har det nå, og `wenche-config` spør hvis det mangler (#34). Har du laget `selskap.yaml` før denne versjonen, legg til `kontakt_epost` under `selskap`.
- **Første år i Bodil for et eldre selskap gir riktige sammenligningstall.** Uten fjorårets `regnskap.md` fantes ingen regel for fjorårets resultatregnskap, og et utelatt `foregaaende_aar.resultatregnskap` fikk Wenche til å sende fjorårets resultat som 0. `bokforing` spør nå om fjorårets resultat fra det innsendte årsregnskapet, og `wenche-config` stopper i stedet for å utelate det (#35).
- **Utbytte vedtatt i året må ha dekning i sist godkjente årsregnskap.** Bodil kontrollerte fri egenkapital per 31.12 i inneværende år, så årets resultat kunne dekke et utbytte som ikke hadde dekning da det ble vedtatt (aksjeloven § 8-1). `bokforing` kontrollerer nå mot fjorårets balanse og stopper hvis dekningen mangler, og «stopp» gjelder også kontrollen av årets balanse. Eksempeldataene har fått 15 000 i annen egenkapital ved årets start, og `config.golden.yaml` er oppdatert, så golden-fixturet ikke lenger bygger inn et utbytte uten dekning (#36).
- **`wenche-config` spør etter `formuesverdi_aksjer`.** Skillen sa bare at feltet må fylles inn manuelt, og i en test ble det stående tomt. Wenche godtar et tomt felt uten varsel og regner med 0. Nå spør Claude brukeren og skriver aldri 0 uten bekreftelse.

**Overgang:** har fjoråret, ført med Bodil 1.0.0 eller eldre, en eierpost under `andre_aksjer` som nå er datterselskap, flytter `bokforing` fjorårets beløp til `aksjer_i_datterselskap` i sammenligningstallene, så linjene er sammenlignbare. Summen eiendeler endres ikke, og fjorårets `regnskap.md` og innsendte årsregnskap røres ikke. Debetrenter ble tidligere ført som `andre_driftskostnader` («alle andre utbetalinger») og føres nå som `rentekostnader`. Har fjoråret slike renter, står de derfor på ulike linjer i de to kolonnene. Resultatet er det samme, og ingenting må sendes inn på nytt.

**Testet mot Wenche ≥ 1.7.2.**

## [1.0.0]

Denne versjonen endrer den låste bokføringsmodellen. Les «Overgang» nederst i seksjonen
før du fører et nytt år.

- **Utbytte føres nå i avsetningsåret, ikke i utbetalingsåret.** Bodil bokførte utbytte
  når pengene forlot konto. Det gjorde protokollen umulig å datere ærlig: den skrives
  våren året etter, men skulle «vedta» en utdeling som allerede hadde skjedd, og skillen
  lovet samtidig å være «det lovpålagte bilaget». Bodil følger nå aksjelovens normalsti.
  Styret foreslår utbyttet når regnskapet utarbeides, det står som `avsatt utbytte`
  (kortsiktig gjeld, konto 2800) per 31.12 og reduserer egenkapitalen i det året det
  gjelder, generalforsamlingen vedtar avsetningen når den godkjenner årsregnskapet, og
  utbetalingen året etter gjør bare opp gjelden. Alt Bodil produserer er dermed datert
  når det faktisk skjer.
- **To rader i den låste modellen er byttet ut.** «Penger ut til eier → utbytte» er delt
  i to: en utbetaling opp til utestående avsetning reduserer gjelden og rører ikke
  egenkapitalen, mens alt utover den blir **flagget**. Ny rad for selve avsetningen, som
  er den ene posten i modellen som ikke stammer fra bankeksporten, fordi den er en
  beslutning og ikke en betaling.
- **Penger til eier uten dekkende avsetning gjettes ikke lenger på.** Bodil spør om det
  er et utbytte vedtatt i løpet av året på grunnlag av fjorårets godkjente regnskap, et
  lån til aksjonær, eller en tilbakebetaling av innbetalt kapital. Det første føres som
  før (`utbytte_utbetalt`, reduserer egenkapitalen i utbetalingsåret) mot at brukeren
  bekrefter at det finnes et vedtak datert senest på betalingsdagen. De to andre er
  utenfor modellen og flagges.
- **`protokoll` tilbakedaterer ikke lenger et vedtak.** Er utbyttet allerede utbetalt i
  regnskapsåret, omtaler protokollen utdelingen som et faktum og sier eksplisitt at den
  ikke er bilaget for vedtaket, i stedet for å «vedta» den i ettertid. Skillen lager
  aldri et bilag den ikke kan datere riktig.
- **Dekningskravet gjelder nå avsetningen.** En avsetning er en utdeling etter
  aksjeloven § 8-1 og er allerede trukket fra annen egenkapital, så den kan gjøre fri
  egenkapital negativ helt alene. Sjekken så tidligere bare på utbetalt utbytte.
- **`regnskap.md` har fått en «Utbytte»-seksjon** som skiller inngående avsetning,
  utbetaling mot den, utbytte vedtatt og utbetalt i året, og årets avsetning. Den er
  input til `protokoll`, til `avsatt_utbytte` i `wenche-config`, og til neste års
  bokføring. `avsatt_utbytte` er også ny linje i balansen, og `aapningsbalanse` i
  `selskap.yaml` har fått feltet.
- **`avsatt_utbytte` og `utbytte_utbetalt` er bevisst to felt.** Det første er balansen
  og egenkapitalen i avsetningsåret; det andre er kontantstrømmen og posten i
  aksjonærregisteroppgaven i utbetalingsåret, jf. Wenches egen definisjon. De er ulik
  null samtidig det året fjorårets avsetning betales og et nytt utbytte avsettes, og
  `wenche-config` har et sjekklistepunkt mot forveksling.
- **Nytt fixture `tests/fixtures/config.avsatt-utbytte.yaml`** dekker nettopp den
  kombinasjonen: 10 000 utbetalt mot fjorårets avsetning og 8 000 avsatt for året.
  Avstemmingen viser `avsattEllerForventetUtbytte` 8 000 og ingen utbyttepost for
  utbetalingen, som er oppførselen Wenche 1.5.1 retter. Gaten dekker nå fire fixtures,
  og `config.golden.yaml` beholdes uendret som dekning for utbetalingsstien.
- Sperren mot å gå til 1.0 i `release`-skillen er fjernet. Avviket om rentebærende
  aksjonærlån som gjorde den nødvendig er avklart.

**Overgang:** det første året etter oppgraderingen finnes det ingen inngående avsetning,
så en utbetaling til eier vil bli flagget. Det er tilsiktet. Svar «utbytte vedtatt i
året» hvis utdelingen hadde et gyldig vedtak, så føres den som før. Fra året etter er du
på normalstien. Balansen for tidligere år endres ikke, og ingenting må sendes inn på
nytt.

**Testet mot Wenche ≥ 1.5.1.**

## [0.6.0]

- **Utbetalt utbytte får riktig kode hos Skatteetaten.** Wenche 1.4.0 har fått avklart
  at samleposten «andre negative endringer i egenkapital» ikke skal brukes ved utdeling
  av utbytte, og koder nå utbetalingen som `tilleggsutbytte`: utdeling i løpet av året
  basert på sist godkjente årsregnskap, som er nøyaktig det Bodils modell produserer.
  Golden-fixturet gikk fra `annenNegativEndringIEgenkapital` til `tilleggsutbytte` uten
  at en eneste linje i Bodils output endret seg. Alle som har delt ut utbytte fra et
  Bodil-ført regnskap har sendt inn med den avviste samleposten; det retter seg ved å
  bumpe pinnet Wenche, ingenting annet må gjøres.
- **Selskap stiftet ved tinginnskudd kan nå rapportere det.** Skytes aksjer i et annet
  selskap inn som aksjekapital, som er en vanlig måte å etablere en holdingstruktur på,
  rapporterte egenkapitalavstemmingen hele stiftelsesinnskuddet som kontantinnskudd i
  første regnskapsår. Det nye, valgfrie feltet `tinginnskudd_ved_stiftelse` i
  `selskap.yaml` oppgir tingdelen, og kontantinnskuddet blir resten. Feltet kan ikke
  utledes fra bankeksporten, siden et tinginnskudd aldri går gjennom bankkontoen, så
  `wenche-config` fører det opp i sjekklisten over manuelle poster. Det gjelder bare
  første regnskapsår; senere år ignorerer Wenche det med en advarsel.
- **Gaten dekker nå tre former** Bodil kan produsere: nytt fixture
  `tests/fixtures/config.tinginnskudd.yaml` for et delt stiftelsesinnskudd (25 000 som
  aksjer, 5 000 som penger), som tvinger både `tinginnskudd` og `kontantinnskudd` ut i
  avstemmingen.
- Pinnet Wenche bumpet fra 1.3.1 til 1.5.1. Ingen feltnavn Bodil bruker er fjernet eller
  døpt om. Wenche 1.5.0 la til `avsatt_utbytte` for utbytte som avsettes i regnskapet og
  utbetales året etter; Bodil bruker det ikke i denne versjonen, siden den låste modellen
  fører utbytte når pengene forlater konto.

**Testet mot Wenche ≥ 1.5.1.**

## [0.5.0]

- **Skattekostnad er nå en del av den låste modellen.** Bodil regnet årsresultatet
  som utbytte minus driftskostnader, altså implisitt skattekostnad 0. Det stemmer
  for et hvilende år, men et år med mottatt utbytte og eierandel under 90 % har en
  reell skattepliktig inntekt gjennom 3 %-sjablonen i fritaksmetoden (sktl. § 2-38
  sjette ledd), og regnskapsloven § 6-1 krever skattekostnaden som egen linje før
  årsresultatet. Årsresultatet ble dermed rapportert for høyt, og Wenche varslet
  «skatten er beregnet, men ikke ført». `bokforing` regner nå skatten etter samme
  regel som Wenche (skattepliktig del av utbyttet minus driftskostnader, minus
  fremført underskudd, ganget med 22 %), og fører `betalbar_skatt` som motpost i
  balansen. Golden-fixturet gikk fra ført 0 mot beregnet 55 kr til avvik 0.
- **Betaling av skatt har fått sin egen rad i modellen.** Uten den ville
  innbetalingen til Skatteetaten året etter blitt klassifisert som driftskostnad og
  dermed kostnadsført to ganger. Den reduserer nå betalbar skatt.
- **`regnskap.md` har en ny «Skattemessig»-seksjon** med skattepliktig inntekt,
  anvendt fremført underskudd og underskudd til fremføring neste år. Den er input
  til neste års bokføring og til `underskudd_til_fremfoering` i `wenche-config`,
  som tidligere måtte hentes manuelt fra RF-1028 hvert år.
- **`selskap.stiftelsesdato` tas nå med når den er kjent.** Uten den oppgir
  aksjonærregisteroppgaven 1. januar som stiftelsestidspunkt for de nyutstedte
  aksjene. Feltet er lagt til i `selskap.example.yaml` (hentes fra Enhetsregisteret).
- **Forlenget første regnskapsår støttes** via `regnskapsstart` og `regnskapsslutt`
  i `wenche-config`. Et selskap stiftet sent på året kan la første regnskapsår løpe
  i inntil 18 måneder (rskl. § 1-7 andre ledd); Bodil oppgav tidligere hele
  kalenderåret uansett.
- **Kompatibilitetsgaten dekker nå begge formene** Bodil kan produsere: nytt fixture
  `tests/fixtures/config.foerste-aar.yaml` for det forlengede første regnskapsåret,
  og både validering og feltnavn-lint kjører over alle fixtures i `tests/fixtures/`
  i stedet for bare golden-fixturet.
- Pinnet Wenche bumpet fra 0.31.2 til 1.3.1. Ingen feltnavn Bodil bruker er fjernet
  eller døpt om i 1.x; hele endringen over handler om felt Bodil ikke utnyttet.

**Testet mot Wenche ≥ 1.3.1.**

## [0.4.2]

- CI-workflowene (`docs.yml`, `wenche-kompatibilitet.yml`) kjører nå kun i
  Bodils eget repo (`if: github.repository == 'olefredrik/Bodil'`). Template-
  kopier som har hentet inn `.github/` får dem dermed hoppet over i stedet for å
  feile med e-postvarsel ved hver push.
- Oppdateringsoppskriften (`docs/oppdatere.md`) henter ikke lenger inn `.github`,
  og forklarer hvorfor Bodils CI ikke hører hjemme i en regnskapskopi (+ hvordan
  rydde hvis den allerede er hentet inn). Eksempelversjonen er oppdatert.

**Testet mot Wenche ≥ 0.31.2.**

## [0.4.1]

- Tydeligere veiledning for Folio-integrasjonen: `folio-import`-skillen og docs
  forklarer nå steg for steg hvordan API-nøkkelen lages (Lesetilgang på
  app.folio.no/til/api-tilgang) og legges i en `.env`-fil, og feilmeldingen ved
  manglende nøkkel er gjort handlingsrettet.
- Språk: «lese-only» erstattet med «kun lesing» i skill, skript og docs.

**Testet mot Wenche ≥ 0.31.2.**

## [0.4.0]

- Hostet Wenche ([wenche.cloud](https://wenche.cloud)) er nå den anbefalte
  innsendingsveien i dokumentasjon og skills: brukeren laster opp `config.yaml`
  via **Tall → Hent tall fra Bodil**, uten å installere noe. Self-hosted lokalt
  er fortsatt et likeverdig alternativ.
- `wenche-config` krever ikke lenger at Wenche er installert. Lokal validering
  (`wenche valider-aarsregnskap`) kjøres hvis kommandoen finnes, ellers skjer
  valideringen ved opplasting på wenche.cloud. Senker terskelen for web-brukere.
- Personvern-note: `config.yaml` inneholder fødselsnummer, som forlater maskinen
  ved opplasting til wenche.cloud (behandles kun i økten, ikke lagret).
- Release-badgen i README er nå statisk (`badge/release-vX.Y.Z`) i stedet for
  `github/v/release`, som intermitterende feilet med «Unable to select next
  GitHub token from pool» fra shields.io.
- Forenklet release-prosess: versjon og badge navngis nå i selve feature-PR-ene
  (entry under `## [X.Y.Z]`), så `/release` er bare en tag + GitHub Release,
  ingen egen versjons-bump-PR.

**Testet mot Wenche ≥ 0.31.2.**

## [0.3.0]

- Verifisert kompatibilitet med Wenche 0.31.2 og bumpet pinnet versjon fra 0.24.0.
  Feltnavnene i `config.yaml` og kommandoen `wenche valider-aarsregnskap` er
  uendret i 0.31.2; golden-fixturet validerer fortsatt grønt, så ingen
  skill-endring var nødvendig.
- Ny valgfri skill `folio-import`: henter et regnskapsårs transaksjoner fra
  Folio (api.folio.no/v2, lese-only) og skriver `<år>/bankeksport.csv`. Erstatter
  kun det manuelle CSV-nedlastingssteget; alt nedstrøms er uendret. Kun stdlib,
  kun GET-kall, aldri `/payments`, API-nøkkel fra `.env`.
- `scripts/sync-from-bodil`: synker verktøy-allowlisten (ikke data) til en privat
  kopi av malen, pinnet til en Bodil-tag, med en deny-list som nekter å røre
  `selskap.yaml`, `*/config.yaml`, `*/bankeksport.csv` og `*/bilag/`.
- Folio-importørens rene logikk dekkes av `tests/test_folio_import.py`, som kjører
  i CI-gaten sammen med Wenche-valideringen og feltnavn-linten.
- Kompatibilitets-gaten kjører nå også på push til main, så Actions-badgen i
  README reflekterer mains faktiske Wenche-kompatibilitet.
- README: badges (release, lisens, status, CI, Claude Code) og tydeliggjort at
  Bodil forutsetter tilgang til Claude (den eneste kostnaden; verktøyene er gratis).

**Testet mot Wenche ≥ 0.31.2.**

## [0.2.0]

- `/release` automatiserer nå tagging og release notes: henter noten fra
  CHANGELOG og kjører tag + GitHub Release etter én bekreftelse.
- CI feiler nå hvis `WENCHE_PINNET` ikke matcher «Testet mot Wenche ≥ …» i
  CHANGELOG, så de to kan ikke drifte fra hverandre.
- CLAUDE.md-regel: hver oppførselsendrende PR oppdaterer `[Ikke utgitt]`.
- Den ukentlige kjøringen mot nyeste Wenche oppretter nå en GitHub-issue ved
  brudd (med duplikat-vern), i stedet for bare en passiv annotering.

**Testet mot Wenche ≥ 0.24.0.**

## [0.1.0]

Første versjonerte utgave.

- Tre skills for bokføring, protokoll og Wenche-config for passive holdingselskaper.
- Automatisk kompatibilitetstest mot Wenche: golden-fixture valideres med
  `wenche valider-aarsregnskap`, og en feltnavn-lint sjekker at Bodils feltnavn
  finnes i Wenches datamodell. Kjører som PR-gate (pinnet) og ukentlig (nyeste).
- Rettet feltnavn i wenche-config: `eierandel_datterselskap` →
  `eierandel_for_fritaksmetoden` (Wenche leste aldri det gamle navnet, så
  eierandel under 90 % ble feilaktig behandlet som fullt skattefritt utbytte).

**Testet mot Wenche ≥ 0.24.0.**

[1.2.0]: https://github.com/olefredrik/Bodil/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/olefredrik/Bodil/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/olefredrik/Bodil/compare/v0.6.0...v1.0.0
[0.6.0]: https://github.com/olefredrik/Bodil/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/olefredrik/Bodil/compare/v0.4.2...v0.5.0
[0.4.2]: https://github.com/olefredrik/Bodil/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/olefredrik/Bodil/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/olefredrik/Bodil/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/olefredrik/Bodil/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/olefredrik/Bodil/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/olefredrik/Bodil/releases/tag/v0.1.0
