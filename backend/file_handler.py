import __init__
from backend.config import Config
from backend.strategy import HandlerStrategy
from datetime import datetime

import os
import subprocess



class TerminalNote(Config, HandlerStrategy):
    def __init__(self):
        super().__init__()
        if not os.path.exists(self.PATH_TO_STORAGE):
            os.makedirs(self.PATH_TO_STORAGE)
        self.ERRORS: dict[str, dict[int, str]]

    def get_path(self, file_name: str) -> str:
        """Создаёт переменную путь к файлу.
        Args:
            file_name (str): Имя файла
        Returns:
            str: Путь к файлу, пример: /home/belousov/terminal_note/file_name.md
        """
        file_path = f"{self.PATH_TO_STORAGE}/{file_name}"
        return file_path

    def create(self, file_name: str) -> dict[int, str] | None:
        """Создание файла.

        Args:
            file_name (str): Имя создаваемого файла
        Returns:
            dict: {0: "Файл создан"}, {1: "Файл существует"}

        """
        file_path = f"{self.get_path(file_name)}.{self.EXTENSION}"
        if not os.path.exists(file_path):
            with open(file_path, "w"):
                return self.ERRORS.get("file_created")
        return self.ERRORS.get("file_exists")

    def create_on_template(self, file_name: str) -> dict[int, str] | None:
        """Создать файл по шаблону.
        Создаёт файл на основании шаблона пользователя.
        Args:
            file_name (str): имя файла, который создаём

        Returns:
            dict[int, str]:
                {0: "Файл создан"},
                {1: "Файл существует"},
                {2: "Шаблон не существует"},

        """
        file_path = f"{self.get_path(file_name)}.{self.EXTENSION}"
        if not os.path.exists(self.PATH_TO_TEMPLATE_FILE):
            return self.ERRORS.get("template_is_not_exists")
        if not os.path.exists(file_path):
            with open(self.PATH_TO_TEMPLATE_FILE, "r") as t:
                template = t.read()
            with open(file_path, "w") as f:
                f.write(template)
            return self.ERRORS.get("file_created")
        return self.ERRORS.get("file_exists")

    def edit(self, file_name: str) -> None | dict[int, str] | Exception:
        """Изменить файл.
        Функция открывает файл для его изменения в редакторе, который указан в
        в конфиге
        Args:
            file_name (str): Имя файла, который будем редактировать
        Returns:
            dict[int, str]: {3: "Редактор не найден"},
            subprocess.CalledProcessError: Ошибка при открытии файла.
            None: Если всё хорошо, то открывается редактор.
        """
        try:
            subprocess.run([self.EDITOR, file_name], check=True)
        except FileNotFoundError:
            return self.ERRORS.get("editor_error")
        except subprocess.CalledProcessError as e:
            return e

    def delete(self, file_name: str) -> dict[int, str] | None:
        """Удалить файл.
        Args:
            file_name (str): Имя файла
        Returns:
            dict: {5: "Файл удалён", 4: "Файл не существет"}
        """
        file_path = self.get_path(file_name)
        if not os.path.exists(file_path):
            return self.ERRORS.get("file_is_not_exists")
        os.remove(file_path)
        return self.ERRORS.get("file_deleted")

    def inline_note(self, text: str) -> dict[int, str] | None:
        """Записать однострочную заметку.

        При запсиси одностройчной заметки создаётся файл в хранилище
        С указанным расширением, имя файла генерируется автоматически в формате
        даты и времени "2025-05-06 13:26:15"

        Args:
            text (str): строка, текст быстрой заметки
        Returns:
            dict[int,str]: {6: "Заметка сохранена"}, {7: "Ошибка при сохранении}
            None: Если ошибки нет в списке
        """
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_path = f"{self.get_path(date)}.{self.EXTENSION}"
        try:
            with open(file_path, "w") as f:
                f.writelines(f"{text}\n")
            return self.ERRORS.get("text_saved")
        except OSError:
            return self.ERRORS.get("text_saved_error")

    def read(self, file_name: str) -> str:
        """Прочитать файл.
        Функция читает файл и возвращавет его содержимое.

        Args:
            file_name (str): имя файла

        Returns:
            str: содержимое файла

        """
        file_path = self.get_path(file_name)
        with open(file_path, "r") as f:
            return f.read()

    def show_tree(self) -> list[str]:
        """Вывести список файлов в директории
        Returns:
            list[str]: список директорий и файлоа
        """
        return os.listdir(self.PATH_TO_STORAGE)



