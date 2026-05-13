import json

# importando pathlib para gerenciar pastas e caminhos de arquivos
from pathlib import Path

# SAVE_FILE é o caminho absoluto do arquivo de save
SAVE_FILE = Path(__file__).parent / "score" / "save.json"

def load_highscore() -> 0 | int:
    if not SAVE_FILE.exists():
        return 0

    with open(SAVE_FILE, "r") as f:
        data = json.load(f)
        return data.get("highscore", 0)


def save_highscore(score) -> None:
    # cria a pasta de score antes salvá-lo
    SAVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(SAVE_FILE, "w+") as f:
        json.dump({"highscore": score}, f)