import __init__
import pytest 
from pathlib import Path
from backend.file_handler import TerminalNote

def config(monkeypatch, suffix):
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

    monkeypatch.setattr(f"{suffix}.MODE", "files")
    monkeypatch.setattr(f"{suffix}.EDITOR", "nvim")
    monkeypatch.setattr(f"{suffix}.EXTENSION", "md")
    monkeypatch.setattr(f"{suffix}.PATH_TO_TEMPLATE_FILE", f"{Path(__file__).parent}/terminal_note/templates/template.md")
    monkeypatch.setattr(f"{suffix}.PATH_TO_STORAGE", f"{Path(__file__).parent}/terminal_note")
    monkeypatch.setattr(f"{suffix}.FILE_READER", "bat")
    monkeypatch.setattr(f"{suffix}.ERRORS", errors)


@pytest.fixture
def setup_config_resource(monkeypatch):
    suffix = "backend.config.config"
    config(monkeypatch, suffix)

@pytest.fixture
def setup_file_handler_resource(monkeypatch):
    suffix = "backend.file_handler.TerminalNote"
    config(monkeypatch, suffix)
    tn = TerminalNote()
    return tn


