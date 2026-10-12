import sys
from pathlib import Path
from typing import Final

from interpreter import build_jump_table, interpret, sanitize
from style import BG_BLUE, BG_CYAN, BLACK, BOLD, BRIGHT_WHITE, CYAN, DIM, GREEN, RED, YELLOW, paint

CODES_DIR: Final[Path] = Path(__file__).resolve().parent.parent / "codes"


def _error(message: str) -> str:
    return paint(f"❌ {message}", RED)


def _read_programs() -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    if not CODES_DIR.is_dir():
        print(_error("Folder 'codes/' not found."))
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
        f"{paint('1)', BOLD, CYAN)} 📂 Run the programs in codes/\n"
        f"{paint('2)', BOLD, CYAN)} ✍️  Write a program here"
    )
    while True:
        choice = input(paint(">", BOLD, CYAN) + " ").strip()
        if choice in ("1", "2"):
            print()
            return choice
        print(_error("Wrong input: type 1 or 2."))


def _get_programs() -> list[tuple[str, str]]:
    if _ask_choice() == "2":
        try:
            return [("your code", sanitize(input("✍️  Write your code: ")))]
        except ValueError as e:
            print(f"\n{_error(str(e))}")
            sys.exit(1)

    programs, failed = _read_programs()

    if not programs and not failed:
        print(paint("⚠️  No programs found in codes/.", YELLOW))
        sys.exit(1)

    print(paint(f"✅ {len(programs)} file(s) read", GREEN))
    for name, reason in failed:
        print(f"{paint(f'⚠️  Skipped {name}', YELLOW)} {paint(reason, DIM)}")
    print()

    return programs


def _format_memory(memory: dict[int, int]) -> str:
    # zero cells are dimmed so the cells actually used by the program stand out
    return " ".join(
        paint(f"[{idx}]={value}", DIM) if value == 0 else paint(f"[{idx}]={value}", BOLD, CYAN)
        for idx, value in memory.items()
    )


def _run(name: str, code: str) -> None:
    print(paint(f" ▶ {name} ", BOLD, BLACK, BG_CYAN))
    try:
        jump_table: dict[int, int] = build_jump_table(code)
    except ValueError as e:
        print(f"   {_error(str(e))}\n")
        return

    print(f"   📤 {paint('Output:', DIM)} ", end="")
    try:
        memory: dict[int, int] = interpret(code, jump_table)
    except ValueError as e:
        print(f"\n   {_error(str(e))}\n")
        return

    print()
    print(f"   🧮 {paint('Memory:', DIM)} {_format_memory(memory)}")
    print()


def main():
    print(paint(" 🧠 pyf_ck · Brainfuck interpreter ", BOLD, BRIGHT_WHITE, BG_BLUE) + "\n")

    for name, code in _get_programs():
        _run(name, code)


if __name__ == '__main__':
    main()
