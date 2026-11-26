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
    raport = section(read("SKILL.md"), "## Raport z pracy")
    needles = ["Co się zmieniło:", "Co to znaczy dla projektu:", "Co masz zrobić:",
               "Pewność:", "bez bolda", "nie listę plików", "ani funkcje"]
    return [f"SKILL.md Raport z pracy: brak „{n}”" for n in needles if n not in raport]


def mode_order() -> list[str]:
    wybor = section(read("references/tryby.md"), "## Jak wybrać tryb")
    errors = []
    first = wybor.find("1. ")
    if "wykonałem akcje" not in wybor[first:wybor.find("2. ")]:
        errors.append("tryby.md: pierwsze pytanie nie dotyczy wykonanych akcji")
    if "Trzy razy „nie”" in wybor or "Trzy razy „nie\"" in wybor:
        errors.append("tryby.md: zdanie o trzech „nie” przeczy domyślnej Odpowiedzi")
    return errors


def examples_keep_content() -> list[str]:
    text = read("references/przyklady.md")
    errors = []
    dokument = section(text, "## Tryb dokument")
    if "konfiguracyjn" not in dokument.split("README, po:")[-1].split("Komunikat")[0]:
        errors.append("przyklady.md: README po zamienia termin „konfiguracyjne”")
    if "2.0" in dokument:
        errors.append("przyklady.md: README po dopisuje wersję 2.0")
    if ".env" in dokument:
        errors.append("przyklady.md: komunikat błędu dopisuje plik .env")
    rodo = section(text, "## Czego nie ruszać")
    if rodo.count("z zastrzeżeniem art. 28") < 2 or "innej firmie" in rodo:
        errors.append("przyklady.md: przykład RODO zmienia treść zastrzeżenia")
    ostrz = section(text, "## Reguła: `ostrzezenie-zawsze`")
    if "Źródło:" not in ostrz:
        errors.append("przyklady.md: para ostrzezenie-zawsze nie pokazuje źródła z ostrzeżeniem")
    if "przejrzeć" not in section(text, "## Reguła: `jedna-mysl`").split("Dobrze:")[-1]:
        errors.append("przyklady.md: jedna-mysl gubi treść w wersji Dobrze")
    if "Ustaliliśmy" in section(text, "## Reguła: `bezosobowe`") and "znany z kontekstu" not in section(text, "## Reguła: `bezosobowe`"):
        errors.append("przyklady.md: bezosobowe wymyśla wykonawcę")
    return errors


def implementowac_not_deploy() -> list[str]:
    for line in read("references/zamienniki.md").splitlines():
        if line.startswith("| implementować |"):
            replacement = line.split("|")[2]
            if "wdraża" in replacement:
                return ["zamienniki.md: implementować → wdrażać myli pisanie kodu z wdrożeniem"]
    return []


def opis_z_polskimi_znakami() -> list[str]:
    text = read("SKILL.md")
    block = text[4:text.find("\n---", 4)]
    opis = next((line for line in block.splitlines()
                 if line.startswith("description:")), "")
    return [f"SKILL.md opis: brak polskich znaków w „{word}”"
            for word in ("Używaj", "każdym", "błędów", "zrobiłeś")
            if word not in opis]


def styl_agenta_bez_sprzecznosci() -> list[str]:
    text = section(read("references/styl-agenta.md"), "## Czego nie pisać")
    errors = []
    if "nigdy" in text:
        errors.append("styl-agenta.md: „nigdy” przeczy dopuszczalnej liście plików")
    if "To nie jest zakaz" in text:
        errors.append("styl-agenta.md: „to nie jest zakaz” przeczy zdaniu o „nigdy”")
    return errors


def zrodla_w_readme() -> list[str]:
    text = read("README.md")
    errors = []
    if "strict i flavored" not in text:
        errors.append("README.md: brak „strict i flavored” przy danyuchn")
    if "samokontrola" in text:
        errors.append("README.md: „samokontrola” nie występuje w SKILL.md")
    if "zespół Jasnopis" in text:
        errors.append("README.md: zasady 2024 mają więcej autorów niż Jasnopis")
    return errors


def zamienniki_nie_za_ostre() -> list[str]:
    rows = [line for line in read("references/zamienniki.md").splitlines()
            if line.startswith("| ")]
    errors = []
    for word in ("ten sam", "ważnie", "wziąć udział", "wziąć się za coś"):
        if any(line.startswith(f"| {word} |") for line in rows):
            errors.append(f"zamienniki.md: „{word}” to nie para zamienna")
    for line in rows:
        if line.startswith("| w zakresie |") and "(usuń)" in line:
            errors.append("zamienniki.md: „w zakresie” nie zawsze jest puste")
    return errors


CHECKS = [frontmatter_parses, report_format_in_skill, mode_order,
          examples_keep_content, implementowac_not_deploy,
          opis_z_polskimi_znakami, styl_agenta_bez_sprzecznosci,
          zrodla_w_readme, zamienniki_nie_za_ostre]


def main() -> int:
    errors = [e for check in CHECKS for e in check()]
    for error in errors:
        print("FAIL:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
