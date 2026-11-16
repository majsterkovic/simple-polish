# Simple Polish, faza 1: prompt — plan implementacji

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dostarczyć działający skill `simple-polish`: `SKILL.md`, pięć plików referencyjnych, README i test strukturalny, bez lintera.

**Architecture:** Skill jest plikiem promptu plus referencjami ładowanymi na żądanie. `SKILL.md` trzyma trzy tryby pracy i dziesięć reguł twardych, bo to musi być w kontekście zawsze. Reszta leży w `references/` i model sięga po nią wtedy, gdy potrzebuje szczegółów. Testy są skryptami w czystym Pythonie, bez pytest, bo cały projekt ma nie mieć zależności.

**Tech Stack:** Markdown, Python 3.12+ (tylko biblioteka standardowa), git.

**Spec:** `docs/superpowers/specs/2026-11-16-simple-polish-design.md`

## Global Constraints

- Język projektu: polski. Nazwy plików i identyfikatorów reguł: ASCII, bez polskich znaków.
- Reguły są sygnałami i progami, nie zakazami. Każdy limit ma kierunek i tolerancję.
- Skill zmienia formę, nie treść. Fakty, liczby, nazwy, kod i cytowane błędy zostają nietknięte.
- Zero zależności runtime. Testy to skrypty `python tests/<plik>.py`, kod wyjścia różny od zera przy błędzie.
- `SKILL.md` ma najwyżej 150 linii. Szczegóły idą do `references/`.
- Identyfikatory reguł twardych, kanoniczne: `jedna-mysl`, `wyliczenie-lista`, `podwojna-negacja`, `bezosobowe`, `lancuch-dopelniaczowy`, `rama-analityczna`, `warunek-najpierw`, `termin-przy-pierwszym-uzyciu`, `fakty-nietkniete`, `ostrzezenie-zawsze`.
- Licencja MIT. Autorstwo cudzych reguł podane w README.

## Review Focus

Pięć przypadków, które najłatwiej zepsuć w prompcie. Każdy dostaje przykład
w `references/przyklady.md` i asercję w teście z Zadania 6.

1. Termin fachowy, który jest zarazem najprostszym słowem (*konfiguracja*,
   *wymaganie*, *jakość*). Skill nie może go tępić.
2. Proza przemieszana z blokami kodu i identyfikatorami w rodzaju
   `createUser`. Kod zostaje, tłumaczone jest tylko otoczenie.
3. Akcja nieodwracalna. Ostrzeżenie musi przetrwać upraszczanie.
4. Zastrzeżenie prawne albo warunek bezpieczeństwa. Nie wolno go skrócić.
5. Pytanie, na które należy odpowiedzieć jednym zdaniem. Raport
   pięcioczęściowy byłby tu nadużyciem.

---

### Task 1: Repozytorium i `SKILL.md`

**Files:**
- Create: `SKILL.md`
- Create: `.gitignore`
- Create: `LICENSE`
- Create: `tests/rules.py`
- Create: `tests/test_skill_md.py`
- Create: `tests/run.py`

**Interfaces:**
- Produces: dziesięć identyfikatorów reguł z sekcji Global Constraints, używanych przez Zadania 3, 6 i 8.

- [ ] **Step 1: Zainicjuj repozytorium**

```bash
cd /home/mariusz/Desktop/simple-polish
git init
```

- [ ] **Step 2: Napisz `.gitignore`**

Zawartość: `SimpleEnglish/`, `asd-ste100-skill/`, `prosta-polszczyzna/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`.

- [ ] **Step 3: Napisz `LICENSE`**

Standardowy tekst MIT, rok 2026, dzierżawca: Mariusz.

- [ ] **Step 4: Napisz `tests/rules.py` i test `tests/test_skill_md.py`**

`tests/rules.py`:

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES = [
    "jedna-mysl", "wyliczenie-lista", "podwojna-negacja", "bezosobowe",
    "lancuch-dopelniaczowy", "rama-analityczna", "warunek-najpierw",
    "termin-przy-pierwszym-uzyciu", "fakty-nietkniete", "ostrzezenie-zawsze",
]
```

`tests/test_skill_md.py`:

```python
import re
import sys

from rules import ROOT, RULES


