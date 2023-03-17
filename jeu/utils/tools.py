import tkinter
import tkinter.filedialog
from enum import Enum, IntEnum


def prompt_for_file(file_kind: str, extensions: list[str]) -> str:
    """Creates a dialog prompting the user for a specific kind of file

    Args:
        file_kind (str): Type of files (Images, Excel document, Executables...)
        extensions (list[str]): Extensions to open (*.png, *.jpg, ...)

    Returns:
        str: Path of the chosen file
    """
    top = tkinter.Tk()
    top.withdraw()
    file_name = tkinter.filedialog.askopenfilename(filetypes=[(file_kind, ' '.join(extensions))])
    top.destroy()
    return file_name

class gamemode(IntEnum):
    LOCAL = 0
    AI = 1
    ONLINE = 2