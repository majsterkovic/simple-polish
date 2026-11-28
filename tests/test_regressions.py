"""Regresje z końcowego przeglądu fazy 1. Każda funkcja odpowiada jednemu znalezisku."""
import sys

from rules import ROOT


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def section(text: str, header: str) -> str:
    start = text.find(header)
    if start < 0:
        return ""
    end = text.find("\n## ", start + len(header))
    return text[start:] if end < 0 else text[start:end]


def frontmatter_parses() -> list[str]:
    """W YAML wartość bez cudzysłowu nie może zawierać „: ” — parser uzna to za nowy klucz."""
    text = read("SKILL.md")
    block = text[4:text.find("\n---", 4)]
    errors = []
    for line in block.splitlines():
        key, _, value = line.partition(": ")
        value = value.strip()
        quoted = len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'"
        if not quoted and ": " in value:
            errors.append(f"frontmatter: wartość {key} zawiera „: ” bez cudzysłowu")
    return errors


def report_format_in_skill() -> list[str]:
    report = section(read("SKILL.md"), "## Raport z pracy")
    needles = ["Co się zmieniło:", "Co to znaczy dla projektu:", "Co masz zrobić:",
               "Pewność:", "bez bolda", "nie listę plików", "ani funkcje"]
    return [f"SKILL.md Raport z pracy: brak „{n}”" for n in needles if n not in report]


def mode_order() -> list[str]:
    mode_selection = section(read("references/modes.md"), "## Jak wybrać tryb")
    errors = []
    first = mode_selection.find("1. ")
    if "wykonałem akcje" not in mode_selection[first:mode_selection.find("2. ")]:
        errors.append("modes.md: pierwsze pytanie nie dotyczy wykonanych akcji")
    if "Trzy razy „nie”" in mode_selection or "Trzy razy „nie\"" in mode_selection:
        errors.append("modes.md: zdanie o trzech „nie” przeczy domyślnej Odpowiedzi")
    return errors


def examples_keep_content() -> list[str]:
    text = read("references/examples.md")
    errors = []
    document_section = section(text, "## Tryb dokument")
    if "konfiguracyjn" not in document_section.split("README, po:")[-1].split("Komunikat")[0]:
        errors.append("examples.md: README po zamienia termin „konfiguracyjne”")
    if "2.0" in document_section:
        errors.append("examples.md: README po dopisuje wersję 2.0")
    if ".env" in document_section:
        errors.append("examples.md: komunikat błędu dopisuje plik .env")
    gdpr_example = section(text, "## Czego nie ruszać")
    if gdpr_example.count("z zastrzeżeniem art. 28") < 2 or "innej firmie" in gdpr_example:
        errors.append("examples.md: przykład RODO zmienia treść zastrzeżenia")
    warning_example = section(text, "## Reguła: `ostrzezenie-zawsze`")
    if "Źródło:" not in warning_example:
        errors.append("examples.md: para ostrzezenie-zawsze nie pokazuje źródła z ostrzeżeniem")
    if "przejrzeć" not in section(text, "## Reguła: `jedna-mysl`").split("Dobrze:")[-1]:
        errors.append("examples.md: jedna-mysl gubi treść w wersji Dobrze")
    if "Ustaliliśmy" in section(text, "## Reguła: `bezosobowe`") and "znany z kontekstu" not in section(text, "## Reguła: `bezosobowe`"):
        errors.append("examples.md: bezosobowe wymyśla wykonawcę")
    return errors


def implement_is_distinct_from_deploy() -> list[str]:
    for line in read("references/word-alternatives.md").splitlines():
        if line.startswith("| implementować |"):
            replacement = line.split("|")[2]
            if "wdraża" in replacement:
                return ["word-alternatives.md: implementować → wdrażać myli pisanie kodu z wdrożeniem"]
    return []


def description_has_polish_characters() -> list[str]:
    text = read("SKILL.md")
    block = text[4:text.find("\n---", 4)]
    description = next((line for line in block.splitlines()
                 if line.startswith("description:")), "")
    return [f"SKILL.md opis: brak polskich znaków w „{word}”"
            for word in ("Używaj", "każdym", "błędów", "zrobiłeś")
            if word not in description]


def agent_style_is_consistent() -> list[str]:
    text = section(read("references/agent-style.md"), "## Czego nie pisać")
    errors = []
    if "nigdy" in text:
        errors.append("agent-style.md: „nigdy” przeczy dopuszczalnej liście plików")
    if "To nie jest zakaz" in text:
        errors.append("agent-style.md: „to nie jest zakaz” przeczy zdaniu o „nigdy”")
    return errors


def readme_credits_sources() -> list[str]:
    text = read("README.md")
    errors = []
    if "strict i flavored" not in text:
        errors.append("README.md: brak „strict i flavored” przy danyuchn")
    if "samokontrola" in text:
        errors.append("README.md: „samokontrola” nie występuje w SKILL.md")
    if "zespół Jasnopis" in text:
        errors.append("README.md: zasady 2024 mają więcej autorów niż Jasnopis")
    return errors


def word_alternatives_preserve_meaning() -> list[str]:
    rows = [line for line in read("references/word-alternatives.md").splitlines()
            if line.startswith("| ")]
    errors = []
    for word in ("ten sam", "ważnie", "wziąć udział", "wziąć się za coś"):
        if any(line.startswith(f"| {word} |") for line in rows):
            errors.append(f"word-alternatives.md: „{word}” to nie para zamienna")
    for line in rows:
        if line.startswith("| w zakresie |") and "(usuń)" in line:
            errors.append("word-alternatives.md: „w zakresie” nie zawsze jest puste")
    return errors


CHECKS = [frontmatter_parses, report_format_in_skill, mode_order,
          examples_keep_content, implement_is_distinct_from_deploy,
          description_has_polish_characters, agent_style_is_consistent,
          readme_credits_sources, word_alternatives_preserve_meaning]


def main() -> int:
    errors = [e for check in CHECKS for e in check()]
    for error in errors:
        print("FAIL:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
