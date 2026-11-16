import sys

from rules import ROOT, RULES

CASES = ["konfiguracja", "createUser", "nieodwracaln", "zastrzeżenie", "jedno zdanie"]
SECTIONS = ["## Tryb dokument", "## Tryb odpowiedź", "## Tryb raport",
            "## Czego nie ruszać", "## Tekst już dobry"]


def main() -> int:
    path = ROOT / "references" / "przyklady.md"
    if not path.exists():
        print("FAIL: brak references/przyklady.md")
        return 1
    text = path.read_text(encoding="utf-8")

    errors = [f"brak reguly: {rule}" for rule in RULES if f"## Reguła: `{rule}`" not in text]
    errors += [f"brak przypadku: {case}" for case in CASES if case not in text]
    errors += [f"brak sekcji: {s}" for s in SECTIONS if s not in text]

    for error in errors:
        print("FAIL:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
