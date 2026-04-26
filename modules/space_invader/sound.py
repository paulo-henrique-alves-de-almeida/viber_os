from ..caixa_som import CaixaSom


SOUNDS_DIR = "modules/space_invader/sounds"
caixa_som = CaixaSom(musicas=SOUNDS_DIR, efeitos=SOUNDS_DIR)
caixa_som.init()

def play_music():
    caixa_som.tocar_musica('space_battle.wav')
    caixa_som.volume_musica(0.3)

def stop_music():
    caixa_som.pausar_musica()

def play_shoot():
    efeito = 'shoot.ogg'
    caixa_som.tocar_efeito(efeito)
    caixa_som.volume_efeito(efeito, 0.4)

def play_defeat():
    efeito = 'defeat.ogg'
    caixa_som.tocar_efeito(efeito)
    caixa_som.volume_efeito(efeito, 0.4)


def play_explosion():
    caixa_som.tocar_efeito('explosion.ogg')
