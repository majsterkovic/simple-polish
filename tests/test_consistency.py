import re
import sys

from rules import ROOT, RULES

FILES = ["SKILL.md", "references/rules.md", "references/examples.md"]


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    block = text[4:text.find("\n---", 4)]
    fields = {}
    for line in block.splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return fields


def main() -> int:
    errors = []
    for name in FILES:
        path = ROOT / name
        if not path.exists():
            errors.append(f"brak pliku: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        errors += [f"{name}: brak reguly {rule}" for rule in RULES if rule not in text]

    meta = frontmatter((ROOT / "SKILL.md").read_text(encoding="utf-8"))
    if not re.fullmatch(r"[a-z0-9-]{1,64}", meta.get("name", "")):
        errors.append(f"zla nazwa we frontmatterze: {meta.get('name')!r}")
    description = meta.get("description", "")
    if not description or len(description) > 1024:
        errors.append(f"description ma {len(description)} znakow (1-1024)")

    for error in errors:
        print("FAIL:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
