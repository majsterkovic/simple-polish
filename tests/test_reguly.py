import sys

from rules import ROOT, RULES

HEADERS = [
    "Określ odbiorcę",
    "Układ i kompozycja",
    "Słownictwo",
    "Składnia",
    "Sprawdź tekst",
    "Zdrowy rozsądek",
]


def main() -> int:
    path = ROOT / "references" / "reguly.md"
    if not path.exists():
        print("FAIL: brak references/reguly.md")
        return 1
    text = path.read_text(encoding="utf-8")

    errors = [f"brak: {rule}" for rule in RULES if rule not in text]
    errors += [f"brak: {header}" for header in HEADERS if header not in text]
    for year in ("2024", "2016"):
        if year not in text:
            errors.append(f"brak roku: {year}")

    for error in errors:
        print("FAIL:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
