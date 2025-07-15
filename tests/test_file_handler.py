import __init__
import pytest
import os
import subprocess

from pathlib import Path
from tests.fixture import setup_file_handler_resource as setup
from unittest.mock import MagicMock, patch

def test_get_path(setup):
    file_name = "SQLAlchemy"
    path_to_file = f"{Path(__file__).parent}/terminal_note/{file_name}"
    assert setup.get_path(file_name) == path_to_file


def test_file_list(setup):
    file_list = [
        "SQLAlchemy.md",
        "SQL Case - When.md",
        "SQL Distinct.md",
        "SQL Filter.md",
        "SQL group_by.md",
        "SQL json_agg vs ORM.md",
        "SQL Агрегатные функции.md",
        "SQL Многие ко многим.md",
        "SQL Один к одному.md",
    ]
    for file_in_dir in file_list:
        assert file_in_dir in [str(file).split("/")[-1] for file in setup.file_list()]

def test_prompt_fzf(setup):
    file_list = [file for file in setup.file_list()]
    
    def mock_fzf():
        return ('', str(file_list[0]))

    def mock_prompt():
        return (str(file_list[1]), '')

    def mock_prompt_none():
        return ('', None)

    with patch("backend.file_handler.TerminalNote.prompt_fzf", return_value=mock_fzf()):
        result_fzf = setup.prompt_fzf()

    with patch("backend.file_handler.TerminalNote.prompt_fzf", return_value=mock_prompt()):
        result_prompt = setup.prompt_fzf()
    
    with patch("backend.file_handler.TerminalNote.prompt_fzf", return_value=mock_prompt_none()):
        result_prompt_none = setup.prompt_fzf()

    assert result_fzf == ('', str(file_list[0]))
    assert result_prompt == (str(file_list[1]), '')
    assert result_prompt_none == ('', None)

@pytest.fixture
def mock_prompt_fzf(setup):
    with patch.object(setup, 'prompt_fzf', return_value=(None, None)):
        yield

@pytest.fixture
def mock_create_on_template():
    return None

@pytest.fixture
def mock_create(setup):
    with patch.object(setup, 'create'):
        yield

@pytest.fixture
def mock_subprocess_run():
    with patch('subprocess.run') as mock:
        yield mock

@pytest.fixture
def mock_errors(setup):
    errors = {"template_is_not_exists": {2: "Шаблон не существует"}, "editor_error": {3: "Редактор не найден"}}
   
    with patch.object(setup, 'ERRORS', errors):
        yield

class TestUpdateMethod:
    def test_successful_open_editor(self, setup, mock_prompt_fzf, mock_create_on_template, mock_create, mock_subprocess_run, mock_errors):
        # Тест успешного открытия файла редактором
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        result = setup.update()
        assert result is None
        mock_subprocess_run.assert_called_once()
        
    def test_called_process_error(self, setup, mock_prompt_fzf, mock_create_on_template, mock_create, mock_subprocess_run, mock_errors):
        # Тест обработки ошибки процесса
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(cmd="", returncode=1)
        result = setup.update()
        assert isinstance(result, subprocess.CalledProcessError)
        
    def test_keyboard_interrupt(self, setup, mock_prompt_fzf, mock_create_on_template, mock_create, mock_subprocess_run, mock_errors):
        # Тест обработки клавиатурного прерывания
        mock_subprocess_run.side_effect = KeyboardInterrupt()
        result = setup.update()
        assert isinstance(result, KeyboardInterrupt)
        
    def test_not_a_directory_error(self, setup, mock_prompt_fzf, mock_create_on_template, mock_create, mock_subprocess_run, mock_errors):
        # Тест обработки ошибки отсутствия нужного каталога
        mock_subprocess_run.side_effect = NotADirectoryError()
        result = setup.update()
        assert result == {3: "Редактор не найден"}
        
    def test_template_creation(self, setup, mock_prompt_fzf, mock_create_on_template, mock_create, mock_subprocess_run, mock_errors):
        # Тест попытки создания нового файла при отсутствии шаблона
        result = setup.update()
        assert result is None

