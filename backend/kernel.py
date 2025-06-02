from config import Config

import os
import sys

class TerminalNote(Config):
    def __init__(self):
        super()


if __name__ == "__main__":
    a = TerminalNote()
    sys.path()   
    print(os.path.exists(a.PATH_TO_STORAGE))
    print(a.PATH_TO_STORAGE)
