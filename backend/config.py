import tomllib

path_to_config = "config.toml"

class Config:
    with open(path_to_config, "rb") as f:
        config_data = tomllib.load(f)
    
    PATH_TO_STORAGE = config_data["backend"]["path_to_storage_directory"]
    PATH_TO_CONFIG_TN = config_data["backend"]["path_to_config_tn"]
    EXTENSION = config_data["backend"]["file_extension"]
    PATH_TO_TEMPLATE_FILE = config_data["template"]["path_to_template_note"]
    EDITOR = config_data["editor"]["editor"]
    ERRORS = {
            "file_created": {0: "Файл создан"},
            "file_exists": {1: "Файл существует"},
            "template_is_not_exists": {2: "Шаблон не существует"},
            "editor_error": {3: "Редактор не найден"},
            "file_is_not_exists": {4: "Файл не существует"},
            "file_deleted": {5: "Файл удалён"},
            "text_saved": {6: "Заметка сохранена"},
            "text_saved_error": {7: "Ошибка при сохранении"}
            }
