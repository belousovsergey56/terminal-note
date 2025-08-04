install:
	pip uninstall terminal-note
	uv build
	pip install ~/code/terminal-note/dist/terminal_note-0.9.0-py3-none-any.whl

run_test:
	pytest -v tests
