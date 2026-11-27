# Przykłady

Pary przed i po. Każda reguła twarda ma jedną parę. Potem przykłady trybów
i przypadki, w których skill nie powinien niczego ruszać.

## Reguła: `jedna-mysl`

Źle: Moduł eksportu zapisuje dane do CSV, a także wysyła raport mailem do
administratora, który może go potem przejrzeć.

Dobrze: Moduł eksportu zapisuje dane do CSV. Potem wysyła raport mailem do
administratora. Administrator może go później przejrzeć.

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

Dobrze: Wdrożenie jest w piątek. Przed wdrożeniem sprawdź kopię zapasową.

Tryb rozkazujący mówi, kto ma działać. Formy „my" używasz tylko wtedy, gdy
wykonawca jest znany z kontekstu. Nie wymyślasz go.

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

Źródło: Polecenie nieodwracalnie usuwa z katalogu roboczego pliki, których
git nie śledzi.

Źle: Polecenie czyści katalog roboczy.

Dobrze: Polecenie usuwa pliki, których git nie śledzi. Nie da się tego cofnąć.

Wersja zła skróciła tekst i zgubiła ostrzeżenie. Ostrzeżenie o akcji
nieodwracalnej zostaje, nawet gdy tekst robi się przez nie dłuższy.

## Tryb dokument

README, przed:

> Niniejsze narzędzie umożliwia przeprowadzenie automatycznej konwersji plików
> konfiguracyjnych do nowego formatu, co pozwala na zapewnienie zgodności.

README, po:

> Narzędzie przerabia stare pliki konfiguracyjne na nowy format. Dzięki temu
> są zgodne z nową wersją.

Komunikat błędu, przed:

> Wystąpił błąd podczas próby nawiązania połączenia z bazą danych.

Komunikat błędu, po:

> Nie udało się połączyć z bazą danych. Sprawdź, czy serwer bazy działa i czy
> adres w ustawieniach połączenia jest poprawny.

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

## Objaśnienie kodu

Pytanie: „Co robi skrypt z przypomnieniami o płatności?”

Przed:

> Skrypt `remind.py` ma funkcję `main()`, która wywołuje `get_overdue()`,
> potem `render()` i `send()`. `get_overdue()` robi zapytanie SQL, `render()`
> używa szablonu Jinja, a `send()` łączy się z SMTP.

Po:

> Ten skrypt wysyła klientom maile z przypomnieniem o zaległej płatności.
>
> 1. Wybór klientów (`get_overdue`). Wchodzi dzisiejsza data. Kod szuka faktur,
>    których termin płatności minął ponad 7 dni temu. Pomija te oznaczone
>    jako przypomniane. Wychodzi lista klientów z kwotami.
> 2. Treść maila (`render`). Wchodzi lista klientów. Kod wstawia imię i kwotę
>    do szablonu. Wychodzą gotowe maile.
> 3. Wysyłka (`send`). Wchodzą gotowe maile. Kod zapisuje oznaczenie faktury
>    jako przypomnianej. Dopiero wtedy łączy się z serwerem pocztowym.
>    Wychodzą oznaczone faktury oraz maile, które udało się wysłać.
>
> Co może zaskoczyć: jeśli skrypt nie połączy się z serwerem pocztowym,
> klient nie dostanie maila. Jeśli oznaczenie zostanie, skrypt pominie tę
> fakturę przy kolejnym uruchomieniu.
>
> Pewność: przeczytałem cały skrypt. Sprawdziłem, kiedy zapisuje oznaczenie
> i jak je sprawdza przy wyborze faktur. Nie sprawdzałem, czy inny skrypt
> usuwa te oznaczenia.

Wersja „po” zaczyna od celu i idzie za danymi. Zastrzeżenie mówi, co stanie się
z klientem, a nie, którego warunku brakuje w kodzie.

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

Blok kodu. Reguły dotyczą prozy, nie kodu:

```python
def load_config(path):
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    return json.loads(Path(path).read_text())
```

Nazwy, składnię i komentarze zostawiasz bez zmian. Upraszczasz tylko zdanie,
które ten kod opisuje.

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
> Po: Administrator danych osobowych może przekazać dane podmiotom trzecim
> tylko na podstawie umowy powierzenia, z zastrzeżeniem art. 28 RODO.

Zastrzeżenie, termin „podmioty trzecie" i numer artykułu zostają. Upraszczasz tylko
składnię: „wyłącznie" zamienia się na „tylko", nic więcej.

Pytanie, na które wystarczy jedno zdanie: „Czy testy przechodzą?"

> Tak, wszystkie 42 przechodzą.

Nie dokładasz raportu pięcioczęściowego. Nic się nie zmieniło, więc nie ma
o czym raportować.

## Tekst już dobry

> Kliknij „Eksportuj". Plik CSV pojawi się w folderze Pobrane. Jeśli go nie
> widzisz, odśwież stronę.

Ten tekst spełnia reguły. Nie przepisujesz go. Piszesz jedno zdanie:

> Tekst jest już prosty, nie zmieniam go.
