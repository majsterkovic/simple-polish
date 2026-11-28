# Jak opisywać wykonaną pracę

Raport czyta osoba, która decyduje. Nie czyta kodu. Chce wiedzieć, co zmiana
znaczy dla projektu i co ma zrobić dalej.

Układ i skalowanie raportu opisuje `references/modes.md`. Ten plik mówi, jak
pisać poszczególne części.

## Skutek zamiast listy czynności

Pierwsze zdanie raportu to skutek: co działa inaczej z punktu widzenia
projektu. Czynności agenta mogą pojawić się później, jeśli są potrzebne.

Pliki.

Źle: Zmieniłem `config/loader.py` i `config/defaults.py`.

Dobrze: Aplikacja uruchamia się teraz także wtedy, gdy brakuje pliku
z ustawieniami. Bierze wtedy wartości domyślne.

Funkcje.

Źle: Dodałem funkcję `retry_request()` i wywołuję ją w `fetch_orders()`.

Dobrze: Pobieranie zamówień nie przerywa się już po jednym błędzie sieci.
Próbuje trzy razy, zanim zgłosi problem.

Błąd testu.

Źle: `test_export_csv` pada z `AssertionError: 41 != 42`.

Dobrze: Eksport do CSV gubi ostatni wiersz. Test to wykrył i jeszcze tego nie
naprawiłem.

Nazwa pliku, funkcji albo dokładny komunikat błędu mogą pójść dalej w raporcie,
gdy czytelnik ich potrzebuje. Cytowany błąd zostaje wtedy bez zmian.

## Czego nie pisać

Te elementy opisują pracę agenta, a nie skutek dla projektu:

- ścieżki plików
- numery linii
- nazwy funkcji, klas i zmiennych
- „dodałem", „zmieniłem", „usunąłem" jako początek zdania
- lista commitów

Pierwsze zdanie mówi o skutku, więc te elementy trafiają dopiero do dalszej
części raportu. Pojawiają się tam, gdy czytelnik musi coś z nimi zrobić. Gdy
pyta „które pliki ruszyłeś", odpowiedz listą plików.

## Pewność

Część „Pewność" rozdziela dwie rzeczy.

- **sprawdzone**: to, co agent zobaczył sam. Uruchomiony test, przeczytany
  plik, wykonane polecenie i jego wynik.
- **założone**: cała reszta. To, co powinno działać, ale nikt tego nie
  uruchomił.

Agent nie pisze „działa", jeśli niczego nie uruchomił. Nie zamienia
„powinno" na „jest".

Przykłady zdań:

- Sprawdzone: wszystkie 42 testy przechodzą po zmianie.
- Sprawdzone: aplikacja startuje lokalnie bez pliku z ustawieniami.
- Założone: na serwerze produkcyjnym zachowa się tak samo, ale tam tego nie
  uruchamiałem.
- Założone: inne moduły nie korzystają ze starej funkcji. Szukałem w kodzie,
  ale nie sprawdzałem zewnętrznych skryptów.

## Gdy pracy było mało

Drobna zmiana dostaje trzy części: skutek, decyzja, pewność. Każda może mieć
jedno zdanie.

> Literówka w komunikacie o błędzie logowania jest poprawiona. Nic nie musisz
> robić. Sprawdziłem, że komunikat wyświetla się poprawnie.

> Przycisk „Zapisz" ma teraz ten sam kolor co reszta formularza. Jeśli wolisz
> stary kolor, cofnę zmianę. Oglądałem to tylko w jednej przeglądarce.

> README ma aktualny numer wersji Pythona. Nic nie musisz robić. Nie
> uruchamiałem testów, bo zmiana dotyczy tylko tekstu.

## Gdy coś poszło nie tak

Porażka idzie na początek raportu, prostymi słowami. Bez „drobnych trudności",
„pewnych wyzwań" i „prawie działa". Czytelnik musi wiedzieć, w jakim stanie
jest projekt teraz.

Podaj trzy rzeczy: co nie działa, w jakim stanie zostawiłeś projekt i co
proponujesz.

> Migracja bazy się nie udała i nie zmieniłem żadnych danych.
>
> Co się zmieniło: nic. Skrypt zatrzymał się na pierwszej tabeli, zanim cokolwiek
> zapisał.
>
> Co to znaczy dla projektu: nowa funkcja raportów nie zadziała, dopóki migracja
> nie przejdzie.
>
> Co masz zrobić: zdecyduj, czy mam spróbować jeszcze raz na kopii bazy.
>
> Pewność: sprawdziłem, że tabele mają tę samą liczbę wierszy co przed próbą.
> Nie wiem jeszcze, dlaczego skrypt się zatrzymał.
