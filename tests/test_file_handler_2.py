import __init__
import pytest

from tests.fixture import setup_file_handler_resource as setup
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_prompt_fzf(setup):
    with patch.object(setup, 'prompt_fzf', return_value=("test_delete.md", setup.PATH_TO_STORAGE)):
        yield

@pytest.fixture
def mock_remove():
    with patch('os.remove') as mock:
        yield mock

@pytest.fixture
def mock_errors(setup):
    errors = {"file_deleted": {5: "Файл удалён"}}
    with patch.object(setup, 'ERRORS', errors):
        yield

class TestDeleteMethod:
    def test_successful_delete(self, setup, mock_prompt_fzf, mock_remove, mock_errors):
        # Тест успешного удаления файла
        result = setup.delete()
        assert result == {5: "Файл удалён"}
        mock_remove.assert_called_once_with(setup.PATH_TO_STORAGE)

    def test_file_not_found(self, setup, mock_prompt_fzf, mock_remove, mock_errors):
        # Тест обработки ошибки FileNotFoundError
        mock_remove.side_effect = FileNotFoundError()
        result = setup.delete()
        assert isinstance(result, FileNotFoundError)

    def test_keyboard_interrupt(self, setup, mock_prompt_fzf, mock_remove, mock_errors):
        # Тест отмены операции
        mock_remove.side_effect = KeyboardInterrupt()
        result = setup.delete()
        assert isinstance(result, KeyboardInterrupt)

