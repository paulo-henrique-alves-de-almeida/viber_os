# importações internas
from console import console, limpar_tela, erro, aviso
from caixa_som import caixa_som

# importação de Rich
from rich.panel import Panel
from rich import box
from rich.align import Align
from rich.text import Text
from rich.console import Group

# outras importações
from pathlib import Path
from art import text2art
import msvcrt


def mostrar_biblioteca(musicas: list, selected: int) -> None:
    console.print(Panel(Align.center(text2art('MUSICAS')), style='green', box=box.DOUBLE))
    console.print()

    lista_musicas = Text()
    for i, music in enumerate(musicas):
        numero = f"0{i + 1}" if i < 9 else str(i + 1)
        if i == selected:
            lista_musicas.append(f'\n[{numero}]  ▶  {Path(music).stem}\n', style="bold green")
        else:
            lista_musicas.append(f'\n[{numero}]     {Path(music).stem}\n', style="dim green")

    musica_atual = Text(f'\nMúsica Atual: {str(Path(caixa_som.get_musica_atual()).stem).title()}\n', justify='center', style='bold green')
    dicas = Text('↑ ↓: Navegar  |  Enter: Tocar  |  M: Mudo  |  Q: Sair', justify='center', style='dim green')

    conteudo = Group(lista_musicas, musica_atual, dicas)
    console.print(Panel(conteudo))
    console.print()


def biblioteca_musicas() -> None:
    caixa_som.init()
    musicas = sorted(caixa_som.listar_musicas())
    selected = 0

    while True:
        limpar_tela()
        mostrar_biblioteca(musicas, selected)

        key = msvcrt.getch()

        if key == b'\xe0':  # seta especial
            key2 = msvcrt.getch()
            if key2 == b'H':  # seta cima
                selected = (selected - 1) % len(musicas)
            elif key2 == b'P':  # seta baixo
                selected = (selected + 1) % len(musicas)

        elif key in (b'\r', b'\n'):  # Enter — toca a música selecionada
            caixa_som.tocar_musica(musicas[selected], 0.5)

        elif key.lower() == b'm':  # M — mudo
            caixa_som.tocar_musica('mute')

        elif key.lower() == b'q':  # Q — sair
            break


if __name__ == '__main__':
    biblioteca_musicas()
