from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from config import WIDTH, HEIGHT, PLAYER_CHAR, ENEMY_CHAR, BULLET_CHAR


class Game:
    def __init__(self, highscore):
        self.player_pos = WIDTH // 2
        self.bullet = None
        self.enemies = [[x, 2] for x in range(5, WIDTH - 5, 4)]
        self.game_over = False
        self.score = 0
        self.highscore = highscore

    def update(self):
        # bullet
        if self.bullet:
            self.bullet[1] -= 1
            if self.bullet[1] < 0:
                self.bullet = None

        # Colisão
        if self.bullet:
            for enemy in self.enemies:
                if enemy[0] == self.bullet[0] and int(enemy[1]) == int(self.bullet[1]):
                    self.enemies.remove(enemy)
                    self.bullet = None
                    self.score += 10
                    break

        # Enemies
        for enemy in self.enemies:
            enemy[1] += 0.05
            if int(enemy[1]) >= HEIGHT - 1:
                self.game_over = True

    def handle_input(self, key):
        if key == b'a' and self.player_pos > 0:
            self.player_pos -= 1
        elif key == b'd' and self.player_pos < WIDTH - 1:
            self.player_pos += 1
        elif key == b' ' and self.bullet is None:
            self.bullet = [self.player_pos, HEIGHT - 2]

    def draw(self):
        screen = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

        screen[HEIGHT - 1][self.player_pos] = PLAYER_CHAR

        if self.bullet:
            screen[int(self.bullet[1])][self.bullet[0]] = BULLET_CHAR

        for ex, ey in self.enemies:
            screen[int(ey)][ex] = ENEMY_CHAR

        text = Text()
        for row in screen:
            text.append("".join(row) + "\n")

        panel = Panel(
            text,
            border_style="green",
            width=WIDTH + 4,
            height=HEIGHT + 4,
            expand=False,
            title=f"[green]SCORE: {self.score} | HIGH: {self.highscore}[/green]"
        )

        return Align.center(panel, vertical="middle")