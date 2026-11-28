# Simple Polish: objaśnianie kodu i poprawki z przeglądu — plan implementacji

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dodać do trybu Odpowiedź wariant „Objaśnienie kodu” i zamknąć cztery drobne braki z przeglądu.

**Architecture:** Wariant żyje w nowym pliku `references/code-explanation.md`. SKILL.md i `modes.md` dostają tylko krótkie odsyłacze, żeby SKILL.md został mały. Poprawki z przeglądu to pojedyncze zdania w SKILL.md, `modes.md`, README i specu. Każdą zmianę pilnuje test w stylu istniejących: skrypt z `main() -> int`, który szuka etykiet i odsyłaczy.

**Tech Stack:** Markdown, Python 3 (tylko biblioteka standardowa), git.

**Spec:** `docs/superpowers/specs/2026-11-28-code-explanation-design.md`

## Global Constraints

- Nowe teksty piszesz według reguł samego skilla, w trybie Dokument: jedno zdanie to jedna myśl, bez `-no/-to`, bez „zaleca się”, warunek przed poleceniem.
- Cudzysłowy polskie: „…”. Etykiety części piszesz zwykłym tekstem z dwukropkiem, bez bolda.
- SKILL.md ma najwyżej 150 linii. Linie poza tabelami mają najwyżej 200 znaków. Zawijaj prozę około 80 znaków, jak reszta plików.
- Testy: tylko biblioteka standardowa, skrypt `tests/test_*.py` z funkcją `main() -> int`, `from rules import ROOT`. Uruchamia je `python3 tests/run.py`.
- Testy sprawdzają etykiety, nagłówki i odsyłacze. Nie sprawdzają brzmienia prozy.
- Komunikaty commitów jak w historii: `feat:`, `fix:`, `docs:`, bez polskich znaków, z linią `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Poza zakresem: linter, hooki, ewaluacja, zmiana `description`, przepisywanie istniejących testów.

## Review Focus

1. Pytanie o jedną funkcję. Model nie powinien dawać listy etapów, tylko dwa, trzy zdania prozy. Pilnuje tego sekcja „Gdy kodu jest mało” w zadaniu 1.
2. Użytkownik sam używa nazw z kodu. Model nie powinien chować identyfikatorów w nawiasach. Pilnuje tego sekcja „Odbiorca” w zadaniu 1.
3. Pytanie „jak to działa” zaraz po edycji tego kodu. To objaśnienie, nie raport z pracy. Pilnuje tego zdanie w `modes.md` w zadaniu 1.
4. Kod bez niczego nietypowego. Model pisze jedno zdanie zamiast wymyślać zastrzeżenia. Pilnuje tego needle „nic nietypowego” w zadaniu 1.
5. Twierdzenie „nie widzę obsługi” bez przeczytania całej ścieżki. Pilnuje tego needle „całej ścieżki” w zadaniu 1.

---

### Task 1: Wariant „Objaśnienie kodu”

**Files:**
- Create: `references/code-explanation.md`
- Create: `tests/test_code_explanation.py`
- Modify: `SKILL.md:27` (po trzeciej regule) i `SKILL.md:126` (lista „Kiedy sięgnąć po referencję”)
- Modify: `references/modes.md:15` (po akapicie o trybie Odpowiedź)
- Modify: `references/examples.md:169` (nowa sekcja przed `## Czego nie ruszać`)

**Interfaces:**
- Produces: nagłówki w `references/code-explanation.md`, w tej kolejności: `## Kiedy`, `## Układ`, `## Co może zaskoczyć`, `## Pewność`, `## Gdy kodu jest mało`, `## Odbiorca`, `## Przykład wzorcowy`, `## Kontrprzykład`. Sekcja `## Objaśnienie kodu` w `references/examples.md`.

- [ ] **Step 1: Write the failing test `tests/test_code_explanation.py`**

