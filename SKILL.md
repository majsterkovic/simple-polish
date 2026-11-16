---
name: simple-polish
description: "Pisze po polsku prosto i konkretnie. Uzywaj przy kazdym tekscie po polsku: dokumentacji, mailach, commitach, komunikatach bledow, a przede wszystkim gdy opisujesz wykonana prace. Triggery: prosty jezyk, jasnopis, nie rozumiem, opisz mi to, co zrobiles."
---

# Simple Polish

Piszesz po polsku tak, żeby zlecający zrozumiał wynik bez czytania kodu.

## Trzy tryby

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

## Raport z pracy

Układ: skutek → co się zmieniło → co to znaczy dla projektu → decyzja
(„Co masz zrobić") → pewność.

Pierwsze zdanie mówi, co się zmieniło z punktu widzenia projektu. Nie mówi,
które pliki ani funkcje ruszyłeś.

Etykiety części piszesz zwykłym tekstem z dwukropkiem: Co się zmieniło:,
Co to znaczy dla projektu:, Co masz zrobić:, Pewność:. Raport jest prozą,
bez bolda i bez nagłówków.

W „Co się zmieniło" opisujesz zmianę zachowania, nie listę plików. Pliki
i funkcje podajesz tylko wtedy, gdy czytelnik musi coś z nimi zrobić.

> Logowanie działa teraz stabilniej i łatwiej je później zmieniać.
>
> Co się zmieniło: sprawdzanie tokenów jest w jednym miejscu, a nie rozproszone
> po kilku plikach.
>
> Co to znaczy dla projektu: stara ścieżka logowania przestanie działać.
>
> Co masz zrobić: nic. Jeśli chcesz, mogę usunąć starą ścieżkę.
>
> Pewność: testy przechodzą, ale nie sprawdzałem tego na prawdziwym ruchu.

Część „pewność" rozdziela sprawdzone od założonego. Sprawdzone to uruchomiony
test, przeczytany plik, wykonane polecenie. Założone to reszta. Nie piszesz
„działa", jeśli niczego nie uruchomiłeś.

Rozwinięcie i przykłady: `references/styl-agenta.md`.

## Reguły twarde

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

Reguły są mechaniczne. Stosujesz je w każdym trybie. Wyjątek to słownik
domenowy: termin, który jest najprostszym słowem dla rzeczy, zostaje.

## Progi, nie zakazy

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

## Reguły doradcze

Stosujesz je świadomie. Nie są powodem, żeby przepisać dobry tekst.

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

Szczegóły i tabele zamienników: `references/reguly.md`, `references/zamienniki.md`.

## Granice

- Skill zmienia formę, nie treść.
- Nie upraszcza zastrzeżeń prawnych ani warunków bezpieczeństwa.
- Nie podnosi niepewności do pewności i nie usuwa hedgingu.
- Jeśli tekst już spełnia reguły, powiedz to jednym zdaniem i nic nie
  przepisuj.
- Nie komentujesz przepisania, chyba że tryb tego wymaga.

Kiedy sięgnąć po referencję:

- nie wiesz, który tryb wybrać, albo piszesz raport — `references/tryby.md`
- potrzebujesz uzasadnienia reguły albo pełnej listy zasad — `references/reguly.md`
- szukasz prostszego zamiennika — `references/zamienniki.md`
- opisujesz wykonaną pracę — `references/styl-agenta.md`
- chcesz zobaczyć before/after — `references/przyklady.md`
