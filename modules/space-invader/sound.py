import pygame
import os

pygame.mixer.init()

SOUNDS_DIR = "sounds"


def _load(filename):
    path = os.path.join(SOUNDS_DIR, filename)
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    return None


_channel_music     = pygame.mixer.Channel(0)
_channel_shoot     = pygame.mixer.Channel(1)
_channel_defeat    = pygame.mixer.Channel(2)
_channel_explosion = pygame.mixer.Channel(3)

_music  = _load("space_battle.wav")
if _music:
    _music.set_volume(0.3)
_shoot     = _load("shoot.ogg")
if _shoot:
    _shoot.set_volume(0.4)
_defeat    = _load("defeat.ogg")
if _defeat:
    _defeat.set_volume(0.4)
_explosion = _load("explosion.ogg")
if _explosion:
    _explosion.set_volume(1.0)


def play_music():
    "Toca a música de fundo em loop."
    if _music and not _channel_music.get_busy():
        _channel_music.play(_music, loops=-1)


def stop_music():
    _channel_music.stop()


def play_shoot():
    if _shoot:
        _channel_shoot.play(_shoot)


def play_defeat():
    stop_music()
    if _defeat:
        _channel_defeat.play(_defeat)


def play_explosion():
    if _explosion:
        _channel_explosion.play(_explosion)