```python
import re
import sys

from rules import ROOT

REF = "references/code-explanation.md"
HEADERS = ["## Kiedy", "## Układ", "## Co może zaskoczyć", "## Pewność",
           "## Gdy kodu jest mało", "## Odbiorca", "## Przykład wzorcowy",
           "## Kontrprzykład"]
NEEDLES = {
    "## Układ": ["Co może zaskoczyć:", "Pewność:"],
    "## Co może zaskoczyć": ["najwyżej trzy", "nic nietypowego"],
    "## Pewność": ["widzę obsługę", "nie widzę obsługi", "nie sprawdzałem",
                   "całej ścieżki"],
    "## Odbiorca": ["nazw z kodu"],
}

def section(text: str, header: str) -> str: ...   # jak w test_examples.py

def numbered(body: str) -> int:
    return len(re.findall(r"^> \d+\. ", body, re.M))
```

Asercje w `main()`, każda jako osobny komunikat `FAIL:`:
- `REF` istnieje i ma każdy nagłówek z `HEADERS`.
- Każdy needle z `NEEDLES` występuje w swojej sekcji.
- `numbered(section(ref, "## Przykład wzorcowy")) >= 3`.
- `numbered(section(ref, "## Gdy kodu jest mało")) == 0`.
- `"Co może zaskoczyć:"` występuje w `section(ref, "## Przykład wzorcowy")`.
- `REF` występuje w `SKILL.md` i w `references/modes.md`.
- `references/modes.md` zawiera `„jak to działa”`.
- `section(przyklady, "## Objaśnienie kodu")` nie jest pusta, ma `"Co może zaskoczyć:"` i `numbered(...) >= 3`.

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tests/test_code_explanation.py`
Expected: `FAIL: brak pliku: references/code-explanation.md`, kod wyjścia 1.

- [ ] **Step 3: Write `references/code-explanation.md`**

Treść każdej sekcji bierzesz z części „Wariant »Objaśnienie kodu«” w specu:
- `## Kiedy`: przykłady pytań ze specu. Wariant należy do trybu Odpowiedź.
- `## Układ`: cztery części. Cel to pierwsze zdanie bez etykiety. Etapy to lista numerowana według przepływu danych: co wchodzi, co się dzieje, co wychodzi. Ludzka nazwa idzie przed identyfikatorem w nawiasie. Dalej etykiety `Co może zaskoczyć:` i `Pewność:`. Lista wygrywa tu z prozą, bo kolejność ma znaczenie.
- `## Co może zaskoczyć`: najwyżej trzy rzeczy od największego skutku i cztery kategorie ze specu jako lista. Każda rzecz wynika z przeczytanego kodu i opisuje zachowanie. Dosłowne wyjście: „Nie znalazłem nic nietypowego.”
- `## Pewność`: przeczytane czy wnioskowane z nazw. Trzy rodzaje zdań, każde z jednym przykładem. „Nie widzę obsługi” wymaga przeczytania całej ścieżki.
- `## Gdy kodu jest mało`: jedna funkcja albo jeden krok dostaje dwa, trzy zdania prozy: cel i pewność. Lista etapów pojawia się od dwóch etapów wzwyż. Jeden przykład w cytacie, bez listy numerowanej.
- `## Odbiorca`: domyślnie osoba, która nie czyta kodu. Jeśli użytkownik sam używa nazw z kodu, identyfikatory mogą pojawić się od początku.
- `## Przykład wzorcowy`: cytat `>` z celem, co najmniej trzema etapami zapisanymi jako `> 1. `, jedną rzeczą w `Co może zaskoczyć:` i częścią `Pewność:`. Proponowany temat: import zamówień z CSV, czyli wczytanie, sprawdzenie i zapis. Zaskoczenie: pusty wiersz zatrzymuje import w połowie bez komunikatu.
- `## Kontrprzykład`: to samo objaśnienie ułożone według plików i funkcji. Pod spodem jedno, dwa zdania, dlaczego jest gorszy.

- [ ] **Step 4: Add pointers in `SKILL.md` and `references/modes.md`**

