install:
	pip uninstall terminal-note
	uv build
	pip install ~/code/terminal_note/dist/terminal_note-0.1.0-py3-none-any.whl

run_test:
	pytest -v tests
