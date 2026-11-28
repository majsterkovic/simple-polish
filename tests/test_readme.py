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
    "objaśni",
    "czternastu scenariuszach",
]
PREFIX = "tekst, który zostaje:"


def document_items(text: str) -> list[str]:
    """Rodzaje tekstu z kolumny „Kiedy” w wierszu | **Dokument** |."""
    for line in text.splitlines():
        if line.startswith("| **Dokument** |"):
            when_column = line.split("|")[2].strip()
            when_column = when_column.removeprefix(PREFIX).strip()
            return [item.strip() for item in when_column.split(", ") if item.strip()]
    return []


def main() -> int:
    path = ROOT / "README.md"
    if not path.exists():
        print("FAIL: brak README.md")
        return 1
    text = path.read_text(encoding="utf-8")

    errors = [f"brak: {needle}" for needle in NEEDLES if needle not in text]

    skill = document_items((ROOT / "SKILL.md").read_text(encoding="utf-8"))
    if not skill:
        errors.append("SKILL.md: brak wiersza Dokument w tabeli trybów")
    readme = document_items(text)
    errors += [f"README, wiersz Dokument: brak „{item}”"
               for item in skill if item not in readme]

    for error in errors:
        print("FAIL:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