`SKILL.md`, akapit po trzeciej regule (linia 27), dosłownie:

```markdown
Pytanie o to, jak działa istniejący kod, to wariant Odpowiedzi: objaśnienie
kodu. Układ: cel, etapy, co może zaskoczyć, pewność.
```

`SKILL.md`, nowa pozycja na liście referencji po `opisujesz wykonaną pracę`, dosłownie:

```markdown
- objaśniasz istniejący kod — `references/code-explanation.md`
```

`references/modes.md`, nowy akapit po linii 15, dosłownie:

```markdown
Pytanie o to, jak działa istniejący kod, to wariant Odpowiedzi: objaśnienie
kodu. Pytanie „jak to działa” zostaje objaśnieniem także wtedy, gdy przed
chwilą edytowałeś ten kod. Raportem jest pytanie o to, co zrobiłeś. Układ
i zasady: `references/code-explanation.md`.
```

- [ ] **Step 5: Add `## Objaśnienie kodu` to `references/examples.md`**

Umieść sekcję przed `## Czego nie ruszać`. Daj jedno pytanie użytkownika, wersję „Przed” opisującą pliki i funkcje oraz wersję „Po” w układzie z kroku 3. Temat ma być inny niż w przykładzie wzorcowym, żeby model nie uczył się jednego tekstu.

- [ ] **Step 6: Run tests to verify they pass**

Run: `python3 tests/run.py`
Expected: wszystkie pliki `OK`, w tym `test_code_explanation.py: OK` i `test_skill_md.py: OK`. `wc -l SKILL.md` pokazuje najwyżej 150.

- [ ] **Step 7: Commit**

```bash
git add references/code-explanation.md references/modes.md references/examples.md SKILL.md tests/test_code_explanation.py docs/superpowers/specs/2026-11-28-code-explanation-design.md docs/superpowers/plans/2026-11-28-code-explanation.md
git commit -m "feat: wariant objasniania kodu w trybie odpowiedz"
```

### Task 2: Lista a proza i pierwszeństwo instrukcji

**Files:**
- Modify: `SKILL.md:84-85` (sekcja „Progi, nie zakazy”) i `SKILL.md:110-119` (sekcja „Granice”)
- Modify: `references/modes.md` (po akapicie dodanym w zadaniu 1)
- Test: `tests/test_skill_md.py`, `tests/test_modes.py`

**Interfaces:**
- Consumes: akapit o objaśnieniu w `references/modes.md` z zadania 1.

- [ ] **Step 1: Write the failing tests**

W `tests/test_skill_md.py`, w `main()`, przed pętlą wypisującą błędy:

```python
for needle in ("kolejność ma znaczenie", "mają pierwszeństwo przed skillem"):
    if needle not in text:
        errors.append(f"brak zdania: {needle}")
```

W `tests/test_modes.py` dopisz `"kolejność ma znaczenie"` do `NEEDLES`.

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 tests/test_skill_md.py; python3 tests/test_modes.py`
Expected: `FAIL: brak zdania: kolejność ma znaczenie`, `FAIL: brak zdania: mają pierwszeństwo przed skillem`, `FAIL: brak: kolejność ma znaczenie`.

- [ ] **Step 3: Add the sentences**

`SKILL.md`, nowa pozycja w „Progi, nie zakazy” zaraz po pozycji o limicie 30 słów:

```markdown
- W trybie odpowiedzi lista wygrywa z prozą, gdy kolejność ma znaczenie albo
  gdy elementów jest co najmniej cztery (`wyliczenie-lista`).
```

`SKILL.md`, nowa pozycja na końcu listy w „Granice”:

```markdown
- Instrukcje użytkownika i harnessu mają pierwszeństwo przed skillem, na
  przykład narzucony format odpowiedzi.
```

`references/modes.md`, nowy akapit po akapicie z zadania 1, z tym samym zdaniem o liście co w SKILL.md.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 tests/run.py`
Expected: wszystkie `OK`. `wc -l SKILL.md` pokazuje najwyżej 150.

