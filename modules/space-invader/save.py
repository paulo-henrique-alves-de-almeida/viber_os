import json
import os

SAVE_FILE = "save.json"


def load_highscore():
    if not os.path.exists(SAVE_FILE):
        return 0

    with open(SAVE_FILE, "r") as f:
        data = json.load(f)
        return data.get("highscore", 0)


def save_highscore(score):
    with open(SAVE_FILE, "w") as f:
        json.dump({"highscore": score}, f)