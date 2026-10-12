from collections import defaultdict
from typing import Final

ADMITTED_CODE_PATTERN: Final[set[str]] = set('+-><.,[]')


def sanitize(code: str) -> str:
    """
    Removes the whitespace from the code and checks that only Brainfuck
    instructions are left.

    Parameters
    ----------
    code : str
        The raw string of Brainfuck code.

    Returns
    -------
    str
        The code without whitespace and line breaks.

    Raises
    ------
    ValueError
        If the code contains a character that is not a Brainfuck instruction.
    """
    code = "".join(code.split())
    if not all(c in ADMITTED_CODE_PATTERN for c in code):
        raise ValueError(f"Invalid code. Instructions permitted are: {ADMITTED_CODE_PATTERN}")
    return code


def build_jump_table(code: str) -> dict[int, int]:
    """
    Builds the bidirectional jump table used by the interpreter.

    The jump table maps the index of each bracket to the index of its matching
    one, in both directions: '[' -> ']' and ']' -> '['. It is computed once,
    before the execution, so that the interpreter can jump between brackets
    in constant time instead of scanning the code looking for the match
    every time a loop starts or ends.

    Example: for the code "+[-]" the table is {1: 3, 3: 1}.

    Parameters
    ----------
    code : str
        The string of Brainfuck code to process.

    Returns
    -------
    dict[int, int]
        Bidirectional jump table.

    Raises
    ------
    ValueError
        If a closing bracket has no opening bracket before it, or if at the
        end of the reading one or more opening brackets remained unmatched.
    """
    # stack of '[' still waiting for their ']': the last one opened is the first one closed,
    # which is what makes nested loops match correctly
    unmatched_open_idxs: list[int] = []
    jump_table: dict[int, int] = {}

    for i, symbol in enumerate(code):
        if symbol == '[':
            unmatched_open_idxs.append(i)
        elif symbol == ']':
            if not unmatched_open_idxs:
                raise ValueError(f"Found closing bracket at index {i} without any opening brackets available")
            closing_idx: int = i
            opening_idx: int = unmatched_open_idxs.pop()

            jump_table[opening_idx] = closing_idx
            jump_table[closing_idx] = opening_idx

    if unmatched_open_idxs:
        raise ValueError(f"Could not find match for bracket(s) at index(es): {unmatched_open_idxs}")

    return jump_table



def interpret(
        code: str,
        jump_table: dict[int, int]
) -> None:
    """
    Executes a Brainfuck program, then prints the final state of the memory.

    The memory is a tape of cells, each holding a value between 0 and 255
    (it wraps around when going over the limits). A pointer tells which cell
    is the current one, and the instructions move it or change its value.

    Instruction set:
        '+' / '-' : increment / decrement the current cell
        '>' / '<' : move the pointer to the next / previous cell
        '.'       : print the current cell as an ASCII character
        ','       : read a single character and store it in the current cell
        '['       : if the current cell is 0, jump after the matching ']'
        ']'       : jump back to the matching '[' (which checks the cell again)

    Parameters
    ----------
    code : str
        The sanitized string of Brainfuck code to execute.
    jump_table : dict[int, int]
        Bidirectional jump table of the code, as built by `build_jump_table`.

    Raises
    ------
    ValueError
        If the code contains an unknown symbol, or if the input given to ','
        is not a single character.
    """
    # defaultdict gives every cell a starting value of 0 and lets the tape
    # grow on demand in both directions (negative indexes included)
    cells: dict[int, int] = defaultdict(int)

    pointer_idx: int = 0

    i: int = 0
    while i < len(code):
        current_symbol: str = code[i]

        if current_symbol == '+':
            cells[pointer_idx] += 1
            cells[pointer_idx] %= 256  # wrap around: 255 + 1 -> 0
            i += 1
        elif current_symbol == '-':
            cells[pointer_idx] -= 1
            cells[pointer_idx] %= 256  # wrap around: 0 - 1 -> 255
            i += 1
        elif current_symbol == '>':
            pointer_idx += 1
            i += 1
        elif current_symbol == '<':
            pointer_idx -= 1
            i += 1
        elif current_symbol == '.':
            print(chr(cells[pointer_idx]), end='')
            i += 1
        elif current_symbol == ',':
            while True:
                try:
                    user_input: int = ord(input("Write a single character: "))
                except ValueError:
                    raise ValueError('Invalid input. Expected 1 single character.')
                else:
                    break
            cells[pointer_idx] = user_input % 256
            i += 1
        elif current_symbol == '[':
            if cells[pointer_idx] == 0:
                closing_idx: int = jump_table[i]  # skip the loop body entirely
                i = closing_idx + 1  # move 1 index after closing bracket to continue program
            else:
                i += 1
        elif current_symbol == ']':
            opening_idx: int = jump_table[i]
            i = opening_idx  # move to the opening bracket index to check for cell value
        else:
            raise ValueError(f'Unknown symbol: {current_symbol!r}')

    print()
    _print_memory(cells)
    print()


def _print_memory(cells: dict[int, int]) -> None:
    print('MEMORY STATUS')
    for k, v in cells.items():
        print(f'{k}: {v}')