- [ ] **Step 5: Commit**

```bash
git add SKILL.md references/modes.md tests/test_skill_md.py tests/test_modes.py
git commit -m "fix: lista a proza i pierwszenstwo instrukcji harnessu"
```

### Task 3: README, spec z 16 listopada i `.gitignore`

**Files:**
- Modify: `README.md:31` (wiersz Dokument), `README.md:35` (zdanie pod tabelą), `README.md:98` (liczba scenariuszy)
- Modify: `docs/superpowers/specs/2026-11-16-simple-polish-design.md:55`, `:300-303`, `:363`
- Modify: `.gitignore`
- Test: `tests/test_readme.py`

**Interfaces:**
- Produces: `document_items(text: str) -> list[str]` w `tests/test_readme.py`.

- [ ] **Step 1: Write the failing test**

W `tests/test_readme.py` dodaj:

```python
def document_items(text: str) -> list[str]:
    """Rodzaje tekstu z kolumny „Kiedy” w wierszu | **Dokument** |."""
```

Funkcja bierze pierwszą linię zaczynającą się od `| **Dokument** |`, drugą kolumnę tabeli, ucina prefiks `tekst, który zostaje:` i dzieli resztę po `, `. Brak wiersza daje pustą listę.

Asercje w `main()`:
- `document_items(skill)` nie jest pusta.
- Każdy element `document_items(skill)` występuje w `document_items(readme)`. Komunikat: `FAIL: README, wiersz Dokument: brak „{item}”`.
- Dopisz do `NEEDLES`: `"objaśni"` i `"czternastu scenariuszach"`.

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tests/test_readme.py`
Expected: `FAIL: README, wiersz Dokument: brak „release notes”`, to samo dla `UI`, `FAIL: brak: objaśni`, `FAIL: brak: czternastu scenariuszach`.

- [ ] **Step 3: Update `README.md`**

- Wiersz Dokument, kolumna „Kiedy”: `tekst, który zostaje: README, mail, release notes, UI, commit, opis PR, komunikat błędu`.
- Po zdaniu „W razie wątpliwości agent wybiera Odpowiedź…” nowe zdanie: `Pytanie o to, jak działa istniejący kod, dostaje objaśnienie: cel, etapy, co może zaskoczyć i pewność.`
- Linia 98: `dwunastu scenariuszach` → `czternastu scenariuszach`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tests/test_readme.py`
Expected: kod wyjścia 0, bez linii `FAIL`.

- [ ] **Step 5: Update the 16 November spec**

- Sekcja 4, lista „Poza zakresem”: `- wyjaśnianie kodu` → `- ocena poprawności kodu`.
- Sekcja 13: `dwanaście, po dwa na tryb:` → `czternaście:`. Na końcu wyliczenia, po `odpowiedź na pytanie „czy to bezpieczne”`, dopisz `, objaśnienie pipeline'u, objaśnienie jednej funkcji`.
- Sekcja 17, faza 3: `Dwanaście scenariuszy` → `Czternaście scenariuszy`.

Run: `grep -n -i "dwanaś\|wyjaśnianie kodu" docs/superpowers/specs/2026-11-16-simple-polish-design.md`
Expected: brak wyników.

- [ ] **Step 6: Update `.gitignore`**

Dopisz dwie linie: `smoke*.err` i `smoke*.json`. Plików `smoke2.*` nie usuwasz.

Run: `git status --short`
Expected: brak `smoke2.err` i `smoke2.json` na liście.

- [ ] **Step 7: Run all tests**

Run: `python3 tests/run.py`
Expected: wszystkie `OK`.

- [ ] **Step 8: Commit**

```bash
git add README.md tests/test_readme.py docs/superpowers/specs/2026-11-16-simple-polish-design.md .gitignore
git commit -m "docs: README i spec zgodne z wariantem objasniania"
```
