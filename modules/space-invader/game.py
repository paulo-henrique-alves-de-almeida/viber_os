import random
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from config import WIDTH, HEIGHT, PLAYER_CHAR, ENEMY_CHAR, BULLET_CHAR
import sound


def _formation_linha() -> list:
    return [[x, 2] for x in range(5, WIDTH - 5, 4)]


def _formation_v() -> list:
    center = WIDTH // 2
    xs = [center - 8, center - 4, center, center + 4, center + 8]
    return [[x, 2 + abs(x - center) // 2] for x in xs]


def _formation_disperso() -> list:
    xs = random.sample(range(3, WIDTH - 3), 6)
    return [[x, random.randint(1, 4)] for x in xs]


def _formation_duas_fileiras() -> list:
    fileira1 = [[x, 2] for x in range(5, WIDTH - 6, 7)]
    fileira2 = [[x, 5] for x in range(7, WIDTH - 6, 7)]
    return fileira1 + fileira2


_FORMATIONS = [
    _formation_linha,
    _formation_v,
    _formation_disperso,
    _formation_duas_fileiras,
]


def _make_wave(wave_number: int) -> list:
    formation = random.choice(_FORMATIONS)
    return formation()


class Game:
    def __init__(self, highscore):
        self.player_pos = WIDTH // 2
        self.bullet = None
        self.game_over = False
        self.score = 0
        self.highscore = highscore

        #w
        self.wave = 1
        self.enemies = _make_wave(self.wave)
        self.enemy_speed = 0.05
        self._speed_increment = 0.01
        self._wave_cleared = False

        #ex
        self.explosions = []  # cada item: [x, y, frames_restantes]

        sound.play_music()


    def _current_speed(self) -> float:
        return self.enemy_speed + self._speed_increment * (self.wave - 1)

   
    def update(self):
        
        if self.bullet:
            self.bullet[1] -= 1
            if self.bullet[1] < 0:
                self.bullet = None

        # sys col1
        if self.bullet:
            for enemy in self.enemies:
                if (enemy[0] == self.bullet[0]
                        and abs(enemy[1] - self.bullet[1]) <= 1.0):
                    self.explosions.append([enemy[0], int(enemy[1]), 4])
                    self.enemies.remove(enemy)
                    self.bullet = None
                    self.score += 10
                    sound.play_explosion()
                    break

        #ex
        for exp in self.explosions:
            exp[2] -= 1
        self.explosions = [e for e in self.explosions if e[2] > 0]

        #mov em
        speed = self._current_speed()
        for enemy in self.enemies:
            enemy[1] += speed
            if int(enemy[1]) >= HEIGHT - 1:
                self.game_over = True

        # def
        if self.game_over:
            sound.play_defeat()
            return

        # res w
        if not self.enemies and not self._wave_cleared:
            self._wave_cleared = True
            self.wave += 1
            self.score += self.wave * 50
            self.enemies = _make_wave(self.wave)
            self._wave_cleared = False


    def handle_input(self, key):
        if key == b'a' and self.player_pos > 0:
            self.player_pos -= 1
        elif key == b'd' and self.player_pos < WIDTH - 1:
            self.player_pos += 1
        elif key == b' ' and self.bullet is None:
            self.bullet = [self.player_pos, HEIGHT - 2]
            sound.play_shoot()

   
    def draw(self):
        screen = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

        screen[HEIGHT - 1][self.player_pos] = PLAYER_CHAR

        if self.bullet:
            screen[int(self.bullet[1])][self.bullet[0]] = BULLET_CHAR

        for ex, ey in self.enemies:
            screen[int(ey)][ex] = ENEMY_CHAR

        for ex, ey, _ in self.explosions:
            if 0 <= ey < HEIGHT and 0 <= ex < WIDTH:
                screen[ey][ex] = "*"

        text = Text()
        for row in screen:
            text.append("".join(row) + "\n")

        panel = Panel(
            text,
            border_style="green",
            width=WIDTH + 4,
            height=HEIGHT + 4,
            expand=False,
            title=(
                f"[green]WAVE: {self.wave} | "
                f"SCORE: {self.score} | "
                f"HIGH: {self.highscore}[/green]"
            )
        )

        return Align.center(panel, vertical="middle")
