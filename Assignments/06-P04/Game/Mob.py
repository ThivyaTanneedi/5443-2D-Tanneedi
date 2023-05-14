from .Physics import RigidBody
from .Animation import Animation
from .settings import *
from . import settings
import pygame
import random
import os
from .UI import Font


class Mob(RigidBody, pygame.sprite.Sprite):
    class State:
        
        walking = 1
        

    textures = None
    death_sound = None

    @staticmethod
    def _load_textures():

        if Mob.textures is None:
            print("loading mob textures")
            Mob.textures = {
                
                'enemy-walk': pygame.image.load(
                    os.path.join(settings.img_folder, "Enemy",
                                 "skeleton.png")).convert_alpha(),
                
            }

       

    def __init__(self, spawn_point, groups):
        self._load_textures()
        self.state = self.State.walking
        self.animation = Animation()
        self.animation.add(self.State.walking, Mob.textures['enemy-walk'], 1, 1, 'left', offset=(-4, -5))

        self._layer = 1
        RigidBody.__init__(self, *spawn_point, 64, 64)
        
        self.pushable = False
        pygame.sprite.Sprite.__init__(self, groups)

        
        self.walk_speed = (PLAYER_WALK_SPEED * 2 / 3)*(random.randint(10,20)/10)
        
        
        
        
        self.v_x = self.walk_speed*random.choice([-1,1])

        self.facing = self.animation.sprites[self.state].default_facing
        if self.walk_speed<0:
            print(self.walk_speed)
            self.facing="left"
        

    def _ground_check(self, pt, collidables):
        for obs in collidables:
            if obs.rect.collidepoint(pt):
                return True
        return False

    def _ai(self, colliding):
        x = (self.rect.left - 8) if self.facing == 'left' else (self.rect.right + 8)
        self._ground_checker = (int(x), int(self.rect.bottom + 8))
        if self.state == self.State.walking:
            if self.facing == 'left' and (colliding['left'] ):
                self.v_x = self.walk_speed
            elif self.facing == 'right' and (colliding['right'] ):
                self.v_x = -self.walk_speed
            
                

        
                

  

    def do_physics(self, delta_time, collidables):
        colliding = RigidBody.do_physics(self, delta_time, collidables)
        

        return colliding

    def _change_states(self):
        
            
        self.state = self.State.walking
            

        if self.v_x < 0 and self.facing != 'left':
            self.facing = 'left'
        if self.v_x > 0 and self.facing != 'right':
            self.facing = 'right'

    

    def update(self, delta_time, map):
       
        colliding = self.do_physics(delta_time, map.collidables)
        self._ai(colliding)
        self._change_states()
            
       
        self.animation.play(self.state, delta_time)

    

    def render(self, surface, camera):
        self.animation.render(surface, camera.get_relative_rect(self.rect), self.facing)
        RigidBody.render(self, surface, camera)

        # if settings.DEBUG_DRAW:
        #     if self._ground_checker is not None:
        #         pygame.draw.circle(surface, (255, 255, 0), camera.get_relative_pos(*self._ground_checker), 3)

        #     Font.put_text(surface, [ 'walk'][self.state],
        #                   camera.get_relative_pos(self.rect.left, self.rect.top-32), (0, 255, 255))

