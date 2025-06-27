import __init__

from pathlib import Path
from tests.fixture import setup_file_handler_resource as setup



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
    files = setup.file_list()
    for file_in_dir in list(files):
        assert file_in_dir.split("/")[-1] in file_list

def test_prompt_fzf(setup):
    pass
