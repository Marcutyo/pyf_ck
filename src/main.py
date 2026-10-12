import sys
from pathlib import Path
from typing import Final

from interpreter import build_jump_table, interpret

CODES_DIR: Final[Path] = Path(__file__).resolve().parent.parent / "codes"
ADMITTED_CODE_PATTERN: Final[set[str]] = set('+-><.,[]')


def _check_and_sanitize(code: str) -> str:
    code = "".join(code.split())
    if not all(c in ADMITTED_CODE_PATTERN for c in code):
        raise ValueError(f"Invalid code. Instructions permitted are: {ADMITTED_CODE_PATTERN}")
    return code


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
            texts.append(_check_and_sanitize(path.read_text(encoding="utf-8")))
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
            return [_check_and_sanitize(input("Write your code: \n"))]
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
        interpret(code, jump_table)


if __name__ == '__main__':
    main()
