import sys

from rules import ROOT

NEEDLES = [
    "Dokument",
    "Odpowiedź",
    "Raport z pracy",
    "W razie wątpliwości",
    "Co się zmieniło",
    "Co to znaczy dla projektu",
    "Co masz zrobić",
    "Pewność",
    "nie zmienia faktów",
]


def main() -> int:
    path = ROOT / "references" / "tryby.md"
    if not path.exists():
        print("FAIL: brak references/tryby.md")
        return 1
    text = path.read_text(encoding="utf-8")

    errors = [f"brak: {needle}" for needle in NEEDLES if needle not in text]

    for error in errors:
        print("FAIL:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
