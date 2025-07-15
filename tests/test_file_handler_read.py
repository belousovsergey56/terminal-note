from os import setgroups
import pytest
from unittest.mock import MagicMock, patch, call
from pathlib import Path

import __init__
from tests.fixture import setup_file_handler_resource as setup

test_md_file = f"{Path(__file__).parent}/terminal_note/file.md"
test_txt_file = f"{Path(__file__).parent}/terminal_note/file.txt"

@patch("subprocess.run")
def test_read_file_not_found(mock_run, capsys, setup):

    setup.prompt_fzf = MagicMock(return_value=(test_txt_file, None))
    result = setup.read()    
    captured = capsys.readouterr()
    assert "Файл \033[32mfile.txt\033[0m не найден" in captured.out
    assert result is None
    mock_run.assert_not_called()

@patch("subprocess.run")
def test_read_md_file_success(mock_run, setup):
    setup.prompt_fzf = MagicMock(return_value=("file.md", test_md_file))
    
    result = setup.read()
    
    mock_run.assert_called_once_with(["frogmouth", str(test_md_file)], check=True)
    assert result is None

@patch("subprocess.run")
def test_read_other_extension_success(mock_run, setup):
    setup.prompt_fzf = MagicMock(return_value=("file.txt", test_txt_file))
    
    result = setup.read()
    
    mock_run.assert_called_once_with([setup.FILE_READER, str(test_txt_file)], check=True)
    assert result is None

def test_keyboard_interrupt_during_prompt(setup):
    setup.prompt_fzf = MagicMock(side_effect=KeyboardInterrupt)
    
    result = setup.read()
    
    assert isinstance(result, KeyboardInterrupt)

@patch("subprocess.run")
def test_keyboard_interrupt_during_md_open(mock_run, setup):
    setup.prompt_fzf = MagicMock(return_value=("file.md", test_md_file))
    mock_run.side_effect = KeyboardInterrupt
    
    result = setup.read()
    
    assert isinstance(result, KeyboardInterrupt)
    mock_run.assert_called_once_with(["frogmouth", str(test_md_file)], check=True)

@patch("subprocess.run")
def test_keyboard_interrupt_during_other_open(mock_run, setup):
    setup.prompt_fzf = MagicMock(return_value=("file.txt", test_txt_file))
    mock_run.side_effect = KeyboardInterrupt
    
    result = setup.read()
    
    assert isinstance(result, KeyboardInterrupt)
    mock_run.assert_called_once_with([setup.FILE_READER, str(test_txt_file)], check=True)
