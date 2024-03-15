import pytest
import json
from pathlib import Path
from unittest.mock import patch
from write_the.cli.model import get_config_path, get_default_model, set_default_model


@pytest.fixture
def mock_app_dir(tmp_path):
    return str(tmp_path / "app_dir")


@pytest.fixture
def mock_config_path(mock_app_dir):
    config_path = Path(mock_app_dir) / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    return config_path


@pytest.fixture
def mock_config():
    return {"default_model": "gpt-3.5-turbo-instruct"}


@pytest.fixture
def mock_config_file(mock_config_path, mock_config):
    with open(mock_config_path, "w") as f:
        json.dump(mock_config, f)
    return mock_config_path


@patch("write_the.cli.model.typer.get_app_dir")
def test_get_config_path(mock_get_app_dir, mock_app_dir, mock_config_path):
    mock_get_app_dir.return_value = mock_app_dir
    assert get_config_path() == mock_config_path
    assert mock_config_path.exists()

@patch("write_the.cli.model.typer.get_app_dir")
def test_get_default_model(mock_get_app_dir, mock_app_dir):
    mock_get_app_dir.return_value = mock_app_dir
    assert get_default_model() == "gpt-3.5-turbo-instruct"

@patch("write_the.cli.model.typer.get_app_dir")
def test_set_default_model(mock_get_app_dir, mock_app_dir, mock_config_path):
    mock_get_app_dir.return_value = mock_app_dir
    set_default_model("new_model")
    with open(mock_config_path, "r") as f:
        config = json.load(f)
    assert config["default_model"] == "new_model"
