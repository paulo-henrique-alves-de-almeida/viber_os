from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.console import Group
from art import text2art

def draw_menu(style: str = "retro") -> Align:
    titulo = Text(text2art("VIBE  INVADERS"), style="green")
    versao = Text("v1.1\n", style="dim green", justify="center")

    menu = Text(justify='center')
    menu.append("\n[A] Jogar\n\n", style="bold green")

    # estilo — ativo em verde, inativo em cinza
    menu.append("[S] Estilo:  ", style="bold green")
    menu.append("RETRO (Easy)", style="bold green" if style == "retro" else "dim white")
    menu.append("  /  ", style="bold green")
    menu.append("VIBE (Hard)",  style="bold green" if style == "vibe"  else "dim white")
    menu.append("\n\n", style="bold green")
    menu.append("[Q] Sair\n\n\n", style="bold green")

    ctrl_text = Text(justify="center")
    ctrl_text.append("A: Esquerda (←)  |  D: Direita (→)  |  Space: Atirar\n", style="bold green")
    ctrl_text.append("← → apenas Windows", style="dim green")
    controles = Align(ctrl_text, vertical='bottom', align='center')

    conteudo = Group(titulo, versao, menu, controles)
    panel = Panel(conteudo, border_style="green", height=20)
    return Align.center(panel, vertical="middle")


def draw_gameover(wave, score, highscore) -> Align:
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


def draw_victory(score, highscore) -> Align:
    titulo = Text(text2art("YOU  WIN"), style="bold yellow")

    dados = Text(justify="center")
    dados.append("\n\n")
    dados.append("BOSS DERROTADO!\n\n", style="bold yellow")
    dados.append(f"{'SCORE':<12}{score}\n\n", style="bold green")
    dados.append(f"{'HIGHSCORE':<12}{highscore}\n", style="bold green")

    conteudo = Group(titulo, dados)

    panel = Panel(
        Align.center(conteudo, vertical="middle"),
        border_style="yellow",
        height=20,
        expand=False
    )

    return Align.center(panel, vertical="middle")


def handle_menu_input(key, style: str = "retro"):
    if key == b'a':
        return "game", style
    elif key == b's':
        new_style = "vibe" if style == "retro" else "retro"
        return "menu", new_style
    elif key == b'q':
        return "exit", style

    return "menu", style