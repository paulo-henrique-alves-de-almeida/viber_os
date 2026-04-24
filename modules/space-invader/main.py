import time
import msvcrt
from rich.console import Console
from rich.live import Live

from game import Game
from menu import draw_menu, draw_gameover, handle_menu_input
from save import load_highscore, save_highscore
import sound

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
                        sound.stop_music()
                        break

                live.update(draw_menu())

            # game
            elif state == "game":
                if key:
                    game.handle_input(key)

                game.update()

                if game.game_over:
                    if game.score > highscore:
                        save_highscore(game.score)
                        highscore = game.score

                    sound.stop_music()
                    state = "gameover"
                    gameover_timer = 0

                live.update(game.draw())

            # gameover
            elif state == "gameover":
                gameover_timer += 1
                live.update(draw_gameover(game.wave, game.score, highscore))

                if gameover_timer >= 72 or key:
                    sound.play_music()
                    state = "menu"

            time.sleep(0.05)


if __name__ == "__main__":
    main()
