[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/belousovsergey56/terminal-note/actions/workflows/Tests.yml/badge.svg?branch=main)](https://github.com/belousovsergey56/terminal-note/actions/workflows/Tests.yml)

# terminal-note
Консольная утилита для создания и управления заметками без выхода из терминала.

# Содержание
- [Мотивация](#мотивация)
-  [Особенности](#особенности)
-   [Установка](#установка)
-   [Использвание](#использование)
-   [Демонстрация](#демонстрация)
-   [Зависимости](#зависимости)
-   [Файл конфигурации](#файл-конфигурации)
-   [Структура хранилища](#структура-хранилища)
-   [Пример шаблона template.md](#пример-шаблона-templatemd)
-   [Идеи](#идеи)

## Мотивация
Я работаю преимущественно в терминале и использую инструменты вроде `nvim`, `rg`, `fd`, `fzf`. Для ведения заметок использую Obsidian — он хранит заметки локально в отдельных `.md` - файлах, что очень удобно. Однако запуск Obsidian занимает время, а постоянное переключение между терминалом и GUI-приложением нарушает поток работы.

Чтобы оставаться в терминале, я написал `terminal-note` — утилиту, позволяющую быстро создавать, искать и управлять заметками прямо из консоли.

## Особенности
- Возможность создания заметоки одной командой без открытия редактора.
- Поиск, открытие, удаление и чтение заметок с помощью `fzf`.
- Заметки сохраняются в формате Markdown (`.md`).
- Поддержка шаблонов и гибкая настройка через конфиг.
- Работает с выбранной директорией — легко интегрируется с Obsidian.
- Написание заметки в любимом консольном редакторе: nvim, micro и другие.

## Установка
1. Установите через pip:
   ```bash
   pip install terminal-note --user
   ```
2. Проверьте, что всё работает:
    ```bash
    tn --help
    ```

# Использование
- `tn --config` или `tn -c` — открыть конфигурационный файл.
- `tn "текст заметки"` — создать быструю заметку. Файл будет назван по шаблону (`2025-04-05 15:30:00.md`) и сохранён в указанной директории.
- `tn -o` — создать или открыть заметку. Сначала вводится имя файла, затем открывается редактор. Если файл существует — редактируется, если нет — создаётся.
- `tn -d` — удалить заметку. Через `fzf` выбирается файл для удаления.
- `tn -r` — прочитать заметку. Через `fzf` выбирается файл, который открывается в `frogmouth` (парсит Markdown с поддержкой навигации).

### Демонстрация
##### Вызов справки
![Вызов справки](https://github.com/belousovsergey56/notes/blob/main/assets/help.gif)

###### Редактирование конфиг файла
![Конфиг файл](https://github.com/belousovsergey56/notes/blob/main/assets/config.gif)

###### Быстрая заметка
![inline note](https://github.com/belousovsergey56/notes/blob/main/assets/inlinenote.gif)

###### Редактировать заметку
![edit](https://github.com/belousovsergey56/notes/blob/main/assets/edit.gif)

###### Новая заметка
![new note](https://github.com/belousovsergey56/notes/blob/main/assets/newfile.gif)

###### Удалить заметку
![delete note](https://github.com/belousovsergey56/notes/blob/main/assets/delete.gif)

###### Чтение заметки
![read](https://github.com/belousovsergey56/notes/blob/main/assets/read.gif)


# Зависимости
- python >= 3.11
- iterfzf >= 1.8.0.62.0
- frogmouth >= 0.9.2

# Файл конфигурации
```toml
# Хранение только в файлах
storage_mode = "files"

# Путь к директории, где будут храниться заметки.
# Скрипт парсит только переменную $HOME. Если нужен особенныый путь, то нужно его прописать полностью.
path_to_storage_directory = "$HOME/terminal_note"

# Расширение файла с заметкой: txt, md (без точки .md)
file_extension = "md"

# Утилита для чтения не md файлов: bat, cat, less
file_reader = "cat"

# Путь к файлу с шаблоном.
path_to_template_note = "$HOME/terminal_note/Templates/template.md"

# Редактор в котором удобно писать заметки: vi, vim, nvim, micro, nano и т.д.
editor = "vi"
```

### Структура хранилища
Пример структуры хранилища.
```bash
➜  ~ tree terminal_note
$HOME/terminal_note/
├── 2025-07-22 22:32:26.md
├── 2025-07-22 22:34:56.md
├── 2025-07-27 00:41:52.md
├── Gurtam
│   ├── 1. Виалон.md
│   ├── 2. Авторизация по токену.md
│   └── 3. Поиск элементов.md
├── My Book.md
└── Templates
    └── template.md

3 directories, 8 files
```
### Пример шаблона (template.md)
```markdown
---
Дата создания:
Дата изменения:
ссылки:
tags:
---
```

# Идеи
- [ ] Интеграция с Git: `tn -g` выполнит `pull`, `add`, `commit`, `push`.
- [ ] Поддержка хранения в базе данных (пока не точно — т.к нарушает совместимость с Obsidian).
- [ ] Возможно стоит сделать запись inline заметок в отдельную директорию, чтобы было легче искать.