def main() -> int:
    path = ROOT / "SKILL.md"
    if not path.exists():
        print("FAIL: brak SKILL.md")
        return 1
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors = []

    if len(lines) > 150:
        errors.append(f"SKILL.md ma {len(lines)} linii, limit to 150")
    if not text.startswith("---\n"):
        errors.append("SKILL.md nie zaczyna sie od frontmattera")
    if not re.search(r"^name:\s*simple-polish\s*$", text, re.M):
        errors.append("frontmatter bez name: simple-polish")
    if not re.search(r"^description:\s*\S", text, re.M):
        errors.append("frontmatter bez description")

    for mode in ("Dokument", "Odpowiedź", "Raport z pracy"):
        if mode not in text:
            errors.append(f"brak trybu: {mode}")
    for rule in RULES:
        if rule not in text:
            errors.append(f"brak reguly: {rule}")
    for line in lines:
        if len(line) > 200:
            errors.append(f"linia dluzej niz 200 znakow: {line[:40]}")

    for error in errors:
        print("FAIL:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Napisz `tests/run.py`**

Skrypt przechodzi po `tests/test_*.py`, ładuje każdy przez `importlib.util.spec_from_file_location` i woła `main()`. Zwraca 1, jeśli którykolwiek zwrócił różne od zera.

- [ ] **Step 6: Uruchom test, sprawdź że pada**

Run: `python tests/run.py`
Expected: `FAIL: brak SKILL.md`, kod wyjścia 1.

- [ ] **Step 7: Napisz `SKILL.md`**

Frontmatter:

```yaml
---
name: simple-polish
description: Pisze po polsku prosto i konkretnie. Uzywaj przy kazdym tekscie po polsku: dokumentacji, mailach, commitach, komunikatach bledow, a przede wszystkim gdy opisujesz wykonana prace. Triggery: prosty jezyk, jasnopis, nie rozumiem, opisz mi to, co zrobiles.
---
```

Kolejność sekcji, dokładnie sześć:

1. `## Trzy tryby` — tabela z sekcji 5 specu, plus trzy reguły trzymające całość Dosłownie z sekcji 5, punkty 1–3.
2. `## Raport z pracy` — układ `skutek → co się zmieniło → co to znaczy dla projektu → decyzja → pewność`, zdanie o skalowaniu, zdanie o rozdzielaniu sprawdzonego od założonego.
3. `## Reguły twarde` — tabela z sekcji 7 specu, kolumny `ID | Reguła | Przykład`, w całości.
4. `## Progi, nie zakazy` — lista z sekcji 8 specu, w całości.
5. `## Reguły doradcze` — lista z sekcji 9 specu, w całości.
6. `## Granice` — lista z sekcji 10 specu, plus wskaźniki, kiedy czytać który plik z `references/`.

Każda reguła twarda to jedno zdanie. Żadna nie dostaje słowa „zawsze", „nigdy" ani „bezwzględnie" poza `ostrzezenie-zawsze` i `fakty-nietkniete`.

- [ ] **Step 8: Uruchom test, sprawdź że przechodzi**

Run: `python tests/run.py`
Expected: brak linii `FAIL`, kod wyjścia 0.

- [ ] **Step 9: Commit**

```bash
git add .gitignore LICENSE SKILL.md tests/
git commit -m "feat: rdzen skilla simple-polish z trzema trybami"
```

---

### Task 2: `references/tryby.md`

**Files:**
- Create: `references/tryby.md`
- Create: `tests/test_tryby.py`

**Interfaces:**
- Consumes: nazwy trybów z `SKILL.md`.
- Produces: etykiety pięciu części raportu, powtarzane w Zadanich 5 i 6: `Co się zmieniło`, `Co to znaczy dla projektu`, `Co masz zrobić`, `Pewność`.

- [ ] **Step 1: Napisz test `tests/test_tryby.py`**

Sprawdza, że `references/tryby.md` istnieje i zawiera: `Dokument`, `Odpowiedź`, `Raport z pracy`, `W razie wątpliwości`, `Co się zmieniło`, `Co to znaczy dla projektu`, `Co masz zrobić`, `Pewność`, `nie zmienia faktów`.

- [ ] **Step 2: Uruchom test, sprawdź że pada**

Run: `python tests/run.py`
Expected: `FAIL: brak references/tryby.md`.

- [ ] **Step 3: Napisz `references/tryby.md`**

Zawartość, w tej kolejności:

1. Sposób wyboru trybu w trzech krokach: czy tekst zostaje na stałe, czy to rozmowa, czy właśnie wykonałem akcje.
2. Tabela trybów z sekcji 5 specu.
3. Trzy reguły trzymające całość, rozwinięte po akapicie każda.
4. Skalowanie raportu: tabela `Waga pracy | Części`.
5. Pełny przykład wzorcowy z sekcji 6 specu, przepisany dosłownie.
6. Kontrprzykład: ten sam wynik podany jako lista plików, z jednym zdaniem komentarza, dlaczego jest gorszy.

- [ ] **Step 4: Uruchom test, sprawdź że przechodzi**

Run: `python tests/run.py`
Expected: kod wyjścia 0.

- [ ] **Step 5: Commit**

```bash
git add references/tryby.md tests/test_tryby.py
git commit -m "docs: referencja trybow pracy"
```

---

### Task 3: `references/reguly.md`

**Files:**
- Create: `references/reguly.md`
- Create: `tests/test_reguly.py`

**Interfaces:**
- Consumes: dziesięć identyfikatorów reguł z Zadania 1.

- [ ] **Step 1: Napisz test `tests/test_reguly.py`**

Sprawdza obecność wszystkich dziesięciu identyfikatorów, ciągów `2024` i `2016`, oraz sześciu nagłówków standardu 2024: `Określ odbiorcę`, `Układ i kompozycja`, `Słownictwo`, `Składnia`, `Sprawdź tekst`, `Zdrowy rozsądek`.

- [ ] **Step 2: Uruchom test, sprawdź że pada**

Run: `python tests/run.py`
Expected: `FAIL: brak references/reguly.md`.

- [ ] **Step 3: Napisz `references/reguly.md`**

Struktura: dwie części.

Część `## Zasady 2024` — sześć podsekcji, po jednej na zasadę, każda z numerem i pełną treścią z sekcji „Ustandaryzowane zasady 2024" w `docs/superpowers/specs/2026-11-16-simple-polish-design.md`. Przy każdej podsekcji dopisz, która reguła twarda z `SKILL.md` ją egzekwuje.

Część `## Zasady 2016` — trzydzieści punktów numerowanych 1–30, przepisanych z sekcji „Standard PPP UWr 2016" specu, w formie jednego zdania na punkt.

Na końcu `## Kiedy reguły się gryzą` — trzy akapity: długość kontra precyzja, prostota kontra zastrzeżenie prawne, bezosobowość kontra odpowiedzialność.

- [ ] **Step 4: Uruchom test, sprawdź że przechodzi**

Run: `python tests/run.py`
Expected: kod wyjścia 0.

- [ ] **Step 5: Commit**

```bash
git add references/reguly.md tests/test_reguly.py
git commit -m "docs: reguly 2024 i 2016 pogrupowane wedlug zadania"
```

---

### Task 4: `references/zamienniki.md`

**Files:**
- Create: `references/zamienniki.md`
- Create: `tests/test_zamienniki.py`

- [ ] **Step 1: Napisz test `tests/test_zamienniki.py`**

Trzy asercje:

```python
rows = [l for l in text.splitlines() if l.startswith("|")][2:]  # bez naglowka i separatora
sources = [r.split("|")[1].strip().lower() for r in rows]
assert len(rows) >= 60
assert len(sources) == len(set(sources)), "duplikaty w kolumnie zrodlowej"
assert text.count("\n## ") >= 10
```

- [ ] **Step 2: Uruchom test, sprawdź że pada**

Run: `python tests/run.py`
Expected: `FAIL: brak references/zamienniki.md`.

- [ ] **Step 3: Napisz `references/zamienniki.md`**

Dziesięć sekcji `## `: modne wyrazy, kancelaryzmy, archaizmy, konstrukcje analityczne, pleonazmy, kalki z angielskiego, formy bezosobowe, puste formuły, rusycyzmy, terminy IT po polsku.

Tabela w każdej sekcji: `| Zamiast | Napisz | Dlaczego |`. Minimum sześć wierszy na sekcję, razem co najmniej 60.

Źródła do wykorzystania: `prosta-polszczyzna/references/slownik-substytucji.md` (po odsianiu duplikatów), sekcja „Słownictwo" specu, zasada 27 standardu 2016.

Wiersze muszą być parami, nie pojedynczymi słowami: `dokonać analizy` → `przeanalizować`, nie `analiza` → `?`. Wyjątki domenowe nie wchodzą do tabeli.

- [ ] **Step 4: Uruchom test, sprawdź że przechodzi**

Run: `python tests/run.py`
Expected: kod wyjścia 0.

- [ ] **Step 5: Commit**

```bash
git add references/zamienniki.md tests/test_zamienniki.py
git commit -m "docs: tabela zamiennikow bez duplikatow"
```

---

### Task 5: `references/styl-agenta.md`

**Files:**
- Create: `references/styl-agenta.md`
- Create: `tests/test_styl_agenta.py`

**Interfaces:**
- Consumes: etykiety raportu z Zadania 2.

- [ ] **Step 1: Napisz test `tests/test_styl_agenta.py`**

Sprawdza obecność pięciu etykiet, słów `sprawdzone` i `założone`, oraz co najmniej trzech wystąpień `Źle:` i trzech `Dobrze:`.

- [ ] **Step 2: Uruchom test, sprawdź że pada**

Run: `python tests/run.py`
Expected: `FAIL: brak references/styl-agenta.md`.

- [ ] **Step 3: Napisz `references/styl-agenta.md`**

Części:

1. Zdanie o odbiorcy: osoba decydująca, nie czyta kodu, chce wiedzieć co to znaczy i co dalej.
2. Trzy pary `Źle:` / `Dobrze:` dla części „skutek" — jedna o plikach, jedna o funkcjach, jedna o błędzie testu.
3. Sekcja `## Czego nie pisać`: ścieżki, numery linii, nazwy funkcji, „dodałem", „zmieniłem", lista commitów.
4. Sekcja `## Pewność`: rozdzielenie `sprawdzone` (uruchomiony test, przeczytany plik, wykonane polecenie) od `założone`, z czterema przykładami zdań.
5. Sekcja `## Gdy pracy było mało`: trzy przykłady raportu trzyczęściowego.
6. Sekcja `## Gdy coś poszło nie tak`: jak podać porażkę bez eufemizmów, jeden przykład.

- [ ] **Step 4: Uruchom test, sprawdź że przechodzi**

Run: `python tests/run.py`
Expected: kod wyjścia 0.

- [ ] **Step 5: Commit**

```bash
git add references/styl-agenta.md tests/test_styl_agenta.py
git commit -m "docs: jak opisywac wykonana prace"
```

---

### Task 6: `references/przyklady.md`

**Files:**
- Create: `references/przyklady.md`
- Create: `tests/test_przyklady.py`

**Interfaces:**
- Consumes: identyfikatory reguł z Zadania 1, etykiety z Zadania 2.

- [ ] **Step 1: Napisz test `tests/test_przyklady.py`**

Dwie asercje:

```python
from rules import RULES

for rule in RULES:
    assert rule in text, rule
for case in ["konfiguracja", "createUser", "nieodwracaln", "zastrzeżenie",
             "jedno zdanie"]:
    assert case in text, case
```

- [ ] **Step 2: Uruchom test, sprawdź że pada**

Run: `python tests/run.py`
Expected: `FAIL: brak references/przyklady.md`.

- [ ] **Step 3: Napisz `references/przyklady.md`**

Struktura: sześć sekcji.

1. `## Reguła: <id>` — dziesięć podsekcji, po jednej na regułę twardą. Każda: `Źle:` i `Dobrze:`, jedno zdanie wyjaśnienia.
2. `## Tryb dokument` — README, komunikat błędu.
3. `## Tryb odpowiedź` — pytanie o architekturę, pytanie o bezpieczeństwo.
4. `## Tryb raport` — raport pełny i raport trzyczęściowy.
5. `## Czego nie ruszać` — pięć przypadków z sekcji Review Focus: termin domenowy `konfiguracja`, identyfikator `createUser` w zdaniu, ostrzeżenie o `nieodwracaln` akcji, `zastrzeżenie` prawne, pytanie wymagające odpowiedzi w `jedno zdanie`.
6. `## Tekst już dobry` — przykład tekstu, którego nie wolno przepisywać, i zdanie, które model ma wtedy napisać.

- [ ] **Step 4: Uruchom test, sprawdź że przechodzi**

Run: `python tests/run.py`
Expected: kod wyjścia 0.

- [ ] **Step 5: Commit**

```bash
git add references/przyklady.md tests/test_przyklady.py
git commit -m "docs: przyklady before/after dla trzech trybow"
```

---

### Task 7: `README.md`

**Files:**
- Create: `README.md`
- Create: `tests/test_readme.py`

- [ ] **Step 1: Napisz test `tests/test_readme.py`**

Sprawdza obecność: `npx skills add`, `Dokument`, `Odpowiedź`, `Raport z pracy`, frazy `Czego nie robi`, oraz nazw `kashiash`, `AminBlg`, `danyuchn`, `Jasnopis`.

- [ ] **Step 2: Uruchom test, sprawdź że pada**

Run: `python tests/run.py`
Expected: `FAIL: brak README.md`.

- [ ] **Step 3: Napisz `README.md`**

Sekcje, w tej kolejności:

1. Jedno zdanie, co to robi, i jedno zdanie, dla kogo.
2. `## Instalacja` — `npx skills add <repo> --skill simple-polish` oraz instalacja jako skill projektu.
3. `## Trzy tryby` — tabela, trzy wiersze.
4. `## Przyklad` — przykład wzorcowy raportu ze specu.
5. `## Czego nie robi` — pięć punktów z sekcji „Granice" specu, plus brak certyfikacji ISO.
6. `## Skad pochodza reguly` — źródła i autorzy: kashiash, AminBlg, danyuchn, Jasnopis, standard PPP UWr, Ustandaryzowane zasady 2024.
7. `## Testy` — `python tests/run.py`.
8. `## Licencja` — MIT.

- [ ] **Step 4: Uruchom test, sprawdź że przechodzi**

Run: `python tests/run.py`
Expected: kod wyjścia 0.

- [ ] **Step 5: Commit**

```bash
git add README.md tests/test_readme.py
git commit -m "docs: README z instalacja, ograniczeniami i zrodlami"
```

---

### Task 8: Spójność i wydanie fazy 1

**Files:**
- Create: `tests/test_consistency.py`
- Modify: `.gitignore` (dopisz `docs/superpowers/plans/` tylko jeśli użytkownik o to poprosi — domyślnie nie)

**Interfaces:**
- Consumes: wszystkie wcześniejsze zadania.

- [ ] **Step 1: Napisz test `tests/test_consistency.py`**

Importuje `RULES` z `tests/rules.py`. Pierwsza asercja: każdy identyfikator z listy występuje w `SKILL.md`, w `references/reguly.md` i w `references/przyklady.md`. Druga asercja: `name:` we frontmatterze pasuje do `^[a-z0-9-]{1,64}$`, a `description:` ma najwyżej 1024 znaki.

- [ ] **Step 2: Uruchom test**

Run: `python tests/run.py`
Expected: kod wyjścia 0. Jeśli nie, brakujący identyfikator wskazuje plik do poprawy.

- [ ] **Step 3: Sprawdź, że skill jest kompletny bez lintera**

Run: `python tests/run.py && ls references/`
Expected: kod 0 i pięć plików: `przyklady.md`, `reguly.md`, `styl-agenta.md`, `tryby.md`, `zamienniki.md`.

- [ ] **Step 4: Sprawdź ręcznie jeden przypadek**

Wklej do sesji Claude Code z zainstalowanym skillem polecenie „zmieniłem nazwę funkcji w trzech plikach, zaktualizuj changelog" i sprawdź, czy odpowiedź ma części: skutek, co się zmieniło, co to znaczy, decyzja, pewność. Zapisz wynik w opisie commita, jeśli jest niezgodny.

- [ ] **Step 5: Commit**

```bash
git add tests/test_consistency.py
git commit -m "test: spojnosc identyfikatorow regul i frontmattera"
```

---

## Po fazie 1

Faza 2 (linter) i faza 3 (ewaluacja, hooki, pakowanie) dostają osobne plany po
weryfikacji fazy 1. Ten plan nie tworzy `scripts/lint.py` ani `evals/` i nie
zawiera zależności, których one wymagają.
