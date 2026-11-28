"""Regresje z końcowego przeglądu wariantu objaśniania. Jedna funkcja to jedno znalezisko."""
import re
import sys

from rules import ROOT

REF = "references/objasnianie-kodu.md"


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def section(text: str, header: str) -> str:
    match = re.search(rf"^{re.escape(header)}$", text, re.M)
    if not match:
        return ""
    end = text.find("\n## ", match.end())
    return text[match.start():] if end < 0 else text[match.start():end]


def flat(text: str) -> str:
    """Skleja linie, także w cytacie, żeby fraza przełamana w tekście nie uciekła."""
    return re.sub(r"\s*\n>?\s*", " ", text)


def stages(body: str) -> list[str]:
    """Etapy z listy numerowanej w cytacie, każdy z liniami kontynuacji."""
    items, current = [], None
    for line in body.splitlines():
        if re.match(r"^>\s*\d+\. ", line):
            current = [line]
            items.append(current)
        elif current is not None and re.match(r"^>\s{2,}\S", line):
            current.append(line)
        else:
            current = None
    return [" ".join(item) for item in items]


def przyklady_sa_spojne() -> list[str]:
    """Cel i zastrzeżenie wynikają z opisanych etapów, nie z domysłu."""
    errors = []
    wzorzec = flat(section(read(REF), "## Przykład wzorcowy"))
    for phrase in ("raz na dobę", "pusty wiersz"):
        if phrase in wzorzec:
            errors.append(f"{REF}: przykład wzorcowy ma „{phrase}”, czego etapy nie pokazują")
    if "codziennie rano" in flat(section(read("references/przyklady.md"), "## Objaśnienie kodu")):
        errors.append("przyklady.md: „codziennie rano” nie wynika z przeczytanego skryptu")
    return errors


def kazdy_etap_ma_wyjscie() -> list[str]:
    errors = []
    for name, header in ((REF, "## Przykład wzorcowy"),
                         ("references/przyklady.md", "## Objaśnienie kodu")):
        for number, stage in enumerate(stages(section(read(name), header)), 1):
            if "Wychodz" not in stage:
                errors.append(f"{name}: etap {number} bez „Wychodzi”")
    return errors


def jedna_funkcja_bez_listy() -> list[str]:
    errors = []
    malo = flat(section(read(REF), "## Gdy kodu jest mało"))
    for needle in ("między funkcjami", "jednym zdaniem", "Gdy etapy są co najmniej dwa"):
        if needle not in malo:
            errors.append(f"{REF}, Gdy kodu jest mało: brak „{needle}”")
    if "Jedna funkcja albo jeden krok" not in flat(read("SKILL.md")):
        errors.append("SKILL.md: brak skalowania objaśnienia dla jednej funkcji")
    return errors


def jak_to_dziala_po_edycji() -> list[str]:
    errors = []
    wybor = section(read("references/tryby.md"), "## Jak wybrać tryb")
    pierwsze = flat(wybor[wybor.find("1. "):wybor.find("2. ")])
    if "nawet po edycji" not in pierwsze:
        errors.append("tryby.md: pytanie 1 nie wyklucza „jak to działa” po edycji")
    if "przed chwilą zmieniony" not in flat(read("SKILL.md")):
        errors.append("SKILL.md: objaśnienie nie obejmuje kodu przed chwilą zmienionego")
    return errors


def identyfikatory_dla_programisty() -> list[str]:
    ref = read(REF)
    errors = []
    if "zobacz Odbiorca" not in flat(section(ref, "## Układ")):
        errors.append(f"{REF}: Układ nie odsyła do części Odbiorca")
    if "używasz ich od początku" not in flat(section(ref, "## Odbiorca")):
        errors.append(f"{REF}: Odbiorca tylko pozwala, zamiast kazać")
    return errors


def reguly_twarde_w_nowych_tekstach() -> list[str]:
    errors = []
    ref = flat(read(REF))
    for old in ("piszesz dopiero po przeczytaniu", "a reguły twarde działają tak samo",
                "i nawias by mu przeszkadzał", "pustego pliku, import"):
        if old in ref:
            errors.append(f"{REF}: zostało „{old}”")
    if "obsługi błędu serwera" in flat(read("references/przyklady.md")):
        errors.append("przyklady.md: łańcuch „obsługi błędu serwera” w wersji dobrej")
    if "ocena poprawności kodu" in read("docs/superpowers/specs/2026-11-16-simple-polish-design.md"):
        errors.append("spec 16.11: łańcuch „ocena poprawności kodu”")
    return errors


def pierwszenstwo_nie_usuwa_ostrzezen() -> list[str]:
    granice = flat(section(read("SKILL.md"), "## Granice"))
    if "Ostrzeżenie o akcji nieodwracalnej zostaje także wtedy" not in granice:
        return ["SKILL.md: pierwszeństwo instrukcji nie chroni ostrzeżeń"]
    return []


CHECKS = [przyklady_sa_spojne, kazdy_etap_ma_wyjscie, jedna_funkcja_bez_listy,
          jak_to_dziala_po_edycji, identyfikatory_dla_programisty,
          reguly_twarde_w_nowych_tekstach, pierwszenstwo_nie_usuwa_ostrzezen]


def main() -> int:
    errors = [e for check in CHECKS for e in check()]
    for error in errors:
        print("FAIL:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
