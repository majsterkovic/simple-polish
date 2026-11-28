# Jak objaśniać istniejący kod

Objaśnienie czyta osoba, która chce zrozumieć, jak działa kod, którego nie
pisała. Chce wiedzieć, po co ten kod istnieje, co robi po kolei i gdzie może ją
zaskoczyć.

## Kiedy

Gdy użytkownik pyta, jak działa istniejący kod. Na przykład: „jak to działa”,
„objaśnij mi ten moduł”, „przeprowadź mnie przez pipeline”, „co robi ten etap”.

Objaśnienie to wariant trybu Odpowiedź. Pierwsze zdanie odpowiada na pytanie.
Reguły twarde działają tak samo jak w całym skillu. Objaśnieniem jest też
pytanie o kod, który przed chwilą zmieniłeś. Pytanie „co zrobiłeś” to raport
z pracy.

## Układ

1. Cel. Pierwsze zdanie, bez etykiety: co ten kod robi dla projektu.
2. Etapy. Lista numerowana w kolejności, w jakiej płyną dane. Przy każdym
   etapie piszesz, co wchodzi, co się dzieje i co wychodzi. Jeśli użytkownik
   sam używa nazw z kodu, zaczynasz od identyfikatora (zobacz Odbiorca).
   W innym razie najpierw podajesz ludzką nazwę etapu, a identyfikator
   w nawiasie.
3. `Co może zaskoczyć:` rzeczy, których czytelnik się nie spodziewa.
4. `Pewność:` co przeczytałeś, a co wnioskujesz z nazw.

Części `Co może zaskoczyć:` i `Pewność:` piszesz prozą. Ich etykiety
zapisujesz zwykłym tekstem.

## Co może zaskoczyć

Podajesz najwyżej trzy rzeczy, od tej o największym skutku. Szukasz ich w
czterech miejscach:

- ciche błędy: wyjątek złapany i pominięty, wartość domyślna podstawiona bez
  ostrzeżenia
- skutki uboczne: zapis na dysk, wywołanie sieci, zmiana wspólnego stanu
- założenia o kolejności: etap działa tylko wtedy, gdy wcześniejszy coś
  przygotował
- przypadki brzegowe z realnym skutkiem: utrata danych, złe liczby, akcja
  nieodwracalna

Każda rzecz wynika z kodu, który przeczytałeś. Opisujesz zachowanie, nie
warunek w kodzie.

Źle: brak obsługi `None` w `parse_row`.

Dobrze: jeśli w pliku jest pusty wiersz, import zatrzyma się w połowie i nie
powie dlaczego.

Jeśli nic nie znalazłeś, piszesz jedno zdanie:
„Nie znalazłem nic nietypowego”. Nie dopisujesz zastrzeżeń, żeby wypełnić tę
część.

## Pewność

Ta część mówi, ile objaśnienie jest warte. Rozdzielasz to, co przeczytałeś,
od tego, co wnioskujesz z nazw plików i funkcji.

O każdym zachowaniu piszesz jednym z trzech rodzajów zdań:

- „widzę obsługę”: przeczytałeś miejsce, w którym kod to obsługuje. Na
  przykład: widzę obsługę pustego pliku. Import wtedy nic nie robi.
- „nie widzę obsługi”: szukałeś i nie znalazłeś. Na przykład: nie widzę
  obsługi zerwanego połączenia z bazą.
- „nie sprawdzałem”: nie wiesz. Na przykład: nie sprawdzałem, jak kod działa
  przy pliku większym niż pamięć.

Bez przeczytania całej ścieżki, od wejścia do wyjścia, nie piszesz „nie widzę
obsługi”. Brak obsługi w jednej funkcji nie znaczy, że nie ma jej wyżej.

## Gdy kodu jest mało

Etap to krok przepływu danych między funkcjami albo modułami. Linia w środku
funkcji nie jest etapem.

Jedną funkcję albo jeden krok objaśniasz w dwóch lub trzech zdaniach prozy.
Podajesz cel i mówisz, co sprawdziłeś. Jeśli coś może zaskoczyć, opisujesz to
jednym zdaniem w ramach tego limitu. Gdy etapy są co najmniej dwa, piszesz
listę.

> Ta funkcja zamienia kwotę w groszach na tekst do faktury, na przykład 12345
> na „123,45 zł”. Przeczytałem ją całą. Nie sprawdzałem, czy ktoś wywołuje ją
> z kwotą ujemną.

## Odbiorca

Domyślnie piszesz dla osoby, która nie czyta kodu. Identyfikatory trafiają
wtedy do nawiasów albo dalej w tekście.

Jeśli użytkownik sam używa nazw z kodu, używasz ich od początku. Taki
czytelnik szuka w kodzie tego, o czym mówisz. Nawias by mu przeszkadzał.

## Przykład wzorcowy

Pytanie: „Jak działa import zamówień?”

> Ten kod przenosi zamówienia z pliku CSV od dostawcy do naszej bazy.
>
> 1. Wczytanie pliku (`read_orders`). Wchodzi plik CSV z serwera dostawcy.
>    Kod czyta go wiersz po wierszu. Wychodzi lista zamówień.
> 2. Sprawdzenie (`validate`). Wchodzi lista zamówień. Kod odrzuca zamówienia
>    bez numeru klienta i z ujemną kwotą. Wychodzą dwie listy: poprawne
>    i odrzucone.
> 3. Zapis (`save_orders`). Wchodzą poprawne zamówienia. Kod zatwierdza każdy
>    zapis osobno. Jeśli zapis się nie uda, kod zapisuje błąd w logu i kończy
>    import. Wychodzą zapisane zamówienia oraz wpis w logu, jeśli wystąpił błąd.
>
> Co może zaskoczyć: jeśli baza odrzuci jedno zamówienie, wcześniejsze
> zostają w bazie. Import kończy się przed zapisem pozostałych zamówień.
>
> Pewność: przeczytałem wszystkie trzy etapy. Sprawdziłem, że kod zatwierdza
> każdy zapis osobno i kończy import po błędzie. Nie sprawdzałem, czy osobne
> zadanie ponawia import.

## Kontrprzykład

To samo objaśnienie ułożone według plików:

> W `import/reader.py` jest funkcja `read_orders()`, która używa
> `csv.DictReader`. W `import/validate.py` jest `validate()` z kilkoma
> warunkami. `import/db.py` zawiera `save_orders()`, która wywołuje
> `session.add()` w pętli. Uwaga: kod wywołuje `session.commit()` po każdym
> zamówieniu.

Dlaczego jest gorszy: czytelnik nie wie, po co ten kod istnieje ani w jakiej
kolejności płyną dane. Zastrzeżenie opisuje warunek w kodzie, a nie to, co
stanie się z zamówieniami. Nie wiadomo też, co autor przeczytał, a co zgadł.
