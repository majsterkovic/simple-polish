import sys

from rules import ROOT, RULES

CASES = {
    "## Czego nie ruszać": ["konfiguracja", "createUser", "nieodwracaln",
                            "zastrzeżenie"],
    "## Tekst już dobry": ["jedno zdanie"],
}
SECTIONS = ["## Tryb dokument", "## Tryb odpowiedź", "## Tryb raport",
            "## Czego nie ruszać", "## Tekst już dobry"]


def section(text: str, header: str) -> str:
    start = text.find(header)
    if start < 0:
        return ""
    end = text.find("\n## ", start + len(header))
    return text[start:] if end < 0 else text[start:end]


def main() -> int:
    path = ROOT / "references" / "examples.md"
    if not path.exists():
        print("FAIL: brak references/examples.md")
        return 1
    text = path.read_text(encoding="utf-8")
    errors = []

    for rule in RULES:
        if not section(text, f"## Reguła: `{rule}`").strip():
            errors.append(f"brak reguly: {rule}")

    for header in SECTIONS:
        body = section(text, header)
        if not body:
            errors.append(f"brak sekcji: {header}")
            continue
        for case in CASES.get(header, []):
            if case not in body:
                errors.append(f"brak przypadku: {case} w sekcji {header}")

    for error in errors:
        print("FAIL:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
