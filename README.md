# simple-polish

Skill dla agentów AI, który każe im pisać po polsku prosto i konkretnie.
Jest dla osób, które zlecają pracę agentowi i chcą zrozumieć wynik bez
czytania kodu.

## Instalacja

Przez [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add majsterkovic/simple-polish
```

Ręcznie w Claude Code, dla wszystkich projektów:

```bash
git clone https://github.com/majsterkovic/simple-polish ~/.claude/skills/simple-polish
```

Dla jednego projektu sklonuj repo do `.claude/skills/simple-polish/` w jego
katalogu. Agent potrzebuje tylko `SKILL.md` i katalogu `references/`.

Skill włącza się sam, gdy agent pisze po polsku. Możesz go też przywołać
wprost, na przykład: „opisz mi prostym językiem, co zrobiłeś".

## Trzy tryby

| Tryb | Kiedy | Co rządzi tekstem |
|---|---|---|
| **Dokument** | tekst, który zostaje: README, mail, commit, opis PR, komunikat błędu | standard 2024 i twarde limity |
| **Odpowiedź** | rozmowa: pytanie, wyjaśnienie, dyskusja | odpowiedź w pierwszym zdaniu, proza, terminy wyjaśniane |
| **Raport z pracy** | agent wykonał akcje i zdaje z nich sprawę | skutek, co się zmieniło, co to znaczy, decyzja, pewność |

W razie wątpliwości agent wybiera Odpowiedź. Raport skaluje się do wagi pracy:
drobna zmiana dostaje trzy części, większa pięć.

## Przykład

Raport z pracy po zmianie w kilku plikach:

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

Więcej przykładów: `references/przyklady.md`.

## Czego nie robi

- Nie zmienia treści, tylko formę. Fakty, liczby, nazwy i kod zostają.
- Nie upraszcza zastrzeżeń prawnych ani warunków bezpieczeństwa.
- Nie zamienia niepewności w pewność i nie usuwa zastrzeżeń typu „chyba",
  „prawdopodobnie".
- Nie przepisuje tekstu, który już jest prosty. Mówi to jednym zdaniem.
- Nie dopisuje komentarza o tym, co uprościł. Oddaje sam tekst.
- Nie rusza kodu, komend ani logów. Reguły dotyczą prozy.
- Nie daje certyfikatu zgodności z normą ISO 24495-1. Korzysta z tych samych
  zasad, ale nikt go pod tym kątem nie badał.

## Skąd pochodzą reguły

- [Ustandaryzowane zasady prostego języka (2024)](https://jasnopis.pl),
  opublikowane przez Jasnopis, Fundację Języka Polskiego, Uniwersytet
  Szczeciński, Uniwersytet im. Adama Mickiewicza w Poznaniu i Uniwersytet
  Warszawski. Podstawa trybu Dokument.
- [Standard prostej polszczyzny](https://prostapolszczyzna.uwr.edu.pl/)
  Pracowni Prostej Polszczyzny Uniwersytetu Wrocławskiego (2016).
  Uzupełnienie zasad 2024.
- [prosta-polszczyzna](https://github.com/kashiash/prosta-polszczyzna),
  autor: kashiash (MIT). Źródło par w `references/zamienniki.md` oraz zasad
  BLUF, Top-Down Bridge i Just-in-Time Context w raporcie z pracy.
- [SimpleEnglish](https://github.com/AminBlg/SimpleEnglish), autor: AminBlg
  (MIT). Podział na rejestry, dyscyplina wyjścia, proza bez bolda
  w odpowiedziach.
- [asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill), autor:
  danyuchn (MIT). Rozdzielenie trybu strict i flavored, dwa poziomy reguł,
  twarde i doradcze, oraz zasada „forma, nie treść".

Część „Pewność" w raporcie z pracy jest własna. Żaden z tych projektów nie
każe agentowi mówić, czego nie sprawdził.

## Stan projektu

Gotowa jest faza 1: sam skill, czyli instrukcje i referencje. Agent stosuje
reguły, ale nic ich nie sprawdza automatycznie.

W planach:

- faza 2: linter, który znajduje naruszenia reguł twardych w pliku,
- faza 3: hooki w Claude Code i ewaluacja na dwunastu scenariuszach.

## Testy

```bash
python3 tests/run.py
```

Testy sprawdzają strukturę skilla i pilnują poprawionych wcześniej błędów.
Wymagają tylko Pythona 3, bez dodatkowych bibliotek.

## Licencja

MIT. Zobacz `LICENSE`.
