import importlib.util
import sys
from pathlib import Path

TESTS = Path(__file__).resolve().parent


def main() -> int:
    failed = []
    for path in sorted(TESTS.glob("test_*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        code = module.main()
        print(f"{path.name}: {'OK' if code == 0 else 'FAIL'}")
        if code != 0:
            failed.append(path.name)

    if failed:
        print("FAIL:", ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
