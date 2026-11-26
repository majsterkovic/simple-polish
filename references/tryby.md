# Tryby pracy

## Jak wybrać tryb

Zadaj dwa pytania po kolei. Pierwsza odpowiedź „tak" rozstrzyga.

1. Czy właśnie wykonałem akcje i zdaję z nich sprawę? Po edycji plików, po
   serii narzędzi, które coś zmieniły, albo gdy użytkownik pyta „co zrobiłeś",
   „co się zmieniło", „na czym stanęło". Jeśli tak, pisz w trybie
   **Raport z pracy**.
2. Czy tekst zostaje na stałe? README, mail, commit, release notes, komunikat
   błędu, opis PR. Jeśli tak, pisz w trybie **Dokument**.

W każdym innym przypadku, także w razie wątpliwości, pisz w trybie
**Odpowiedź**: pytanie, wyjaśnienie, dyskusja, „dlaczego tak".

## Tabela trybów

| Tryb | Kiedy | Co rządzi tekstem |
|---|---|---|
| **Dokument** | tekst, który zostaje: README, mail, release notes, UI, commit, opis PR, komunikat błędu | standard 2024 i twarde limity |
| **Odpowiedź** | rozmowa: pytanie, wyjaśnienie, dyskusja | odpowiedź w pierwszym zdaniu, proza, bez bolda, bez otwarć i zamknięć, terminy wyjaśniane |
| **Raport z pracy** | tylko gdy agent wykonał akcje i zdaje sprawę: po edycji plików, po serii narzędzi, albo gdy użytkownik pyta „co zrobiłeś", „co się zmieniło", „na czym stanęło" | układ pięcioczęściowy |

## Trzy reguły trzymające całość

**W razie wątpliwości wybierz Odpowiedź.** Układ pięcioczęściowy jest drogi.
Płacisz za niego uwagą czytelnika i długością tekstu. Opłaca się tylko wtedy,
gdy jest o czym raportować. Odpowiedź na pytanie „czy to bezpieczne" nie
potrzebuje pięciu części, bo nie zmieniłeś żadnego pliku.

**Raport skaluje się do wagi pracy.** Drobna zmiana dostaje trzy części:
skutek, decyzja, pewność. Kilka plików albo ryzyko regresji dostaje pełne
pięć. Skala jest po to, żeby raport o zmianie przecinka nie wyglądał jak
raport o migracji bazy. Nadużywany układ pięcioczęściowy przestaje być
czytany.

**Tryb nie zmienia faktów.** Żadna reguła nie pozwala pominąć ostrzeżenia
o akcji nieodwracalnej ani dopisać twierdzenia, którego agent nie sprawdził.
Skrót jest dozwolony w formie, nie w treści. Jeśli w źródle jest warunek,
zastrzeżenie albo liczba, zostaje w tekście po przepisaniu.

## Skalowanie raportu

| Waga pracy | Części |
|---|---|
| jedna drobna zmiana, jeden plik, brak ryzyka | trzy: skutek, decyzja, pewność |
| kilka plików albo ryzyko regresji | pięć: skutek, co się zmieniło, co to znaczy dla projektu, decyzja, pewność |

Zmiana nieodwracalna i decyzja do podjęcia przez człowieka dostają pełne pięć
części także wtedy, gdy dotyczą jednego pliku.

## Przykład wzorcowy

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

Pierwsze zdanie mówi, co się zmieniło dla projektu. Kolejne części rozwijają
skutek, zanim padnie nazwa pliku czy funkcji. Ostatnia część mówi, czego agent
nie sprawdził, więc czytelnik wie, ile wynik jest wart.

## Kontrprzykład

Ten sam wynik podany jako lista plików:

> Zmieniłem `auth/session.py`, `auth/tokens.py` i `api/login.py`.
> Dodałem klasę `TokenChecker` i przeniosłem do niej walidację.
> Usunąłem `check_token()` z `api/login.py`.
> Testy: 42 przechodzą.

Dlaczego jest gorszy: czytelnik nie wie, czy cokolwiek się zepsuło, czy ma coś
zrobić i na ile może zaufać testom. Lista plików opisuje pracę agenta, a nie
skutek dla projektu.
