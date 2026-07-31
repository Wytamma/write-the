import json
from pathlib import Path

import requests
import typer
from typing import Optional


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

def fetch_openrouter_models(
        url: str = "https://openrouter.ai/api/v1/models",
        api_key: str | None = None,
        timeout: float = 30.0,
        outfile: Path = None,
        companies: list[str] | None = None,
    ):
    """Fetch model metadata from OpenRouter and return a dict keyed by model ID."""
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    response = requests.get(url, headers=headers, timeout=59)
    response.raise_for_status()

    payload = response.json()
    try:
        data = payload["data"]
    except KeyError as e:
        raise ValueError(f"Unexpected API response: missing 'data' key. Keys: {list(payload.keys())}") from e

    # ormodels = {m["id"]: m for m in data if "id" in m}
    ormodels = {
        m["id"]: m | {"company": m["id"].split('/')[0]}
        for m in data
        if "id" in m and (companies is None or m["id"].split('/')[0] in companies)
    }

    if outfile:
        with open(outfile, 'w', encoding='utf-8') as f:
            json.dump(ormodels, f, indent=4)

    return ormodels

def display_models_table(models: dict, default_model: str, filter_by_company: Optional[str] = None, show_free: bool = True):
    """Renders the models dictionary into a Rich table."""
    from rich import print
    from rich.table import Table

    table_ = Table()
    table_.add_column("Name", justify="left", style="cyan")
    table_.add_column("Company", justify="left", style="cyan")
    table_.add_column("Context", justify="left", style="magenta")
    table_.add_column("Free", justify="left", style="magenta")
    table_.add_column("Default", justify="left", style="green")

    for name, model in sorted(models.items()):
        # Safeguard against missing context_window key in API response
        context = model.get("context_length", "N/A")
        actual_company = model.get("company", "Unknown")
        is_free = name.split(":")[1] == "free" if ":" in name else False


        if filter_by_company and filter_by_company.lower() != actual_company.lower():
            continue
        if show_free and not is_free:
            continue
        checkmark_default = "✅" if name == default_model else ""
        checkmark_free = "✅" if is_free else ""
        table_.add_row(actual_company, name, str(context), checkmark_free, checkmark_default)

    print(table_)