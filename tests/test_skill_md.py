import re
import sys

from rules import ROOT, RULES


def body_lines(text: str) -> list[str]:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                return lines[index + 1:]
    return lines


def main() -> int:
    path = ROOT / "SKILL.md"
    if not path.exists():
        print("FAIL: brak SKILL.md")
        return 1
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors = []

    if len(lines) > 150:
        errors.append(f"SKILL.md ma {len(lines)} linii, limit to 150")
    if not text.startswith("---\n"):
        errors.append("SKILL.md nie zaczyna sie od frontmattera")
    if not re.search(r"^name:\s*simple-polish\s*$", text, re.M):
        errors.append("frontmatter bez name: simple-polish")
    if not re.search(r"^description:\s*\S", text, re.M):
        errors.append("frontmatter bez description")

    for mode in ("Dokument", "Odpowiedź", "Raport z pracy"):
        if mode not in text:
            errors.append(f"brak trybu: {mode}")
    for rule in RULES:
        if rule not in text:
            errors.append(f"brak reguly: {rule}")
    for line in body_lines(text):
        if line.startswith("|"):
            continue
        if len(line) > 200:
            errors.append(f"linia dluzej niz 200 znakow: {line[:40]}")

    for error in errors:
        print("FAIL:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
