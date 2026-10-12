import sys
from pathlib import Path
from typing import Final

from interpreter import ADMITTED_CODE_PATTERN, build_jump_table, interpret, sanitize

CODES_DIR: Final[Path] = Path(__file__).resolve().parent.parent / "codes"


def _read_texts() -> tuple[list[str], list[str]]:
    if not CODES_DIR.is_dir():
        print("Folder '/codes' not found.")
        sys.exit(1)

    texts: list[str] = []
    failed: list[str] = []

    for path in sorted(CODES_DIR.iterdir()):
        if not path.is_file():
            continue
        try:
            texts.append(sanitize(path.read_text(encoding="utf-8")))
        except (OSError, UnicodeDecodeError):
            failed.append(path.name)
        except ValueError as e:
            print(f"{path.name}: {e}")
            failed.append(path.name)

    return texts, failed


def _ask_choice() -> str:
    while True:
        choice = input(
            "1: Read code(s) from folder (/codes)\n"
            "2: Write code here\n"
            "> "
        ).strip()
        if choice in ("1", "2"):
            return choice
        print("Wrong input: type 1 or 2.\n")


def _get_codes() -> list[str]:
    if _ask_choice() == "2":
        try:
            return [sanitize(input("Write your code: \n"))]
        except ValueError:
            print(f"Invalid code, try again. Instructions permitted are: {ADMITTED_CODE_PATTERN}\n")
            sys.exit(1)

    codes, failed = _read_texts()
    total: int = len(codes) + len(failed)

    if failed:
        print(f"{len(failed)}/{total} files are bad: {', '.join(failed)}")
    else:
        print(f"All {total} files correctly read.")

    return codes


def main():
    codes: list[str] = _get_codes()

    for code in codes:
        jump_table: dict[int, int] = build_jump_table(code)
        print("OUTPUT: ", end='')
        memory: dict[int, int] = interpret(code, jump_table)
        print()
        print('MEMORY STATUS')
        for k, v in memory.items():
            print(f'{k}: {v}')
        print()


if __name__ == '__main__':
    main()
