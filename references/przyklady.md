# Przykłady

Pary przed i po. Każda reguła twarda ma jedną parę. Potem przykłady trybów
i przypadki, w których skill nie powinien niczego ruszać.

## Reguła: `jedna-mysl`

Źle: Moduł eksportu zapisuje dane do CSV, a także wysyła raport mailem do
administratora, który może go potem przejrzeć.

Dobrze: Moduł eksportu zapisuje dane do CSV. Potem wysyła raport mailem do
administratora.

Dwie czynności w jednym zdaniu każą czytelnikowi trzymać w głowie dwie rzeczy
naraz.

## Reguła: `wyliczenie-lista`

Źle: Skrypt obsługuje pliki CSV, JSON, XML, YAML i Parquet.

Dobrze: Skrypt obsługuje pliki:

- CSV
- JSON
- XML
- YAML
- Parquet

Od czterech elementów lista pionowa czyta się szybciej niż zdanie.

## Reguła: `podwojna-negacja`

Źle: Nie jest wykluczone, że zmiana nie zadziała na starszych wersjach.

Dobrze: Zmiana może nie działać na starszych wersjach.

Każde „nie" czytelnik musi odwrócić w głowie, więc dwa dają podwójną pracę.

## Reguła: `bezosobowe`

Źle: Zostało ustalone, że wdrożenie odbędzie się w piątek. Zaleca się
wcześniejsze sprawdzenie kopii zapasowej.

Dobrze: Ustaliliśmy, że wdrożymy zmianę w piątek. Przed wdrożeniem sprawdź
kopię zapasową.

Forma osobowa mówi, kto działa, a tryb rozkazujący mówi, kto ma działać.

## Reguła: `lancuch-dopelniaczowy`

Źle: Celem jest umożliwienie spłaty raty kredytu klienta.

Dobrze: Chcemy, żeby klient mógł spłacić ratę kredytu.

Po trzecim dopełniaczu czytelnik gubi, który rzeczownik od którego zależy.

## Reguła: `rama-analityczna`

Źle: Zespół dokona oceny wyników i przeprowadzi weryfikację danych.

Dobrze: Zespół oceni wyniki i sprawdzi dane.

Czasownik mówi to samo co rama „dokonać + rzeczownik", tylko krócej.

## Reguła: `warunek-najpierw`

Źle: Uruchom migrację ponownie, jeśli pierwsza próba zakończyła się błędem.

Dobrze: Jeśli pierwsza próba migracji zakończyła się błędem, uruchom ją
ponownie.

Czytelnik, który wykonuje polecenia po kolei, musi znać warunek, zanim zacznie
działać.

## Reguła: `termin-przy-pierwszym-uzyciu`

Źle: Endpoint jest idempotentny, więc możesz go wywołać kilka razy.

Dobrze: Endpoint jest idempotentny: kolejne wywołanie z tymi samymi danymi
niczego nie zmienia. Możesz go więc wywołać kilka razy.

Termin zostaje, bo jest precyzyjny, ale czytelnik dostaje jego znaczenie od
razu.

## Reguła: `fakty-nietkniete`

Źle: Testy prawie wszystkie przechodzą, jest tylko drobny problem
z importem.

Dobrze: 41 z 42 testów przechodzi. Jeden pada z błędem
`ModuleNotFoundError: No module named 'yaml'`.

Uproszczenie nie może zaokrąglić liczby ani przerobić cytowanego błędu.

## Reguła: `ostrzezenie-zawsze`

Źle: Polecenie czyści katalog roboczy.

Dobrze: Polecenie trwale usuwa wszystkie niezapisane pliki z katalogu
roboczego. Nie da się tego cofnąć.

Ostrzeżenie o akcji nieodwracalnej zostaje, nawet gdy tekst robi się przez nie
dłuższy.

## Tryb dokument

README, przed:

> Niniejsze narzędzie umożliwia przeprowadzenie automatycznej konwersji plików
> konfiguracyjnych do nowego formatu, co pozwala na zapewnienie zgodności.

README, po:

