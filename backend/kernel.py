from config import Config

import os
import subprocess


class TerminalNote(Config):
    def __init__(self):
        super().__init__()
        if not os.path.exists(self.PATH_TO_STORAGE):
            os.makedirs(self.PATH_TO_STORAGE)
    
    def get_path(self, file_name: str) -> str:
        """Создаёт переменную путь к файлу.
        Args:
            file_name (str): Имя файла
        Returns:
            str: Путь к файлу, пример: /home/belousov/terminal_note/file_name.md
        """
        file_path = f"{self.PATH_TO_STORAGE}/{file_name}.{self.EXTENSION}"
        return file_path

    def create_file(self, file_name: str) -> dict:
        """Создание файла.
        
        Args:
            file_name (str): Имя создаваемого файла
        Returns:
            dict: {200: "Файл создан", 400: "Файл существует"}

        """
        file_path = self.get_path(file_name)
        if not os.path.exists(file_path):
            with open(file_path, "w"):
                return {200: "Файл создан"}
        return {400: "Файл существует"}
    
    def edit_file(self, file_name: str) -> None|Exception:
        """Изменить файл.
        Функция открывает файл для его изменения в редакторе, который указан в
        в конфиге
        Args:
            file_name (str): Имя файла, который будем редактировать
        Returns:
            FileNotFoundError: Редактор указанный в конфиге не найден.
            subprocess.CalledProcessError: Ошибка при открытии файла.
            None: Если всё хорошо, то открывается редактор.
        """
        file_path = self.get_path(file_name)
        try:
            subprocess.run([self.EDITOR, file_path], check=True)
        except FileNotFoundError as e:
            return e
        except subprocess.CalledProcessError as e:
            return e

    def delete_file(self, file_name: str) -> dict:
        """Удалить файл.
        Args:
            file_name (str): Имя файла
        Returns:
            dict: {200: "Файл удалён", 400: "Файл не найден"}
        """
        file_path = self.get_path(file_name)
        if not os.path.exists(file_path):
            return {400: "Файл не найден"}
        os.remove(file_path)
        return {200: "Файл удалён"}


if __name__ == "__main__":
    a = TerminalNote()
