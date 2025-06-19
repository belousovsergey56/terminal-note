import __init__

from sys import argv
from backend.strategy import HandlerService
from backend.file_handler import TerminalNote

def main():
    file_service = HandlerService(TerminalNote())
    file_service.inline_note(argv[1])

if __name__ == "__main__":
   main()
