from pathlib import Path
from pygame import mixer

class CaixaSom:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CaixaSom, cls).__new__(cls)
        
        return cls._instance
    
    def __init__(self):
        self.musicas = Path(__file__).parent.parent / 'sons' / 'musicas'
        self.efeitos = Path(__file__).parent.parent / 'sons' / 'efeitos'

        self.musica_atual = None
    
    def init(self):
        if not mixer.get_init():
            mixer.init()
    
    def tocar_efeito(self, nome_efeito: str):
        efeito = mixer.Sound(Path(self.efeitos / nome_efeito))
        efeito.play()

    def tocar_musica(self, nome_musica: str, loop: int = -1, fadeout: int = 0):
        self.musica_atual = str(Path(nome_musica).stem)
        mixer.music.load(Path(self.musicas / nome_musica))
        mixer.music.play(loop)
        mixer.music.fadeout(fadeout)

    def pausar_musica(self):
        mixer.music.stop()

if __name__ == '__main__':
    caixa_som = CaixaSom()
    caixa_som.init()
    caixa_som.tocar_efeito('error.ogg.mp3')
