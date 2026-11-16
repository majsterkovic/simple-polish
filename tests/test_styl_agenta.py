import sys

from rules import ROOT

NEEDLES = [
    "Co się zmieniło",
    "Co to znaczy dla projektu",
    "Co masz zrobić",
    "Pewność",
    "skutek",
    "sprawdzone",
    "założone",
]


def main() -> int:
    path = ROOT / "references" / "styl-agenta.md"
    if not path.exists():
        print("FAIL: brak references/styl-agenta.md")
        return 1
    text = path.read_text(encoding="utf-8")

    errors = [f"brak: {needle}" for needle in NEEDLES if needle not in text]
    if text.count("Źle:") < 3:
        errors.append(f"mniej niz 3 pary: {text.count('Źle:')}")
    if text.count("Dobrze:") < 3:
        errors.append(f"mniej niz 3 pary: {text.count('Dobrze:')}")

    for error in errors:
        print("FAIL:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
