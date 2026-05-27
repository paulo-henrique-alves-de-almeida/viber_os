import json

# importando pathlib para gerenciar pastas e caminhos de arquivos
from pathlib import Path

# SAVE_FILE é o caminho absoluto do arquivo de save
SAVE_FILE = Path(__file__).parent / "score" / "save.json"

def load_highscore() -> int:
    if not SAVE_FILE.exists():
        return 0
    with open(SAVE_FILE, "r") as f:
        data = json.load(f)
        return data.get("highscore", 0)


def save_highscore(score) -> None:
    SAVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = _load_data()
    data["highscore"] = score
    with open(SAVE_FILE, "w+") as f:
        json.dump(data, f)


def load_style() -> str:
    data = _load_data()
    return data.get("style", "retro")


def save_style(style: str) -> None:
    SAVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = _load_data()
    data["style"] = style
    with open(SAVE_FILE, "w+") as f:
        json.dump(data, f)


def _load_data() -> dict:
    if not SAVE_FILE.exists():
        return {}
    with open(SAVE_FILE, "r") as f:
        return json.load(f)