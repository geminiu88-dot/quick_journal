"""Run every test: python tests/run.py   (or one file: python tests/run.py test_todo)

--preview tests the pages in preview/ (before a preview goes live) instead of the main ones.

Each test_*.py file holds functions named test_...; each one is run and
reported as ok or FAIL. Exit code 0 = everything passed. Run this before
every release to live (README, "Tests").
"""
import importlib
import sys
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import browser  # noqa: E402


def main():
    args = sys.argv[1:]
    if "--preview" in args:
        args.remove("--preview")
        browser.PAGES = browser.ROOT / "preview"
        print("testing preview/")
    names = args or sorted(p.stem for p in HERE.glob("test_*.py"))
    passed, failed, start = 0, [], time.time()
    for name in names:
        mod = importlib.import_module(name)
        for fname in [f for f in dir(mod) if f.startswith("test_")]:
            try:
                getattr(mod, fname)()
                passed += 1
                print(f"ok    {name}.{fname}")
            except Exception as e:
                failed.append(f"{name}.{fname}")
                print(f"FAIL  {name}.{fname}: {e}")
                if not isinstance(e, AssertionError):
                    traceback.print_exc()
    browser.close()
    print(f"\n{passed} passed, {len(failed)} failed ({time.time() - start:.0f} s)")
    print("ALL PASSED" if not failed else "FAILED: " + ", ".join(failed))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
