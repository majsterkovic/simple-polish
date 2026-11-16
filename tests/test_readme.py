import sys

from rules import ROOT

NEEDLES = [
    "npx skills add",
    "Dokument",
    "Odpowiedź",
    "Raport z pracy",
    "Czego nie robi",
    "kashiash",
    "AminBlg",
    "danyuchn",
    "Jasnopis",
]


def main() -> int:
    path = ROOT / "README.md"
    if not path.exists():
        print("FAIL: brak README.md")
        return 1
    text = path.read_text(encoding="utf-8")

    errors = [f"brak: {needle}" for needle in NEEDLES if needle not in text]
    for error in errors:
        print("FAIL:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
