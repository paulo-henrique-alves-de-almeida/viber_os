import time
import msvcrt
from rich.live import Live

from modules.console import console
from modules.space_invader.game import Game
from modules.space_invader.menu_vibe_invader import draw_menu, draw_gameover, draw_victory, handle_menu_input
from modules.space_invader.save import load_highscore, save_highscore, load_style, save_style
from modules.space_invader.config import apply_style
from modules.space_invader import sound


def main() -> None:
    state = "menu"
    game = None
    highscore = load_highscore()
    style = load_style()
    apply_style(style)

    with Live(console=console, refresh_per_second=24) as live:
        while True:

            # input
            key = None
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\xe0':  # tecla especial (setas)
                    key = msvcrt.getch()
                else:
                    key = key.lower()

            # menu
            if state == "menu":
                if key:
                    result, new_style = handle_menu_input(key, style)
                    if new_style != style:
                        style = new_style
                        apply_style(style)
                        save_style(style)
                    if result == "game":
                        game = Game(highscore)
                        state = "game"
                    elif result == "exit":
                        sound.stop_music()
                        break

                live.update(draw_menu(style))

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

                if game.victory:
                    if game.score > highscore:
                        save_highscore(game.score)
                        highscore = game.score

                    sound.stop_music()
                    state = "victory"
                    victory_timer = 0

                live.update(game.draw())

            # victory
            elif state == "victory":
                victory_timer += 1
                live.update(draw_victory(game.score, highscore))

                if victory_timer >= 96 or key:
                    sound.play_music()
                    state = "menu"

            # gameover
            elif state == "gameover":
                gameover_timer += 1
                live.update(draw_gameover(game.wave, game.score, highscore))

                if gameover_timer >= 72 or key:
                    sound.play_music()
                    state = "menu"

            time.sleep(0.05)

