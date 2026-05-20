import json
from pathlib import Path


CONFIG_PATH = Path("config.json")


DEFAULT_CONFIG = {
    "agent": {
        "max_iterations": 5,
        "approval_required": False,
    },
    "paths": {
        "default_log_file": "data/sample_logs/app.log",
        "reports_dir": "data/reports",
        "audit_dir": "audit_logs",
    },
    "tools": {
        "default_process_limit": 5,
        "default_process_sort": "cpu",
        "default_disk_path": ".",
    },
}


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return DEFAULT_CONFIG

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        user_config = json.load(file)

    config = DEFAULT_CONFIG.copy()

    for section, values in user_config.items():
        if section in config and isinstance(values, dict):
            config[section].update(values)
        else:
            config[section] = values

    return config