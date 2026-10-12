import os
import subprocess
import sys
from typing import Final

# ANSI escape codes: "\033[<number>m" tells the terminal to change the text style
RESET: Final[str] = "\033[0m"
BOLD: Final[str] = "\033[1m"
DIM: Final[str] = "\033[2m"

BLACK: Final[str] = "\033[30m"
RED: Final[str] = "\033[31m"
GREEN: Final[str] = "\033[32m"
YELLOW: Final[str] = "\033[33m"
CYAN: Final[str] = "\033[36m"
BRIGHT_WHITE: Final[str] = "\033[97m"

BG_BLUE: Final[str] = "\033[44m"
BG_CYAN: Final[str] = "\033[46m"

if os.name == "nt":
    subprocess.run("", shell=True)  # spawns a shell, which makes the legacy Windows console understand ANSI codes

# colors are used only when writing to a real terminal (not to a file or a pipe)
# and when the user did not opt out through the NO_COLOR convention (https://no-color.org)
COLORS_ENABLED: Final[bool] = sys.stdout.isatty() and "NO_COLOR" not in os.environ


def paint(text: str, *styles: str) -> str:
    """
    Wraps the text with the given ANSI styles, resetting them at the end.

    Parameters
    ----------
    text : str
        The text to style.
    *styles : str
        One or more style codes defined in this module (e.g. `BOLD`, `GREEN`).

    Returns
    -------
    str
        The styled text, or the text unchanged if colors are disabled.
    """
    if not COLORS_ENABLED:
        return text
    return "".join(styles) + text + RESET
