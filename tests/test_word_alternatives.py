import sys

from rules import ROOT


def table_rows(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells[0] == "Zamiast":
            continue
        if set(cells[0]) <= {"-", ":"}:
            continue
        rows.append(cells)
    return rows


def main() -> int:
    path = ROOT / "references" / "word-alternatives.md"
    if not path.exists():
        print("FAIL: brak references/word-alternatives.md")
        return 1
    text = path.read_text(encoding="utf-8")

    rows = table_rows(text)
    errors = []
    if len(rows) < 60:
        errors.append(f"tylko {len(rows)} wierszy, minimum to 60")

    sources = [row[0].lower() for row in rows]
    duplicates = sorted({src for src in sources if sources.count(src) > 1})
    for duplicate in duplicates:
        errors.append(f"duplikat w kolumnie zrodlowej: {duplicate}")

    sections = text.count("\n## ")
    if sections < 10:
        errors.append(f"tylko {sections} sekcji, minimum to 10")

    for error in errors:
        print("FAIL:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
