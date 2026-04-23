import time
import msvcrt
from rich.console import Console
from rich.live import Live

from game import Game
from menu import draw_menu, handle_menu_input
from save import load_highscore, save_highscore

console = Console()


def main():
    state = "menu"
    game = None
    highscore = load_highscore()

    with Live(console=console, refresh_per_second=24) as live:
        while True:

            # input
            key = None
            if msvcrt.kbhit():
                key = msvcrt.getch().lower()

            # menu
            if state == "menu":
                if key:
                    result = handle_menu_input(key)
                    if result == "game":
                        game = Game(highscore)
                        state = "game"
                    elif result == "exit":
                        break

                live.update(draw_menu())

            #game
            elif state == "game":
                if key:
                    game.handle_input(key)

                game.update()

                if game.game_over:
                    if game.score > highscore:
                        save_highscore(game.score)
                        highscore = game.score

                    state = "menu"

                live.update(game.draw())

            time.sleep(0.05)


if __name__ == "__main__":
    main()