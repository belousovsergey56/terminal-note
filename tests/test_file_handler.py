import __init__
import pytest
import os

from pathlib import Path
from tests.fixture import setup_file_handler_resource as setup
from unittest.mock import patch

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

def test_create_file_created(setup):
    assert setup.create("test") == setup.ERRORS.get("file_created")

def test_create_file_exists(setup):
    created_file = f"{Path(__file__).parent}/terminal_note/test.md"
    file_list = [file for file in setup.file_list()]
    assert created_file in file_list
    assert setup.create("test") == setup.ERRORS.get("file_exists")
    os.remove(created_file)

def test_create_on_template_not_exists(setup):
    assert setup.create_on_template("test") == setup.ERRORS.get("template_is_not_exists")
    template = f"{Path(__file__).parent}/terminal_note/templates/template.md"
    if not Path(template).exists():
        Path(template).touch(438, True)
    with open(template, "w") as f:
        f.write("Template test text")

def test_create_on_template_created(setup):
    assert setup.create_on_template("test") == setup.ERRORS.get("file_created")

def test_create_on_template_exists(setup):
    assert setup.create_on_template("test") == setup.ERRORS.get("file_exists")

def test_file_created_on_template(setup):
    file = f"{Path(__file__).parent}/terminal_note/test.md"
    with open(file, "r") as f:
        text = f.read()
    assert "Template test text" == text
    os.remove(file)
    os.remove(f"{Path(__file__).parent}/terminal_note/templates/template.md")

