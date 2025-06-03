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
