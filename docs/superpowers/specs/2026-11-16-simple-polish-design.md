# Simple Polish — projekt skilla

Data: 2026-11-16
Status: zaakceptowany, gotowy do planowania

## 1. Cel

Skill dla Claude Code i innych agentów. Ma sprawić, że agent pisze po polsku
tak, żeby zleceniodawca rozumiał, co się stało, bez czytania kodu.

Skill obsługuje trzy rejestry: dokument, odpowiedź i raport z pracy. Raport
z pracy jest nowością. Żaden z trzech zbadanych projektów go nie ma.

## 2. Problem

Cytat użytkownika:

> często claude code opisuje mi swoją pracę tak, że nic nie rozumiem, mimo
> że to ja zlecam mu projekt

Objawy, które chcemy usunąć:

- agent opisuje pliki i funkcje zamiast skutków
- żargon techniczny bez wyjaśnienia
- decyzja schowana na końcu albo nieobecna
- brak informacji, czego agent nie sprawdził

Luka w istniejących projektach. `SimpleEnglish`, `asd-ste100-skill`
i `prosta-polszczyzna` przepisują dokumenty. Żaden nie opisuje pracy agenta
w trakcie sesji. Ten skill celuje właśnie w ten przypadek.

## 3. Odbiorca

Osoba decydująca, nieimplementująca. Nie czyta kodu. Chce wiedzieć:

- co to znaczy dla projektu
- co ma zrobić
- jak bardzo można zaufać wynikowi

Nie interesują jej ścieżki plików, nazwy funkcji ani numery linii.

## 4. Zakres

Praca idzie w trzech fazach. Każda faza działa samodzielnie.

| Faza | Zawartość | Kryterium gotowości |
|---|---|---|
| 1. Prompt | `SKILL.md`, `references/`, `tests/test_skill_md.py`, `README.md` | da się zainstalować i używać bez lintera |
| 2. Linter | `scripts/`, `scripts/data/`, `tests/` | `--selftest` przechodzi, fixture'y mają znaną liczbę znalezisk |
| 3. Ewaluacja i dystrybucja | `evals/`, `src/hooks/`, `.claude-plugin/`, CI | wyniki w repo, hook doradczy, plugin instalowalny |

Poza zakresem:

- upraszczanie treści merytorycznej
- ocena poprawności kodu
- ocena prawdziwości twierdzeń
- certyfikacja zgodności z ISO 24495-1
- język angielski

## 5. Tryby pracy

| Tryb | Kiedy | Co rządzi tekstem |
|---|---|---|
| **Dokument** | tekst, który zostaje: README, mail, release notes, UI, commit, opis PR, komunikat błędu | standard 2024 i twarde limity |
| **Odpowiedź** | rozmowa: pytanie, wyjaśnienie, dyskusja | odpowiedź w pierwszym zdaniu, proza, bez bolda, bez otwarć i zamknięć, terminy wyjaśniane |
| **Raport z pracy** | tylko gdy agent wykonał akcje i zdaje sprawę: po edycji plików, po serii narzędzi, albo gdy użytkownik pyta „co zrobiłeś", „co się zmieniło", „na czym stanęło" | układ pięcioczęściowy |

Trzy reguły trzymają całość:

1. W razie wątpliwości wybierz **Odpowiedź**. Układ pięcioczęściowy jest drogi
   i opłaca się tylko wtedy, gdy jest o czym raportować.
2. **Raport skaluje się do wagi pracy.** Drobna zmiana dostaje trzy części:
   skutek, decyzja, pewność. Kilka plików albo ryzyko regresji dostaje pełne
   pięć.
3. **Tryb nie zmienia faktów.** Żadna reguła nie pozwala pominąć ostrzeżenia
   o akcji nieodwracalnej ani dopisać twierdzenia, którego agent nie sprawdził.

## 6. Raport z pracy

Układ: **skutek → co się zmieniło → co to znaczy dla projektu → decyzja →
pewność**.

