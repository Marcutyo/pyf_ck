from collections import defaultdict


def build_jump_table(code: str) -> dict[int, int]:
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
    cells: dict[int, int] = defaultdict(int)

    pointer_idx: int = 0

    i: int = 0
    while i < len(code):
        current_symbol: str = code[i]

        if current_symbol == '+':
            cells[pointer_idx] += 1
            cells[pointer_idx] %= 256
            i += 1
        elif current_symbol == '-':
            cells[pointer_idx] -= 1
            cells[pointer_idx] %= 256
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
                closing_idx: int = jump_table[i]
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
