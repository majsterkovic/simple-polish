"""Regresje z końcowego przeglądu wariantu objaśniania. Jedna funkcja to jedno znalezisko."""
import re
import sys

from rules import ROOT

REF = "references/code-explanation.md"


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


def examples_are_consistent() -> list[str]:
    """Cel i zastrzeżenie wynikają z opisanych etapów, nie z domysłu."""
    errors = []
    model_example = flat(section(read(REF), "## Przykład wzorcowy"))
    for phrase in ("raz na dobę", "pusty wiersz"):
        if phrase in model_example:
            errors.append(f"{REF}: przykład wzorcowy ma „{phrase}”, czego etapy nie pokazują")
    if "codziennie rano" in flat(section(read("references/examples.md"), "## Objaśnienie kodu")):
        errors.append("examples.md: „codziennie rano” nie wynika z przeczytanego skryptu")
    return errors


def each_stage_has_an_output() -> list[str]:
    errors = []
    for name, header in ((REF, "## Przykład wzorcowy"),
                         ("references/examples.md", "## Objaśnienie kodu")):
        for number, stage in enumerate(stages(section(read(name), header)), 1):
            if "Wychodz" not in stage:
                errors.append(f"{name}: etap {number} bez „Wychodzi”")
    return errors


def single_function_without_stage_list() -> list[str]:
    errors = []
    short_explanation = flat(section(read(REF), "## Gdy kodu jest mało"))
    for needle in ("między funkcjami", "jednym zdaniem", "Gdy etapy są co najmniej dwa"):
        if needle not in short_explanation:
            errors.append(f"{REF}, Gdy kodu jest mało: brak „{needle}”")
    if "Jedna funkcja albo jeden krok" not in flat(read("SKILL.md")):
        errors.append("SKILL.md: brak skalowania objaśnienia dla jednej funkcji")
    return errors


def explanation_after_edit() -> list[str]:
    errors = []
    mode_selection = section(read("references/modes.md"), "## Jak wybrać tryb")
    first_question = flat(mode_selection[mode_selection.find("1. "):mode_selection.find("2. ")])
    if "nawet po edycji" not in first_question:
        errors.append("modes.md: pytanie 1 nie wyklucza „jak to działa” po edycji")
    if "przed chwilą zmieniony" not in flat(read("SKILL.md")):
        errors.append("SKILL.md: objaśnienie nie obejmuje kodu przed chwilą zmienionego")
    return errors


def identifiers_for_developers() -> list[str]:
    ref = read(REF)
    errors = []
    if "zobacz Odbiorca" not in flat(section(ref, "## Układ")):
        errors.append(f"{REF}: Układ nie odsyła do części Odbiorca")
    if "używasz ich od początku" not in flat(section(ref, "## Odbiorca")):
        errors.append(f"{REF}: Odbiorca tylko pozwala, zamiast kazać")
    return errors


def hard_rules_in_new_text() -> list[str]:
    errors = []
    ref = flat(read(REF))
    for old in ("piszesz dopiero po przeczytaniu", "a reguły twarde działają tak samo",
                "i nawias by mu przeszkadzał", "pustego pliku, import"):
        if old in ref:
            errors.append(f"{REF}: zostało „{old}”")
    if "obsługi błędu serwera" in flat(read("references/examples.md")):
        errors.append("examples.md: łańcuch „obsługi błędu serwera” w wersji dobrej")
    if "ocena poprawności kodu" in read("docs/superpowers/specs/2026-11-16-simple-polish-design.md"):
        errors.append("spec 16.11: łańcuch „ocena poprawności kodu”")
    return errors


def instruction_precedence_preserves_warnings() -> list[str]:
    boundaries = flat(section(read("SKILL.md"), "## Granice"))
    if "Ostrzeżenie o akcji nieodwracalnej zostaje także wtedy" not in boundaries:
        return ["SKILL.md: pierwszeństwo instrukcji nie chroni ostrzeżeń"]
    return []


CHECKS = [examples_are_consistent, each_stage_has_an_output, single_function_without_stage_list,
          explanation_after_edit, identifiers_for_developers,
          hard_rules_in_new_text, instruction_precedence_preserves_warnings]


def main() -> int:
    errors = [e for check in CHECKS for e in check()]
    for error in errors:
        print("FAIL:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