Pochodzenie części: pierwsze zdanie jako skutek pochodzi z BLUF
(`prosta-polszczyzna/SKILL.md:35`). Kolejność „co się zmieniło" przed „co to
znaczy" pochodzi z Top-Down Bridge (`prosta-polszczyzna/SKILL.md:43`).
Wycięcie ścieżek i nazw funkcji pochodzi z Just-in-Time Context
(`prosta-polszczyzna/SKILL.md:39`, `SimpleEnglish/skills/simple-english/SKILL.md:32`).
Proza bez bolda pochodzi z `SimpleEnglish/skills/simple-english/SKILL.md:61-68`.

Część „Pewność" jest własna. Żaden z trzech projektów nie każe modelowi
powiedzieć, czego nie sprawdził.

Przykład wzorcowy:

> Logowanie działa teraz stabilniej i łatwiej je później zmieniać.
>
> Co się zmieniło: sprawdzanie tokenów jest w jednym miejscu, a nie rozproszone
> po kilku plikach.
>
> Co to znaczy dla projektu: stara ścieżka logowania przestanie działać. Nie
> używamy jej od dawna, więc nic nie tracimy.
>
> Co masz zrobić: nic. Jeśli chcesz, mogę usunąć starą ścieżkę.
>
> Pewność: testy przechodzą, ale nie sprawdzałem tego na prawdziwym ruchu.

Reguła dla „Pewność": rozdzielaj **sprawdzone** (uruchomiony test, przeczytany
plik, wykonane polecenie) od **założonego**. Agent nie pisze „działa", jeśli
niczego nie uruchomił.

## 7. Reguły twarde

Mechaniczne. Model stosuje je zawsze, bez wyjątku poza słownikiem domenowym.

Identyfikatory są kanoniczne. Wspólne z linterem: `bezosobowe`
i `rama-analityczna`. Pozostałe sprawdza tylko model.

| ID | Reguła | Przykład naruszenia |
|---|---|---|
| `jedna-mysl` | Jedno zdanie = jedna myśl | zdanie z „a także" i drugim orzeczeniem w środku |
| `wyliczenie-lista` | 4 lub więcej elementów wyliczenia zapisz jako listę pionową | „obsługuje A, B, C, D i E" w jednym zdaniu |
| `podwojna-negacja` | Bez podwójnej negacji | „nie jest nieprawdą" |
| `bezosobowe` | Bez `-no/-to` i „zaleca się" | „zostało ustalone", „zaleca się sprawdzić" |
| `lancuch-dopelniaczowy` | Bez łańcuchów dopełniaczowych dłuższych niż dwa rzeczowniki | „umożliwienie spłaty raty kredytu" |
| `rama-analityczna` | Bez ram analitycznych | „dokonać oceny", „przeprowadzić weryfikację" |
| `warunek-najpierw` | Warunek przed poleceniem | „Złóż wniosek, jeśli…" zamiast „Jeśli…, złóż wniosek" |
| `termin-przy-pierwszym-uzyciu` | Termin wyjaśniony przy pierwszym użyciu | „idempotentny" bez objaśnienia |
| `fakty-nietkniete` | Fakty, liczby, nazwy, cytowane błędy i kod pozostają nietknięte | — |
| `ostrzezenie-zawsze` | Ostrzeżenie o akcji nieodwracalnej zostaje zawsze | — |

## 8. Progi i tolerancje

Limity mają kierunek i tolerancję, nie zerojedynkowy próg.

- 20 słów to cel dla instrukcji, 25 dla opisu. Między 20 a 25 tniemy tylko
  zdanie z dwiema myślami. Powyżej 25 tniemy zawsze.
- W trybie odpowiedzi limit jest luźniejszy: 30 słów. Odpowiedź musi czasem
  zmieścić warunek i skutek w jednym zdaniu.
- Akapit ma 3 do 5 zdań. Sześć i więcej to sygnał, nie błąd.
- Strona bierna jest dozwolona, gdy wykonawca jest nieznany albo nieistotny.
- Imiesłowy `-ąc` i rzeczowniki odczasownikowe są dozwolone, gdy są terminem:
  *ustawienie, wymaganie, jakość, konfiguracja*.
- Myślnik jest dozwolony dla dopowiedzeń. Nadmiar jest sygnałem.
- Nadrzędna zasada ze standardu 2024: 19 słów nie zawsze jest lepsze od 21.

## 9. Reguły doradcze

Model stosuje je świadomie. Linter je sygnalizuje, ale nigdy nie zmienia przez
nie kodu wyjścia.

