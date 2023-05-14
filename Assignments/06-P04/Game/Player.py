import pygame
import os
from .Physics import RigidBody
from .Animation import Animation, AnimatedSprite
from .UI import Font
from . import settings
from .Multiplayer.multiplayer import Multiplayer
from .Multiplayer.simple_comms import Simple_Comms
from copy import deepcopy
from random import randint

class Player(RigidBody, pygame.sprite.Sprite):
    class State:
        idle = 0
        walking = 1
        running = 2
        

    textures = None
    sounds = None
    player_type=randint(1,4)

    @staticmethod
    def _load_resources():
        player_folder = os.path.join(settings.img_folder, 'Player',f"Player{Player.player_type}")
        if Player.textures is None:
            print("loading player textures")
            Player.textures = {
                'player-idle': pygame.image.load(os.path.join(player_folder, 'idle.png')).convert_alpha(),
                'player-run': pygame.image.load(os.path.join(player_folder, 'walk.png')).convert_alpha(),
                
            }
        if Player.sounds is None:
            Player.sounds = {
                
                'hurt': pygame.mixer.Sound(os.path.join(settings.music_folder, 'Sound_1.wav')),
            }
            
            Player.sounds['hurt'].set_volume(0.3)

    def __init__(self, spawn_point, groups):
        self._load_resources()

        self.state = self.State.idle
        self.animation = Animation()
        self.animation.add(self.State.idle, Player.textures['player-idle'], 2, 2, 'right', offset=(-4, -10))
        self.animation.add(self.State.walking, Player.textures['player-run'], 2, 4, 'right', offset=(-4, -10))
        
        if settings.MULTIPLAYER:
            self.comms = Simple_Comms()
            self.multiplayer=Multiplayer()

        self._layer = 2
        RigidBody.__init__(self, *spawn_point, 45, 50)

        self.pushable = False
        pygame.sprite.Sprite.__init__(self, groups)

        
        self.walk_speed = settings.PLAYER_WALK_SPEED
        self.climb_speed = settings.PLAYER_WALK_SPEED*2//3
        self.facing = self.animation.sprites[self.state].default_facing

        self.coins = 0
        self._max_health = 5
        self.health = self._max_health
        self._invincible_timer = 0
        self._invincible_time = 1

        self.ledge_grabbing = False
        self._ledge_grab_checker = None  # will be made later
        self._ledge_ground_checker = None  # will be made later

        self.climbing = False

        self.message={}
        
        
    def set_pos(self, pos):
        self.rect.topleft = pos

    def _get_input(self):
        self.v_x = 0
        
        self.v_y = 0
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.v_y += -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.v_y += 1

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) :
            self.v_x += -1
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) :
            self.v_x += 1

        if self.v_x < 0 and self.facing != 'left':
            self.facing = 'left'
        if self.v_x > 0 and self.facing != 'right':
            self.facing = 'right'
        if self.v_x!=0 and self.v_y!=0:
            self.v_x *= self.walk_speed*0.7
            self.v_y *= self.walk_speed*0.7
        else:
            self.v_x *= self.walk_speed
            self.v_y *= self.walk_speed

   

    def do_physics(self, delta_time, map):
        colliding = RigidBody.do_physics(self, delta_time, map.collidables, no_gravity=(self.ledge_grabbing or self.climbing))
        

        return colliding

   

    def _obstacle_check(self, pt, collidables):
        for obs in collidables:
            if obs.rect.collidepoint(pt):
                return True
        return False

    def _change_states(self):
        

        if abs(self.v_x) > 0 or abs(self.v_y) > 0 and self.state != self.State.walking:
            self.state = self.State.walking
        elif abs(self.v_x) == 0 and abs(self.v_y) == 0 and self.state != self.State.idle:
            self.state = self.State.idle
        

    def _mob_collision(self, mob_group):
        mobs = pygame.sprite.spritecollide(self, mob_group, False)
        for mob in mobs:
            if self._invincible_timer == 0:
                self.hurt()

    def hurt(self, health_points=1):
        if self._invincible_timer == 0:
            self.health -= health_points
            self.sounds["hurt"].play()
            print("Player health reduced to", self.health)
            self._invincible_timer = self._invincible_time

    def _coin_collision(self, coin_group):
        coins = pygame.sprite.spritecollide(self, coin_group, False)
        for coin in coins:
            coin.pickup()
            self.coins += 10
    
    def _potion_collision(self, potion_group):
        potions = pygame.sprite.spritecollide(self, potion_group, False)
        for potion in potions:
            potion.pickup()
            self.health += 1

    def _spikes_collision(self, spikes_group):
        spikes = pygame.sprite.spritecollide(self, spikes_group, False)
        for spike in spikes:
            if spike.can_hurt():
                self.hurt()
    
    def _flame_collision(self, flame_group):
        flames = pygame.sprite.spritecollide(self, flame_group, False)
        for flame in flames:
            if flame.can_hurt():
                self.hurt()

    def update_message(self):
        
        self.message['space coord'] = deepcopy(self.rect.topleft)
        self.message['img'] = self.player_type
        self.message['health'] = self.health
        
        
    def update(self, delta_time, map, mob_group, coin_group,potion_group,spike_group,flame_group):
        if self._invincible_timer > 0:
            self._invincible_timer -= delta_time
            if self._invincible_timer < 0:
                self._invincible_timer = 0
        self._mob_collision(mob_group)
        self._coin_collision(coin_group)
        self._potion_collision(potion_group)
        self._spikes_collision(spike_group)
        self._flame_collision(flame_group)

        self._get_input()
        self.do_physics(delta_time, map)
        self._change_states()
        self.animation.play(self.state, delta_time)
        
            #print(self.comms.message)
            #print(self.comms.message)
            #print(len(self.multiplayer.players))

    def render(self, surface, camera):
        self.animation.render(surface, camera.get_relative_rect(self.rect), self.facing, self._invincible_timer)
        if settings.MULTIPLAYER:
            
            self.multiplayer.display_friends(self.comms.message, self,surface, camera)
            self.multiplayer.update(self.comms.message, self)
            self.update_message()
            self.comms.send(self.message)
        RigidBody.render(self, surface, camera)
        
        if settings.DEBUG_DRAW:
            Font.put_text(surface, ['idle', 'walk'][self.state],
                          camera.get_relative_pos(self.rect.left, self.rect.top - 32), (0, 255, 255))

            if self._ledge_grab_checker is not None and self._ledge_ground_checker is not None:
                pygame.draw.circle(surface, (255, 255, 0), camera.get_relative_pos(*self._ledge_grab_checker), 3)
                pygame.draw.circle(surface, (0, 255, 255), camera.get_relative_pos(*self._ledge_ground_checker), 3)


