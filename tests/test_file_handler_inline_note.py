import __init__
import pytest

from tests.fixture import setup_file_handler_resource as setup
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_open():
    with patch('builtins.open', create=True) as mock:
        yield mock

@pytest.fixture
def mock_errors(setup):
    errors = {"text_saved":  {6: "Заметка сохранена"}, "text_saved_error":  {7: "Ошибка при сохранении"}}
    with patch.object(setup, 'ERRORS', errors):
        yield

class TestInlineNoteMethod:
    def test_successful_write(self, setup, mock_open, mock_errors):
        # Тест успешной записи заметки
        result = setup.inline_note("Тестовая заметка")
        assert result == {6: "Заметка сохранена"}
        mock_open.assert_called_once()

    def test_os_error(self, setup, mock_open, mock_errors):
        # Тест обработки ошибки записи (OSError)
        mock_open.side_effect = OSError()
        result = setup.inline_note("Ошибка!")
        assert result == {7: "Ошибка при сохранении"}
