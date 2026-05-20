import json
from pathlib import Path


CONFIG_PATH = Path("config.json")


DEFAULT_CONFIG = {
    "agent": {
        "max_iterations": 5,
        "approval_required": False,
    },
    "llm": {
        "provider": "openrouter",
        "openrouter_model": "openrouter/free",
        "ollama_model": "llama3.1",
        "ollama_base_url": "http://host.docker.internal:11434/v1",
    },
    "paths": {
        "default_log_file": "data/sample_logs/app.log",
        "reports_dir": "ops_reports",
        "audit_dir": "ops_audit_logs",
        "scripts_dir": "generated_scripts",
    },
    "tools": {
        "default_process_limit": 5,
        "default_process_sort": "cpu",
        "default_disk_path": ".",
    },
    "memory": {
        "sqlite_db": "opspilot_memory.db",
        "vector_dir": "vector_store",
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "semantic_search_limit": 3,
    },
}


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return DEFAULT_CONFIG

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        user_config = json.load(file)

    config = {
        section: values.copy() if isinstance(values, dict) else values
        for section, values in DEFAULT_CONFIG.items()
    }

    for section, values in user_config.items():
        if section in config and isinstance(values, dict):
            config[section].update(values)
        else:
            config[section] = values

    return config