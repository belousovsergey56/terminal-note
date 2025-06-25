import __init__
from backend.config import config

def test_mode_field():
    mode = {"SQL": "SQL", "JSON": "JSON", "files": "files"}
    assert mode.get(config.MODE) is not None


def test_errors_field():
    errors = {
            "file_created": {0: "Файл создан"},
            "file_exists": {1: "Файл существует"},
            "template_is_not_exists": {2: "Шаблон не существует"},
            "editor_error": {3: "Редактор не найден"},
            "file_is_not_exists": {4: "Файл не существует"},
            "file_deleted": {5: "Файл удалён"},
            "text_saved": {6: "Заметка сохранена"},
            "text_saved_error": {7: "Ошибка при сохранении"},
            }
    for key, value in errors.items():
        assert config.ERRORS.get(key) == value

def test_extension_field():
    assert config.EXTENSION == "md"

def test_editor_field():
    editors = {"vim": "vim",
               "nvim": "nvim",
               "vi": "vi",
               "nano": "nano",
               "micro": "micro",
               }
    assert editors.get(config.EDITOR) is not None

def test_path_to_template_file():
    path = "/home/belousov/terminal_note/templates/template.md"
    assert path == config.PATH_TO_TEMPLATE_FILE


def test_file_reader():
    reader = {
            "cat": "cat",
            "bat": "bat",
            "less": "less",
            }
    assert reader.get(config.FILE_READER) is not None

def test_path_to_storage():
    path = "/home/belousov/terminal_note"
    assert path == config.PATH_TO_STORAGE


