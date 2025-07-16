import argparse

from backend.file_handler import TerminalNote
from backend.strategy import HandlerService
from sys import argv


def file_service():
    parser = argparse.ArgumentParser(
        description="Terminal-Note - консольная утилита для сохранения быстрых заметок в заранее определённую директорю и c заданым расширением файла.",
        epilog="Быстрая заметка: tn \"Начать читать С.Макконнел 'Совершенный код'\" или c флагом tn -i 'Повтортиь sql запросы'.",
        usage="\ntn [options text] [text]",
    )
    # Флаг -i, который требует текст
    parser.add_argument(
        "-i",
        nargs="?",
        const="",  # если -i без текста, то args.i == ''
        metavar="text",
        help='inline заметка, без открытия редактора. tn -i [text] сохраняется в файл в заданную директорию. Имя файла в фомате "дата время".',
    )
    # Позиционный аргумент — текст заметки
    parser.add_argument(
        "text",
        nargs="?",
        help='inline заметка, без открытия редактора. Не требует ввода флага -i: tn [text] - сохраняется в файл в заданную директорию. Имя файла в фомате "дата время".',
    )

    parser.add_argument(
        "-o",
        nargs="?",
        help="Вызывается fzf, в списке ищем нужный файл для редактирования. Если файла нет, то утилита создаст файл и редактор открывает новый файл.",
    )
    parser.add_argument(
        "-d",
        nargs="?",
        help="Вызывается fzf, выбираем из списка нужный файл для удаления или отменяем операцию.",
    )
    parser.add_argument(
        "-r",
        nargs="?",
        help="Вызывается fzf, выбираем из списка нужный файл для чтения. Если файл в формате .md, то файл откроется утилитой frogmouth, если файл имеет другое расширение, то файл будет прочитан утилитой на выбор: less, cat, bat. Утилиту нужно указать в конфиг файле.",
    )
    args = parser.parse_args()
    file_service = HandlerService(TerminalNote())
    note_text = None
    try:
        if args.i is not None:
            if args.i == "":
                parser.error("Флаг -i требует указания текста после него.")
            note_text = args.i
            file_service.inline_note(note_text)
        elif args.text:
            note_text = args.text
            file_service.inline_note(note_text)

        if argv[1] == "-r":
            file_service.read()

        if argv[1] == "-d":
            file_service.delete()

        if argv[1] == "-o":
            file_service.update()
    except IndexError:
        print("Используй tn --help для получения описания")


if __name__ == "__main__":
    file_service()
