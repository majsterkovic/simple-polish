# Simple Polish — objaśnianie kodu i poprawki z przeglądu

Data: 2026-11-28. Zmiana mała, krótki projekt. Rozszerza
`2026-11-16-simple-polish-design.md`.

## Po co

Użytkownik często pyta agenta, jak działa istniejący kod: pipeline, etapy,
moduł. Dziś takie pytanie trafia do trybu Odpowiedź. Ten tryb nie mówi, jak
przeprowadzić czytelnika przez system krok po kroku. Nie każe też oddzielić
tego, co agent przeczytał, od tego, co zgaduje z nazw.

Przy okazji przegląd skilla znalazł cztery drobne braki. Poprawiamy je w tej
samej zmianie, bo każdy to jedno zdanie albo jedna poprawka.

## Cele

1. Wariant „Objaśnienie kodu” w trybie Odpowiedź.
2. Reguła, kiedy lista wygrywa z prozą.
3. Zdanie o pierwszeństwie instrukcji użytkownika i harnessu.
4. Zgodna tabela trybów w README i SKILL.md.
5. Pliki `smoke2.*` poza repozytorium.

## Poza zakresem

- linter, hooki i ewaluacja z fazy 2 i 3
- zmiana wyzwalaczy w `description`
- przepisywanie testów opartych na szukaniu słów
- ocena, czy objaśniany kod jest poprawny

## Czego nie chcemy

- Wymyślonych zastrzeżeń. Sekcja „Co może zaskoczyć” nie może zmuszać modelu
  do wypełnienia jej czymkolwiek.
- Czwartego trybu. Każdy tryb utrudnia wybór.
- SKILL.md powyżej 150 linii. Dziś ma 126.

## Ograniczenia

- Testy używają tylko biblioteki standardowej Pythona i działają przez
  `python3 tests/run.py`.
- Linie poza tabelami w SKILL.md mają najwyżej 200 znaków.
- Nowe teksty piszemy według reguł samego skilla, w trybie Dokument.
- Zainstalowany skill to dowiązanie do tego repozytorium. Zmiana działa
  od razu po zapisie.

## Podejścia

| Podejście | Zysk | Koszt | Decyzja |
|---|---|---|---|
| Wariant Odpowiedzi z plikiem `references/objasnianie-kodu.md` | pierwsze zdanie działa jak w Odpowiedzi, SKILL.md rośnie o kilka linii | wariant łatwo przeoczyć | wybrane |
| Czwarty tryb „Objaśnienie” | widoczny w tabeli trybów | trudniejszy wybór trybu, przebudowa `tryby.md` | odrzucone |
| Rozszerzenie `styl-agenta.md` | brak nowego pliku | ten plik dotyczy wykonanej pracy, a objaśnienie nie jest pracą | odrzucone |

Wybór podjął agent, a użytkownik zatwierdził zakres w rozmowie.

## Projekt

### Wariant „Objaśnienie kodu”

Kiedy: użytkownik pyta, jak działa istniejący kod. Na przykład: „jak to
działa”, „objaśnij”, „przeprowadź mnie przez”, „co robi ten etap”.

Układ:

1. Cel. Pierwsze zdanie, bez etykiety: co ten kod robi dla projektu.
2. Etapy. Lista numerowana w kolejności przepływu danych. Przy każdym etapie:
   co wchodzi, co się dzieje, co wychodzi. Najpierw ludzka nazwa, identyfikator
   z kodu w nawiasie.
3. `Co może zaskoczyć:` najwyżej trzy rzeczy, od największego skutku.
   Kategorie:
   - ciche błędy
   - skutki uboczne
   - założenia o kolejności
   - przypadki brzegowe z realnym skutkiem
   Każda rzecz wynika z przeczytanego kodu. Opis mówi o zachowaniu, nie
   o warunku w kodzie. Jeśli nic nie ma, wystarczy jedno zdanie: „Nie
   znalazłem nic nietypowego”.
4. `Pewność:` które części agent przeczytał, a które wnioskuje z nazw. Trzy
   rodzaje zdań: „widzę obsługę”, „nie widzę obsługi”, „nie sprawdzałem”.
   Zdanie „nie widzę obsługi” wymaga przeczytania całej ścieżki.

Skalowanie: jedna funkcja albo jeden krok dostaje cel i pewność w dwóch,
trzech zdaniach prozy. Lista etapów pojawia się od dwóch etapów wzwyż.

Odbiorca (decyzja agenta): domyślnie osoba, która nie czyta kodu. Jeśli
użytkownik sam używa nazw z kodu, identyfikatory mogą pojawić się od początku.

Pliki:

- `references/objasnianie-kodu.md`: zasady, przykład wzorcowy, kontrprzykład
  opisujący strukturę plików zamiast przepływu danych.
- `SKILL.md`: jedna linia w tabeli „Kiedy sięgnąć po referencję” i jedno
  zdanie w opisie trybu Odpowiedź.
- `references/tryby.md`: jedno zdanie przy trybie Odpowiedź z odsyłaczem.
- `references/przyklady.md`: sekcja `## Objaśnienie kodu`, para przed i po.

### Lista a proza

W trybie Odpowiedź lista wygrywa z prozą, gdy kolejność ma znaczenie albo gdy
elementów jest co najmniej cztery (`wyliczenie-lista`). Zdanie trafia do
SKILL.md i do `tryby.md`.

### Pierwszeństwo instrukcji

Nowy punkt w sekcji „Granice” w SKILL.md: instrukcje użytkownika i harnessu,
na przykład narzucony format odpowiedzi, mają pierwszeństwo przed skillem.

### README

Wiersz „Dokument” w tabeli trybów dostaje brakujące „release notes” i „UI”.
README wspomina wariant objaśniania jednym zdaniem pod tabelą. Liczba
scenariuszy w „Stan projektu” zmienia się z dwunastu na czternaście.

### Spec z 16 listopada

- Sekcja 4: pozycję „wyjaśnianie kodu” zastępuje „ocena poprawności kodu”.
  Skill zmienia formę objaśnienia, nie jego treść.
- Sekcja 13: dwa nowe scenariusze, objaśnienie pipeline'u i objaśnienie
  jednej funkcji. Razem czternaście.
- Sekcja 17: „Dwanaście scenariuszy” zmienia się na „Czternaście scenariuszy”.

### Pliki `smoke2.*`

Dopisujemy `smoke*.err` i `smoke*.json` do `.gitignore`. Plików nie usuwamy,
bo to wynik uruchomienia użytkownika.

### Testy

- `tests/test_objasnianie.py`: plik istnieje, ma etykiety `Co może zaskoczyć:`
  i `Pewność:`, trzy rodzaje zdań o pewności i wyjście „nic nietypowego”.
  SKILL.md i `tryby.md` odsyłają do pliku. `przyklady.md` ma sekcję
  `## Objaśnienie kodu`.
- `tests/test_readme.py`: każdy rodzaj tekstu z wiersza „Dokument” w SKILL.md
  występuje w wierszu „Dokument” w README.
- `tests/test_skill_md.py`: SKILL.md ma zdanie o pierwszeństwie instrukcji
  i regułę o liście.

Testy sprawdzają etykiety i odsyłacze, nie dokładne brzmienie prozy.

## Do decyzji wykonawcy

- Dokładne brzmienie zdań i przykładów, zgodne z regułami skilla.
- Temat przykładu wzorcowego. Musi mieć co najmniej trzy etapy i jedną rzecz
  w „Co może zaskoczyć”.
- Miejsce zdania o liście w SKILL.md: sekcja „Progi” albo opis trybu.
