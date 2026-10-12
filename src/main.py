import sys
from pathlib import Path
from typing import Final

from interpreter import build_jump_table, interpret, sanitize

CODES_DIR: Final[Path] = Path(__file__).resolve().parent.parent / "codes"


def _read_programs() -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    if not CODES_DIR.is_dir():
        print("❌ Folder 'codes/' not found.")
        sys.exit(1)

    programs: list[tuple[str, str]] = []  # (file name, code)
    failed: list[tuple[str, str]] = []  # (file name, reason)

    for path in sorted(CODES_DIR.iterdir()):
        if not path.is_file():
            continue
        try:
            programs.append((path.name, sanitize(path.read_text(encoding="utf-8"))))
        except (OSError, UnicodeDecodeError):
            failed.append((path.name, "unreadable file"))
        except ValueError as e:
            failed.append((path.name, str(e)))

    return programs, failed


def _ask_choice() -> str:
    print(
        "1) 📂 Run the programs in codes/\n"
        "2) ✍️  Write a program here"
    )
    while True:
        choice = input("> ").strip()
        if choice in ("1", "2"):
            print()
            return choice
        print("❌ Wrong input: type 1 or 2.")


def _get_programs() -> list[tuple[str, str]]:
    if _ask_choice() == "2":
        try:
            return [("your code", sanitize(input("✍️  Write your code: ")))]
        except ValueError as e:
            print(f"\n❌ {e}")
            sys.exit(1)

    programs, failed = _read_programs()

    if not programs and not failed:
        print("⚠️  No programs found in codes/.")
        sys.exit(1)

    print(f"✅ {len(programs)} file(s) read")
    for name, reason in failed:
        print(f"⚠️  Skipped {name}: {reason}")
    print()

    return programs


def _run(name: str, code: str) -> None:
    print(f"▶ {name}")
    try:
        jump_table: dict[int, int] = build_jump_table(code)
    except ValueError as e:
        print(f"   ❌ {e}\n")
        return

    print("   📤 Output: ", end="")
    try:
        memory: dict[int, int] = interpret(code, jump_table)
    except ValueError as e:
        print(f"\n   ❌ {e}\n")
        return

    print()
    print("   🧮 Memory: " + " ".join(f"[{idx}]={value}" for idx, value in memory.items()))
    print()


def main():
    print("🧠 pyf_ck · Brainfuck interpreter\n")

    for name, code in _get_programs():
        _run(name, code)


if __name__ == '__main__':
    main()
