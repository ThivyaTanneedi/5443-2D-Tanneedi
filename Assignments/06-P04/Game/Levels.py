import pygame
from .GameScene import GameScene
from .Player import Player
from .Mob import Mob
from .Collectables import Coin,Health_Potion
from .Spikes import Spike,FlameThrower
from .Map import Map
from .Camera import Camera
from . import settings
import os
from .UI import Font, Mouse


class Levels(GameScene):
    def __init__(self, goto_scene):
        self._goto_scene = goto_scene
        GameScene.__init__(self)

        self.levels = [
            'level64.tmx',
           
        ]
        self.current_level = 0

        self.level_complete = False
        self._fadeout_timer = 0
        self._fadeout_time = 2

        # sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.mobs = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.spike = pygame.sprite.Group()
        self.flames = pygame.sprite.Group()
        self.potion= pygame.sprite.Group()
        
        

        self.player = Player((0, 0), groups=(self.all_sprites,))
        self.camera = Camera()

        self._total_coins = 0
        self._total_deaths = 0

        
        self.textures = {
            
            'coin': pygame.transform.scale(
                        pygame.image.load(os.path.join(settings.img_folder,"Collectables", "coin.png")).convert_alpha().subsurface(pygame.Rect(0, 0, 40, 40)),
                        (32, 32)
                    ),
            "heart": pygame.transform.scale(pygame.image.load(os.path.join(settings.img_folder, "HUD", "heart.png")).convert_alpha(), (30, 27)),

        }
        self.victory=pygame.mixer.Sound("Resources/music/Road to Dazir.ogg")
        self.victory.play(-1)
        self.load_new_level(self.current_level)

    def load_new_level(self, level_num):
        self.all_sprites.empty()
        self.coins.empty()
        self.mobs.empty()
        #self.all_sprites.add(self.player)

        self.level_complete = False
        self._fadeout_timer = 0

        self.map = Map(os.path.join(settings.levels_folder, self.levels[level_num]))
        self.map_img = self.map.make_map()
        self.player.set_pos(self.map.spawn_point)
        self.camera.set_boundaries(self.map_img.get_rect())
        self.camera.set_pos(self.map.spawn_point)

        # mob spawns
        for mob_spawn in self.map.mob_spawns:
            Mob(mob_spawn, groups=(self.all_sprites, self.mobs))

        # coins
        for coin_loc in self.map.coin_spawns:
            Coin(coin_loc[0], coin_loc[1], groups=(self.all_sprites, self.coins))
            self._total_coins+=1
        # potion
        for potion_loc in self.map.potion_spawns:
            Health_Potion(potion_loc[0], potion_loc[1], groups=(self.all_sprites, self.potion))
            
        
        for spike_loc in self.map.spikes:
            Spike(spike_loc[0], spike_loc[1], groups=(self.all_sprites, self.spike))
        
        for flamethrower_loc in self.map.flames:
            FlameThrower(flamethrower_loc[0], flamethrower_loc[1], groups=(self.all_sprites, self.flames))
            

        # make parallax layers
        

    def render_backgrounds(self, surface):
        surface.fill((37, 19, 26))
        

   
    def render_hud(self, surface):
        x = 30
        y = surface.get_rect().height - 40

        # health
        surface.blit(self.textures["heart"], (x, y))
        Font.put_text(surface, str(self.player.health), (x+35, y), (251, 251, 251))

        # coins
        surface.blit(self.textures["coin"], (x+100, y))
        Font.put_text(surface, str(self.player.coins), (x+140, y), (251, 251, 251))

    def render(self, surface):
        if Mouse.is_visible():
            Mouse.set_visible(False)

        if self.level_complete:
            surface.fill((220, 220, 220), special_flags=pygame.BLEND_MULT)
        else:
            self.render_backgrounds(surface)
            surface.blit(self.map_img, (0, 0), area=self.camera.camera_rect)
            for sprite in self.all_sprites:
                sprite.render(surface, self.camera)
            self.player.render(surface, self.camera)
            self.render_hud(surface)

            if settings.DEBUG_DRAW:
                for obs in self.map.collidables:
                    obs.render(surface, self.camera)
            # self.render_foregrounds(surface)

    def respawn_player(self):
        self.player.health = self.player._max_health
        p_pos = self.player.rect.center
        s_pos = self.map.spawn_point
        c_pos = (s_pos[0]+(p_pos[0]-s_pos[0])//3, s_pos[1]+(p_pos[1]-s_pos[1])//3)
        self.player.set_pos(self.map.spawn_point)
        self.camera.set_pos(c_pos)
        self._total_deaths += 1

    def update(self, delta_time):
        self.camera.move_to(self.player.rect.center, delta_time)

        if not self.level_complete:
            # check if reached goal
            if self.map.goal.colliderect(self.player.rect):
                print("Level", self.current_level, "Complete!")
                self.level_complete = True
                self._fadeout_timer = self._fadeout_time

            # normal game loop updates
            self.player.update(delta_time, self.map, self.mobs, self.coins,self.potion,self.spike,self.flames)
            for mob in self.mobs:
                mob.update(delta_time, self.map)
            for coin in self.coins:
                coin.update(delta_time)
            
            for potion in self.potion:
                potion.update(delta_time)
            
            for spike in self.spike:
                spike.update(delta_time)
            
            for flame in self.flames:
                flame.update(delta_time)

            if self.player.health == 0:
                self.respawn_player()

        # goal reached, fadeout animation
        elif self._fadeout_timer > 0:
            self._fadeout_timer -= delta_time

        # fadeout animation complete, load new level
        else:
            if self.current_level == len(self.levels)-1:
                print("Game completed!")
                self._goto_scene("end_menu", self.player.coins, self._total_coins, self._total_deaths)
                self.victory.stop()
            else:
                self.current_level = (self.current_level+1)
                self.load_new_level(self.current_level)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                if self.camera.boundaries is None:
                    self.camera.set_boundaries(self.map_img.get_rect())
                else:
                    self.camera.set_boundaries(None)
            elif event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                self._goto_scene("pause_menu")


