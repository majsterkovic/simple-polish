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

Etapy mają kolejność, więc lista wygrywa tu z prozą. Pozostałe części piszesz
prozą, z etykietą i dwukropkiem, bez bolda.

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

Jedna funkcja albo jeden krok dostaje dwa, trzy zdania prozy: cel i pewność.
Jeśli coś w niej może zaskoczyć, dopisujesz to jednym zdaniem. Gdy etapy są co
najmniej dwa, piszesz listę.

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
> 3. Zapis (`save_orders`). Wchodzą poprawne zamówienia. Kod zapisuje je
>    w bazie po jednym. Wychodzi wpis w logu z liczbą zapisanych zamówień.
>
> Co może zaskoczyć: zapis idzie po jednym zamówieniu, bez transakcji. Jeśli
> baza odrzuci jedno zamówienie, wcześniejsze zostają w bazie, a reszta
> przepada. Kod nie zgłasza przy tym błędu.
>
> Pewność: przeczytałem wszystkie trzy etapy. Widzę obsługę ujemnej kwoty. Nie
> widzę, co kod robi, gdy baza odrzuci zapis, a przeszedłem całą ścieżkę od
> wczytania do zapisu. Nie sprawdzałem, jak często baza odrzuca zamówienia.

## Kontrprzykład

To samo objaśnienie ułożone według plików:

> W `import/reader.py` jest funkcja `read_orders()`, która używa
> `csv.DictReader`. W `import/validate.py` jest `validate()` z kilkoma
> warunkami. `import/db.py` zawiera `save_orders()`, która wywołuje
> `session.add()` w pętli. Uwaga: `save_orders()` nie używa transakcji.

Dlaczego jest gorszy: czytelnik nie wie, po co ten kod istnieje ani w jakiej
kolejności płyną dane. Zastrzeżenie opisuje warunek w kodzie, a nie to, co
stanie się z zamówieniami. Nie wiadomo też, co autor przeczytał, a co zgadł.
