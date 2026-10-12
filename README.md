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

## Notes

- Memory is unbounded in both directions, and each cell is an unsigned 8-bit value (it wraps around at 256).
- The `,` instruction asks for a single character from the terminal.
