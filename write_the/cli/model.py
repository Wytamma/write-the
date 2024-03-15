import typer
import json
from pathlib import Path


def get_config_path():
    APP_NAME = "write-the"
    app_dir = typer.get_app_dir(APP_NAME)
    config_path: Path = Path(app_dir) / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    if not config_path.exists():
        with open(config_path, "w") as f:
            json.dump({}, f)
    return config_path

def get_default_model():
    config_path = get_config_path()
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config["default_model"]
    except Exception:
        return "gpt-3.5-turbo-instruct"

def set_default_model(model: str):
    config_path = get_config_path()
    config = {}
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except Exception:
        pass
    config["default_model"] = model
    with open(config_path, "w") as f:
        json.dump(config, f)