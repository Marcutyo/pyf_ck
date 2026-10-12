# pyf_ck

A simple Brainfuck interpreter written in Python, for educational purposes.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Usage

```bash
uv run src/main.py
```

The program asks how to provide the Brainfuck code:

1. **Read from the `codes/` folder**: every file in `codes/` (at the project root) is read and executed, in alphabetical order. Create the folder and put your programs there, one per file. The folder is git-ignored. Files that cannot be read or contain invalid characters are reported and skipped.
2. **Write the code in the terminal**: type a single program when prompted.

Whitespace and line breaks in the code are ignored. Any other character that is not a Brainfuck instruction (`+ - > < . , [ ]`) makes the code invalid.

After each program runs, its output is printed together with the final state of the memory cells that were used.

Some example programs are available in `samples/`. For instance, to try them:

```bash
mkdir codes
cp samples/Marco_1.txt codes/
uv run src/main.py
```

## How it works

Brainfuck has only 8 instructions and works on a "tape" of memory cells. The interpreter lives in `src/interpreter.py` and is made of two functions.

### The memory model

- The memory is a tape of cells, each one holding a value from 0 to 255. Going over the limits wraps around (`255 + 1 -> 0`, `0 - 1 -> 255`).
- A pointer indicates the current cell. The tape grows on demand in both directions, and every new cell starts at 0 (a `defaultdict` makes this trivial).

| Instruction | Meaning                                                     |
|-------------|-------------------------------------------------------------|
| `+` / `-`   | increment / decrement the current cell                      |
| `>` / `<`   | move the pointer to the next / previous cell                |
| `.`         | print the current cell as an ASCII character                |
| `,`         | read a single character and store it in the current cell    |
| `[`         | if the current cell is 0, jump after the matching `]`       |
| `]`         | jump back to the matching `[` (which checks the cell again) |

### The jump table

`[` and `]` form loops: the code between them is repeated until the current cell becomes 0. To do that, the interpreter must know which `]` matches which `[`, and nesting makes it non-trivial.

Instead of scanning the code for the match every time a loop starts or ends, `build_jump_table` does it **once, before the execution**. It reads the code and keeps a stack of the `[` still waiting for their `]`: the last one opened is the first one closed, so nested loops match correctly. The result is a dictionary that maps each bracket to its match, in both directions. For example, for the code `+[-]`:

```
{1: 3, 3: 1}
```

If a bracket cannot be matched, the code is invalid and a `ValueError` is raised.

### The execution loop

`interpret` walks through the code with an index `i` and acts on the current symbol:

- `+`, `-`, `>`, `<`, `.`, `,` do their job and move to the next symbol.
- `[` with the current cell at 0 sets `i` right after the matching `]`, skipping the loop body.
- `]` always sets `i` back to the matching `[`, which checks the cell again: if it is still not 0 the body runs once more, otherwise the loop is over.

Thanks to the jump table, each of these jumps is a single dictionary lookup.