- nominalizacje powyżej progu gęstości
- żargon bez wyjaśnienia
- anglicyzmy i słabo przyswojone zapożyczenia
- wyrazy modne: *dedykowany, innowacyjny, unikalny, kompleksowy*
- „się" bezosobowe
- przymiotniki marketingowe
- rotacja synonimów: jedno pojęcie, jedno słowo
- otwarcia i zamknięcia w trybie odpowiedzi: „Świetne pytanie", „Mam nadzieję,
  że to pomoże"
- nadmiar bolda i wyróżnień graficznych

## 10. Granice

- Skill zmienia formę, nie treść.
- Nie upraszcza zastrzeżeń prawnych ani warunków bezpieczeństwa.
- Nie podnosi niepewności do pewności i nie usuwa hedgingu.
- Jeśli tekst już spełnia reguły, agent mówi to jednym zdaniem i nic nie
  przepisuje.
- Agent nie komentuje przepisania, chyba że tryb tego wymaga.

## 11. Struktura plików

```
simple-polish/
├── SKILL.md                  # rdzeń promptu, około 150 linii, trzy tryby inline
├── references/
│   ├── tryby.md              # rozwinięcie: kiedy Dokument / Odpowiedź / Raport
│   ├── reguly.md             # reguły 2024 i 2016 pogrupowane wg zadania
│   ├── zamienniki.md         # słowo → prostsze, na bazie słowników ze źródeł
│   ├── styl-agenta.md        # jak opisywać pracę: przykład zły i dobry
│   └── przyklady.md          # before/after dla trzech trybów
├── scripts/
│   ├── lint.py               # linter, stdlib, dwa poziomy
│   └── data/                 # wyjatki.txt, terminy.txt, zamienniki.tsv,
│                             # synonimy.tsv, przymiotniki.tsv
├── tests/                    # fixture'y i test_lint.py
├── evals/                    # scenariusze, runner, rubryka, wyniki
├── src/hooks/                # hooki doradcze
├── simple-polish.json        # konfiguracja użytkownika, opcjonalna
├── .claude-plugin/plugin.json
├── .gitignore
├── LICENSE
└── README.md
```

Decyzje strukturalne:

1. `SKILL.md` leży w katalogu głównym, tak jak w `prosta-polszczyzna`
   i `asd-ste100-skill`. Dzięki temu `npx skills add` działa bez dodatkowej
   konfiguracji. Trzy sklonowane repozytoria zostają w miejscu i trafiają do
   `.gitignore`.
2. Referencje dzielimy według zadania, nie według źródła. Modelowi nie zależy,
   skąd pochodzi reguła. Źródło podajemy w nawiasie przy regule.
3. `zamienniki.md` piszemy od zera. Nie kopiujemy 370 wierszy z
   `prosta-polszczyzna`, bo tabela ma duplikaty i kategorie bez pokrycia
   w standardzie. Bierzemy sprawdzone pary i podajemy autorstwo w README.
4. Dwa poziomy reguł są jawne w promptcie i w linterze. Kod wyjścia zależy
   wyłącznie od reguł twardych.
5. Myślnik zostaje. `SimpleEnglish` banuje `—` jako cechę tekstu pisanego przez
   AI. Standard PPP 2016, zasada 8, każe oznaczać dopowiedzenia myślnikiem.
   Banujemy nadmiar, nie znak. Kopiowanie reguł z angielskiego wprost dałoby
   skill sprzeczny z polskim źródłem.

## 12. Linter

`scripts/lint.py`, Python 3, tylko biblioteka standardowa. Poziom lintera nie
musi być równy poziomowi promptu. Gdy regex nie sięga precyzją, reguła spada do
doradczej.

Reguły pewne, decydują o kodzie wyjścia:

| ID | Wzorzec |
|---|---|
| `rama-analityczna` | dokonać, dokonuje, przeprowadzić + rzeczownik; w celu, w wyniku, w razie, na skutek, w zakresie, w ramach, pod kątem, w oparciu o, za pomocą |
| `bezosobowe` | zaleca się, należy, powinno się, winno się, można, trzeba, warto, na początku zdania lub po przecinku |
| `wyliczenie` | 4 lub więcej elementów rozdzielonych przecinkami przed „i" albo „oraz" |
| `dlugosc-zdania` | powyżej 25 słów w dokumencie, powyżej 30 w odpowiedzi |

