from sys import argvs

import __init___
from backend.config import config
from backend.file_handler import TerminalNote
from backend.strategy import HandlerService


def file_service(mode, text):
    file_service = HandlerService(TerminalNote())
    modes = {
            "inline": file_service.inline_note(text),
            "read": file_service.read(),
            "open": file_service.update(),
            "delete": file_service.delete()
            }
    return modes.get(mode)
