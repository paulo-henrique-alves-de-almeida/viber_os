from pathlib import Path
from pygame import mixer

musica_atual = 'VibeOS.mp3'
class CaixaSom:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.musicas = Path(__file__).parent.parent / 'medias/sons/musicas'
        self.efeitos = Path(__file__).parent.parent / 'medias/sons/efeitos'
    
    def init(self):
        if not mixer.get_init():
            mixer.init()
    
    def get_musica_atual(self):
        return musica_atual

    def tocar_efeito(self, nome_efeito: str, volume: float = 1):
        efeito = mixer.Sound(Path(self.efeitos / nome_efeito))
        efeito.play()
        efeito.set_volume(volume)

    def tocar_musica(self, nome_musica: str, volume: float = 1, salvar_musica_atual: bool = True, loop: int = -1, fadeout: float = 0):
        global musica_atual
        if salvar_musica_atual:
            musica_atual = nome_musica

        mixer.music.load(Path(self.musicas / nome_musica))
        mixer.music.play(loop)
        mixer.music.set_volume(volume)

        if fadeout:
            mixer.music.fadeout(fadeout)

    def pausar_musica(self):
        mixer.music.stop()
    
    def get_busy_music(self) -> bool:
        return mixer.music.get_busy()
    
    def listar_musicas(self) -> list[Path]:
        musicas_sistema = ['playstation-2-startup-intro-ps2.mp3']

        musicas = [
            m for m in self.musicas.glob('*.mp3')
            if m.name not in musicas_sistema
        ]

        return musicas

if __name__ == '__main__':
    caixa_som = CaixaSom()
    caixa_som.init()
    caixa_som.tocar_efeito('error.ogg.mp3')


caixa_som = CaixaSom()