> Narzędzie przerabia stare pliki ustawień na nowy format. Dzięki temu działają
> z wersją 2.0.

Komunikat błędu, przed:

> Wystąpił błąd podczas próby nawiązania połączenia z bazą danych.

Komunikat błędu, po:

> Nie udało się połączyć z bazą danych. Sprawdź, czy serwer bazy działa i czy
> adres w pliku `.env` jest poprawny.

Dobry komunikat mówi, co się stało i co czytelnik może zrobić.

## Tryb odpowiedź

Pytanie o architekturę: „Dlaczego cache jest w osobnym serwisie, a nie
w aplikacji?"

> Bo kilka instancji aplikacji musi widzieć te same dane. Gdyby każda miała
> własny cache, użytkownik mógłby dostać różne wyniki zależnie od tego, która
> instancja go obsłuży. Osobny serwis kosztuje jedno połączenie sieciowe więcej,
> ale to kilka milisekund.

Pytanie o bezpieczeństwo: „Czy mogę wrzucić ten token do repozytorium?"

> Nie. Każdy, kto ma dostęp do repozytorium, dostanie wtedy dostęp do konta,
> także po usunięciu tokenu z kolejnych commitów, bo zostaje w historii.
> Trzymaj go w zmiennej środowiskowej albo w menedżerze sekretów.

Odpowiedź zaczyna się od odpowiedzi. Bez „Świetne pytanie" i bez podsumowania
na końcu.

## Tryb raport

Raport pełny, po zmianie w kilku plikach:

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

Raport trzyczęściowy, po drobnej zmianie:

> Changelog ma wpis o nowej nazwie funkcji eksportu. Nic nie musisz robić.
> Sprawdziłem, że stara nazwa nie występuje już w dokumentacji.

## Czego nie ruszać

Termin domenowy, który jest najprostszym słowem. Słowo „konfiguracja" zostaje:

> Zmiana dotyczy tylko konfiguracji serwera.

Nie zamieniaj go na „ustawienia rzeczy, które serwer ma". Rzeczownik
odczasownikowy jest tu terminem, nie nominalizacją do wycięcia.

Identyfikator w zdaniu. Kod zostaje, upraszczasz tylko otoczenie:

> Przed: Funkcja `createUser` dokonuje walidacji danych wejściowych.
>
> Po: Funkcja `createUser` sprawdza dane wejściowe.

Nazwy `createUser` nie tłumaczysz ani nie odmieniasz.

Ostrzeżenie o akcji nieodwracalnej. Przetrwa każde skracanie:

> Przed: Należy mieć na uwadze, iż wykonanie polecenia `DROP TABLE` skutkuje
> nieodwracalną utratą danych zawartych w tabeli.
>
> Po: Polecenie `DROP TABLE` trwale usuwa tabelę razem z danymi. Nie da się
> tego cofnąć.

Forma jest prostsza, ale słowo „nieodwracalnie" w sensie zostaje.

Zastrzeżenie prawne albo warunek bezpieczeństwa. Nie skracasz jego treści:

> Przed: Administrator danych osobowych może przekazać dane podmiotom trzecim
> wyłącznie na podstawie umowy powierzenia, z zastrzeżeniem art. 28 RODO.
>
> Po: Administrator może przekazać dane osobowe innej firmie tylko na podstawie
> umowy powierzenia. Obowiązuje przy tym art. 28 RODO.

Zastrzeżenie i numer artykułu zostają. Upraszczasz tylko składnię.

Pytanie, na które wystarczy jedno zdanie: „Czy testy przechodzą?"

> Tak, wszystkie 42 przechodzą.

Nie dokładasz raportu pięcioczęściowego. Nic się nie zmieniło, więc nie ma
o czym raportować.

## Tekst już dobry

> Kliknij „Eksportuj". Plik CSV pojawi się w folderze Pobrane. Jeśli go nie
> widzisz, odśwież stronę.

Ten tekst spełnia reguły. Nie przepisujesz go. Piszesz jedno zdanie:

> Tekst jest już prosty, nie zmieniam go.
