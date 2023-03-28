from typing import Any
import json
from time import time

from pathlib import Path

SAVE_FOLDER_PATH = f"{str(Path.home())}/Pipopipette"
SAVE_FILE_PATH = f"{SAVE_FOLDER_PATH}/settings.json"

DEFAULT_SETTINGS = {
    "timer": 60
}

def integrity_check(settings: dict[str, Any]) -> dict[str, Any]:
    """Ensures the integrity of the save data

    Args:
        settings (dict[str, Any]): Settings to check for

    Returns:
        dict[str, Any]: Settings with checked integrity
    """
    for setting_name in settings:
        if setting_name not in DEFAULT_SETTINGS:
            settings.pop(setting_name)

    if (
        "timer" in settings
        and (type(settings["timer"]) != int)
        or (settings["timer"] < 0)
    ):
        settings.pop("timer")
    return settings

def __ensure_exists():
    """Ensures the save folder path and file exists, and are not corrupted.
    """
    # Create the folder
    Path(SAVE_FOLDER_PATH).mkdir(parents=True, exist_ok=True)
    # Create the save file if it doesn't exist
    if not Path(SAVE_FILE_PATH).is_file():
        with open(SAVE_FILE_PATH, 'w') as f:
            f.write("{}")

    # Try and read the save file to see if it's corrupted,
    # if it is, make a backup of the old one and create a new one
    with open(SAVE_FILE_PATH) as json_file:
        try:
            json.load(json_file)
        except json.JSONDecodeError as e:
            print("The settings file is corrupted! Creating a new one..")
            print(f"(Error: {e})")
            corrupted_file = Path(SAVE_FOLDER_PATH)
            corrupted_file.rename(Path(f"{SAVE_FOLDER_PATH}/{time()}.json"))
            with open(SAVE_FILE_PATH, 'w') as f:
                f.write("{}")

def save(settings: dict[str, Any]):
    """Saves the data to the save location

    Args:
        settings (dict[str, Any]): Settings to save
    """
    __ensure_exists()
    settings = integrity_check(settings)
    with open(SAVE_FILE_PATH, 'w') as f:
        json.dump(settings, f)

def get_settings() -> dict[str, Any]:
    """Obtains the settings from the save file

    Returns:
        dict[str, Any]: Settings
    """
    __ensure_exists()
    with open(SAVE_FILE_PATH, 'r') as f:
        settings: dict[str, Any] = json.load(f)
    for setting, default_value in DEFAULT_SETTINGS.items():
        if setting not in settings:
            settings[setting] = default_value
    settings = integrity_check(settings)
    return settings