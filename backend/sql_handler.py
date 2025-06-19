import __init__
from backend.config import Config
from backend.strategy import HandlerStrategy
from datetime import datetime

import os
import subprocess

class SQLTerminalNote(Config, HandlerStrategy):
    def __init__(self):
        super().__init__()
        self.ERRORS: dict[str, dict[int, str]]
        self.DB.execute("""CREATE TABLE IF NOT EXISTS terminal_note (
                           terminal_note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                           title TEXT NOT NULL,
                           note TEXT)""")

    def get_path(self):
        print(self.PATH_TO_STORAGE)

    def create(self):
        pass
    
    def edit(self):
        pass
    
    def create_on_template(self):
        pass

    def inline_note(self):
        pass

    def read(self):
        a = self.DB.execute("""SELECT * FROM terminal_note""")
        print(a.fetchall())
    
    def show_tree(self):
        pass

    def delete(self):
        pass

if __name__ == "__main__":
    a = SQLTerminalNote()
    a.read()
