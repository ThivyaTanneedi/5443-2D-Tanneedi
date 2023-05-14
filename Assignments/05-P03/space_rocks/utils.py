import random

from pygame import Color
from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound


def load_sprite(name, with_alpha=True):
    path = f"../assets/sprites/{name}.png"
    loaded_sprite = load(path)

    return loaded_sprite.convert_alpha() if with_alpha else loaded_sprite.convert()


def load_sound(name):
    path = f"../assets/sounds/{name}.wav"
    return Sound(path)


def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )


def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)


def print_text(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, False, color)

    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2

    surface.blit(text_surface, rect)


############################
def mykwargs(argv):
    args = []
    kargs = {}

    for arg in argv:
        if "=" in arg:
            key, val = arg.split("=")
            kargs[key] = val
        else:
            args.append(arg)
    return args, kargs