Reguły warunkowe, doradcze:

- `-no/-to`, tylko wzorce `-ano`, `-ono`, `-ięto`, `-nięto`, `-yto`, poza listą
  wyjątków
- łańcuchy dopełniaczowe, heurystyka: trzy lub więcej wyrazów zakończonych na
  `-y`, `-i`, `-u`, `-ą` po rzeczowniku odczasownikowym
- podwójna negacja w jednym zdaniu
- strona bierna: `zostać` albo `być` z imiesłowem
- imiesłowy `-ąc`
- gęstość nominalizacji powyżej trzech na 100 słów
- gęstość myślników powyżej dwóch na 100 słów
- przymiotniki marketingowe
- rotacja synonimów
- otwarcia i zamknięcia w trybie odpowiedzi
- bold w trybie odpowiedzi

Tokenizacja jest trudniejszym fragmentem niż same reguły. Przed cięciem zdania
chronimy:

- skróty: np., itd., itp., tj., tzn., tzw., m.in., art., ust., pkt, dr, prof.,
  nr, str., r., w., godz.
- liczby dziesiętne
- adresy
- bloki kodu, inline code, tabele

Bez tego każde zdanie z „np." rozpadnie się na dwa i limity długości zaczną
kłamać.

Interfejs:

```
python scripts/lint.py PLIK...
python scripts/lint.py --mode odpowiedz
python scripts/lint.py --json
python scripts/lint.py --baseline 3
python scripts/lint.py --disable rama-analityczna,wyliczenie
python scripts/lint.py --selftest
```

Wyjście w formie `plik:linia  id-reguły  „fragment"  →  „propozycja"`. Kod
wyjścia 1 wyłącznie przy regułach twardych ponad baseline.

Dane leżą w `scripts/data/` jako pliki tekstowe, edytowalne bez ruszania kodu.
Konfiguracja przez `simple-polish.json`: nadpisanie poziomów i wyłączanie reguł.

Morfologia jest opcjonalna. Aspekt i przypadki wymagają analizatora, na przykład
spaCy `pl_core_news_sm`. Wchodzi za flagą `--morphology` jako zależność
opcjonalna. Domyślna ścieżka zostaje bez instalacji.

Czego linter nie sprawdza i nie będzie: prawdziwości, znaczenia, trafności
terminu dla domeny, liczby myśli w zdaniu. To zostaje modelowi.

## 13. Ewaluacja

Dwie miary, bo jedna kłamie.

Miara deterministyczna: ten sam tekst przed i po, liczony linterem. Twarde
znaleziska na 1000 słów, średnia długość zdania, gęstość nominalizacji. Bez
modelu w pętli, więc wynik jest powtarzalny.

Miara sędziowska: osobny model ocenia odpowiedź w skali 1–5 na pięciu
kryteriach:

1. czy pierwsze zdanie mówi, o co chodzi
2. czy tekst jest zrozumiały bez czytania kodu
3. czy żargon jest wyjaśniony
4. czy fakty zgadzają się z materiałem wejściowym
5. czy wiadomo, co dalej

Rubryka leży w `evals/rubric.md`, żeby dało się ją zakwestionować.

Scenariusze w `evals/scenarios/`, czternaście: raport po edycji
pliku, raport po nieudanym teście, „co zrobiłeś w tej sesji", odpowiedź na
pytanie o architekturę, wyjaśnienie błędu, README, komunikat błędu, commit, opis
PR, mail, notatka o decyzji, odpowiedź na pytanie „czy to bezpieczne",
objaśnienie pipeline'u, objaśnienie jednej funkcji.

Uruchomienie: `evals/run.py` woła `claude -p` dla scenariusza, warunku (bez
skilla i ze skillem) i przebiegu, po czym zapisuje surowe wyjścia.
`evals/score.py` liczy obie miary. `evals/check_numbers.py` przelicza każdą
liczbę z README i z wyników na podstawie surowych plików. Jeśli README kłamie,
CI się wywala.

Czego nie zmierzymy, a co wpiszemy do README: prawdziwego zrozumienia. To
wymaga czytelników, nie modelu. Do tego jeden sędzia, możliwa stronniczość
rodzinowa i jeden przebieg na komórkę.

