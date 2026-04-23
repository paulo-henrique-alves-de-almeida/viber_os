from rich.panel import Panel
from rich.align import Align
from rich.text import Text


def draw_menu():
    text = Text()
    text.append("SPACE INVADERS\n", style="bold green")
    text.append("\n[A] Jogar\n")
    text.append("[Q] Sair\n")

    panel = Panel(
        text,
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