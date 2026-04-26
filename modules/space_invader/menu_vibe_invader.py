from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.console import Group
from art import text2art

def draw_menu():
    titulo = Text(text2art("VIBE  INVADERS"), style="bold green")
    
    menu = Text("\n\n[A] Jogar\n\n[Q] Sair\n\n\n", style="bold green", justify='center')
    
    controles = Align(Text("A: Esquerda  |  D: Direita  |  Backspace: Atirar", style="bold green"), vertical='bottom', align='center')

    conteudo = Group(titulo, menu, controles)

    panel = Panel(conteudo, border_style="green", height=20)

    return Align.center(panel, vertical="middle")


def draw_gameover(wave, score, highscore):
    titulo = Text(text2art("GAME OVER"), style="bold red")
    
    dados = Text(justify="center")
    dados.append("\n\n")
    dados.append(f"{'WAVE':<12}{wave}\n\n", style="bold green")
    dados.append(f"{'SCORE':<12}{score}\n\n", style="bold green")
    dados.append(f"{'HIGHSCORE':<12}{highscore}\n", style="bold green")

    conteudo = Group(titulo, dados)

    panel = Panel(
        Align.center(conteudo, vertical="middle"),
        border_style="green",
        height=20,
        expand=False
    )

    return Align.center(panel, vertical="middle")


def handle_menu_input(key):
    if key == b'a':
        return "game"
    elif key == b'q':
        return "exit"

    return "menu"