## 14. Hooki

Hooki są doradcze, nigdy blokujące.

- Start sesji wstrzykuje skondensowany prompt.
- Po zapisie pliku `.md` linter zwraca do 12 znalezisk.
- Po zakończeniu odpowiedzi sprawdzamy tekst asystenta regułami trybu
  odpowiedzi i wysyłamy uwagę.

Kod wyjścia zawsze 0. Ścieżki wykluczone przez `SIMPLE_POLISH_EXCLUDE`. Zero
zależności.

## 15. Pakowanie i CI

- `plugin.json` i marketplace jak w `SimpleEnglish`.
- Licencja MIT.
- README z sekcją „skąd pochodzą reguły" i podaniem autorstwa
  `prosta-polszczyzna` za zamienniki.
- CI: Python 3.12 i 3.13, `--selftest`, `tests/`, `check_numbers.py`.
- `check_numbers.py` sprawdza też zgodność identyfikatorów reguł w `SKILL.md`
  i w `lint.py`. Bez tego prompt i linter rozjadą się po dwóch miesiącach.

## 16. Ryzyka

- Regex na polskiej fleksji będzie dawał fałszywe alarmy. Ratuje nas podział na
  poziomy i baseline, nie idealna precyzja.
- Biała lista terminów wymaga utrzymania i nigdy nie będzie pełna.
- Skill może upraszczać kosztem precyzji technicznej. Dlatego blok „granice"
  jest twardy i nienegocjowalny.
- Ewaluacja mierzy styl, nie zrozumienie.

## 17. Kryteria akceptacji

Faza 1:

- `SKILL.md` mieści się w 150 liniach i zawiera wszystkie trzy tryby.
- Każda reguła twarda ma przykład naruszenia w `references/przyklady.md`.
- README mówi, czego skill nie robi.

Faza 2:

- `--selftest` przechodzi.
- Fixture z dokładnie dwoma znaleziskami daje dokładnie dwa.
- Plik bez naruszeń daje kod wyjścia 0.
- Reguła doradcza nigdy nie zmienia kodu wyjścia.

Faza 3:

- Czternaście scenariuszy ma surowe wyniki w repo.
- Każda liczba w README ma pokrycie w `check_numbers.py`.
- Hook nie blokuje zapisu pliku.
- Plugin instaluje się przez `npx skills add`.

## 18. Pochodzenie reguł

- Ustandaryzowane zasady prostego języka, 2024, sześć zasad. Podstawa trybu
  Dokument.
- Standard PPP UWr 2016, trzydzieści zasad. Uzupełnienie i uzasadnienie.
- `prosta-polszczyzna` (kashiash, MIT): BLUF, Top-Down Bridge, Just-in-Time
  Context, wzorce zamienników.
- `SimpleEnglish` (AminBlg, MIT): podział na rejestry, samokontrola, dyscyplina
  wyjścia, pomysł na linter i ewaluację.
- `asd-ste100-skill` (danyuchn, MIT): rozdzielenie trybu strict i flavored,
  poziomy reguł, formuła „forma, nie treść".

## 19. Odrzucone podejścia

- **Pasywny skill bez egzekwowania.** Odrzucony, bo model zapomina reguł
  w długiej sesji. Hooki z fazy 3 mają to naprawić.
- **Dwa osobne skille, dokument i odpowiedź.** Odrzucony, bo użytkownik wybrał
  jeden skill z trybami. Trzy tryby w jednym pliku są tańsze w utrzymaniu.
- **Zakaz końcówek `-anie, -enie, -cie, -acja, -sja, -zja, -ość`.** Odrzucony
  po sprzeciwie użytkownika. Dawałby masowe fałszywe alarmy, a standard 2024
  w zasadzie 6 sam zakazuje takiego absolutyzmu. Zamiast tego wykrywamy
  konstrukcję i gęstość.
- **Ban na myślnik, przeniesiony z `SimpleEnglish`.** Odrzucony, bo standard
  PPP 2016, zasada 8, każe używać myślnika w dopowiedzeniach.
- **Kopiowanie tabeli 370 zamienników.** Odrzucony z powodu duplikatów
  i kategorii bez pokrycia w standardzie.
