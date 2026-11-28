"""Wariant „Objaśnienie kodu”: referencja, odsyłacze i przykład."""
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


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def section(text: str, header: str) -> str:
    match = re.search(rf"^{re.escape(header)}$", text, re.M)
    if not match:
        return ""
    end = text.find("\n## ", match.end())
    return text[match.start():] if end < 0 else text[match.start():end]


def numbered(body: str) -> int:
    return len(re.findall(r"^> \d+\. ", body, re.M))


def main() -> int:
    if not (ROOT / REF).exists():
        print(f"FAIL: brak pliku: {REF}")
        return 1
    ref = read(REF)
    errors = [f"{REF}: brak nagłówka {h}" for h in HEADERS if not section(ref, h)]

    for header, needles in NEEDLES.items():
        body = section(ref, header)
        errors += [f"{REF}, {header}: brak „{n}”" for n in needles if n not in body]

    model_example = section(ref, "## Przykład wzorcowy")
    if numbered(model_example) < 3:
        errors.append(f"{REF}: przykład wzorcowy ma mniej niż trzy etapy")
    if "Co może zaskoczyć:" not in model_example:
        errors.append(f"{REF}: przykład wzorcowy bez „Co może zaskoczyć:”")
    if numbered(section(ref, "## Gdy kodu jest mało")) != 0:
        errors.append(f"{REF}: „Gdy kodu jest mało” ma listę etapów")

    modes = read("references/modes.md")
    for name, text in (("SKILL.md", read("SKILL.md")), ("references/modes.md", modes)):
        if REF not in text:
            errors.append(f"{name}: brak odsyłacza do {REF}")
    if "„jak to działa”" not in modes:
        errors.append("references/modes.md: brak zdania o „jak to działa”")

    example = section(read("references/examples.md"), "## Objaśnienie kodu")
    if not example:
        errors.append("examples.md: brak sekcji ## Objaśnienie kodu")
    else:
        if "Co może zaskoczyć:" not in example:
            errors.append("examples.md: objaśnienie bez „Co może zaskoczyć:”")
        if numbered(example) < 3:
            errors.append("examples.md: objaśnienie ma mniej niż trzy etapy")

    for error in errors:
        print("FAIL:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
