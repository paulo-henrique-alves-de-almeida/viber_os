from rich.panel import Panel
from rich.align import Align
from rich.text import Text


def draw_menu():
    text = Text()
    text.append("VIBE INVADERS\n", style="bold green")
    text.append("\n[A] Jogar\n", style="bold green")
    text.append("[Q] Sair\n", style="bold green")

    panel = Panel(
        text,
        border_style="green",
        width=40,
        height=12,
        expand=False
    )

    return Align.center(panel, vertical="middle")


def draw_gameover(wave, score, highscore):
    text = Text(justify="center")
    text.append("GAME OVER\n", style="bold red")
    text.append("\n")
    text.append(f"{'WAVE':<12}{wave}\n", style="bold green")
    text.append(f"{'SCORE':<12}{score}\n", style="bold green")
    text.append(f"{'HIGHSCORE':<12}{highscore}\n", style="bold green")

    panel = Panel(
        Align.center(text, vertical="middle"),
        border_style="green",
        width=40,
        height=12,
        expand=False
    )

    return Align.center(panel, vertical="middle")


def handle_menu_input(key):
    if key == b'a':
        return "game"
    elif key == b'q':
        return "exit"

    return "menu"