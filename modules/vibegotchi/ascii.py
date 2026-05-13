from json import load
from pathlib import Path

SAVE_PATH = Path(__file__).parent / 'dados' / 'vibes.json'

def pegar_vibe(pet) -> str:
    with open(SAVE_PATH, "r", encoding="utf-8") as sprite:
        vibes = load(sprite)

    if pet.aura <= 0:
        return vibes['sem_aura']
    
    if pet.energia < 20:
        return vibes['cansado']
    
    if pet.humor > 70:
        return vibes['feliz']
    
    if pet.humor < 30:
        return vibes['triste']
    
    return vibes['normal']
