import __init__
import os
import pytest
from pathlib import Path
from tests.fixture import setup_file_handler_resource as setup
from unittest.mock import patch, mock_open, MagicMock

def test_create_file_created(setup):
    """Тест создания файла (успешное создание)."""
    # Мокаем проверку существования файла (вернет False) и операцию открытия файла
    with patch('os.path.exists', return_value=False):
        with patch('builtins.open', mock_open()) as mock_file:
            result = setup.create("test")
            assert result == setup.ERRORS.get("file_created")
            # Проверяем, что файл открывался на запись
            mock_file.assert_called_once()

def test_create_file_exists(setup):
    """Тест создания файла (файл уже существует)."""
    # Мокаем проверку существования файла (вернет True)
    with patch('os.path.exists', return_value=True):
        # Мокаем open и проверяем, что он не вызывался
        with patch('builtins.open') as mock_open:
            result = setup.create("test")
            assert result == setup.ERRORS.get("file_exists")
            mock_open.assert_not_called()

def test_create_on_template_not_exists(setup):
    """Тест создания по шаблону (шаблон не существует)."""
    # Мокаем проверку существования: для шаблона False, для файла не важно
    with patch('os.path.exists', side_effect=lambda x: False if x == setup.PATH_TO_TEMPLATE_FILE else True):
        result = setup.create_on_template("test")
        assert result == setup.ERRORS.get("template_is_not_exists")

def test_create_on_template_created(setup):
    """Тест создания по шаблону (успешное создание)."""
    # Мокаем пути: шаблон существует, файл - нет
    with patch('os.path.exists', side_effect=lambda x: True if x == setup.PATH_TO_TEMPLATE_FILE else False):
        # Мокаем чтение шаблона и запись файла
        with patch('builtins.open', mock_open(read_data="Template content")) as mock_file:
            result = setup.create_on_template("test")
            assert result == setup.ERRORS.get("file_created")
            
            # Проверяем вызовы
            mock_file.assert_any_call(setup.PATH_TO_TEMPLATE_FILE, 'r')
            mock_file.assert_any_call(f"{setup.get_path('test')}.{setup.EXTENSION}", 'w')
            
            # Проверяем запись содержимого
            handle = mock_file()
            handle.write.assert_called_once_with("Template content")

def test_create_on_template_exists(setup):
    """Тест создания по шаблону (файл уже существует)."""
    # Мокаем проверку: и шаблон и файл существуют
    with patch('os.path.exists', return_value=True):
        # Мокаем open и проверяем отсутствие вызовов
        with patch('builtins.open') as mock_open:
            result = setup.create_on_template("test")
            assert result == setup.ERRORS.get("file_exists")
            mock_open.assert_not_called()
