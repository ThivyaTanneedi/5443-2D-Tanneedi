import os
import pygame
from .Physics import Collidable
from .Animation import AnimatedSprite
from . import settings


class Spike(pygame.sprite.Sprite):

    texture = None
    pickup_sound = None

    @staticmethod
    def _load_resources():

        if Spike.texture is None:
            Spike.texture = pygame.image.load(os.path.join(settings.img_folder,"spike", "spike.png")).convert_alpha()

        

    def __init__(self, x, y, groups):
        self._layer = 3
        self.delay_duration=1
        self.delay=self.delay_duration
        
        self.rect = pygame.Rect(x, y, 50, 50)
        
        pygame.sprite.Sprite.__init__(self, groups)
        self._load_resources()
        self.animated_sprite = AnimatedSprite(15, loop=True)
        self.animated_sprite.load_from_spritesheet(Spike.texture, (64, 64), 6)
        self.prev=0
    def can_hurt(self):
        return self.animated_sprite.current_frame!=0
        
    def update(self, delta_time):
        if self.animated_sprite.current_frame==0 and self.delay>0:
            self.delay-=delta_time
        else:    
            self.animated_sprite.next_frame(delta_time)
            if self.animated_sprite.current_frame!=self.prev:
                self.delay=self.delay_duration

   

    def render(self, surface, camera):
        self.animated_sprite.render(surface, camera.get_relative_pos(self.rect.x-7, self.rect.y-7))
        if settings.DEBUG_DRAW:
            pygame.draw.rect(surface, settings.DEBUG_DRAW_COLOR,
                             pygame.Rect(camera.get_relative_pos(self.rect.x, self.rect.y),
                                         (self.rect.width, self.rect.height)), 1)

class FlameThrower(pygame.sprite.Sprite):

    texture = None
    pickup_sound = None

    @staticmethod
    def _load_resources():

        if FlameThrower.texture is None:
            FlameThrower.texture = pygame.image.load(os.path.join(settings.img_folder,"FlameThrower", "flamethrower.png")).convert_alpha()

        

    def __init__(self, x, y, groups):
        self._layer = 3
        self.delay_duration=1
        self.delay=self.delay_duration
        
        self.rect = pygame.Rect(x, y, 64, 128)
        pygame.sprite.Sprite.__init__(self, groups)
        self._load_resources()
        self.animated_sprite = AnimatedSprite(8, loop=True)
        self.animated_sprite.load_from_spritesheet(FlameThrower.texture, (64, 128), 4)
        self.prev=0
    def can_hurt(self):
        return self.animated_sprite.current_frame!=0
        
    def update(self, delta_time):
        if self.animated_sprite.current_frame==0 and self.delay>0:
            self.delay-=delta_time
        else:    
            self.animated_sprite.next_frame(delta_time)
            if self.animated_sprite.current_frame!=self.prev:
                self.delay=self.delay_duration

   

    def render(self, surface, camera):
        self.animated_sprite.render(surface, camera.get_relative_pos(self.rect.x, self.rect.y))
        if settings.DEBUG_DRAW:
            pygame.draw.rect(surface, settings.DEBUG_DRAW_COLOR,
                             pygame.Rect(camera.get_relative_pos(self.rect.x, self.rect.y),
                                         (self.rect.width, self.rect.height)), 1)

