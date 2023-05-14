from .GameScene import GameScene
from . import settings
import pygame
import os
from .UI import Mouse, Button, Font, CheckBox
import random





class EndMenu(GameScene):
    class Confetti:
        def __init__(self, color):
            self.color = color
            self.speed = random.randint(200, 500)
            self.size = random.randint(2, 6)
            self.pos = [random.randrange(5, settings.SCREEN_WIDTH-5), 0]
            self._t = 0
            self._dx = 0

        def render(self, surface):
            pygame.draw.rect(surface, self.color, (self.pos, (self.size, self.size)))

        def update(self, delta_time):
            self.pos[1] += self.speed * delta_time
            if self.pos[1] >= settings.SCREEN_HEIGHT:
                self.pos[1] = 0
                self.pos[0] = random.randrange(5, settings.SCREEN_WIDTH-5)

            self._t += delta_time
            if self._t > 0.5:
                self._t = 0
                self._dx = [-50, 50][random.randint(0, 1)]
            self.pos[0] += self._dx*delta_time

    def __init__(self, goto_scene, coins_collected, total_coins, total_deaths):
        self._goto_scene = goto_scene
        GameScene.__init__(self)
        Mouse.set_visible(True)
        #self.victory_sound = pygame.mixer.Sound(os.path.join(settings.music_folder, 'victory.wav'))
        #self.victory_sound.set_volume(0.5)
        sounds=["Aquarium","Aviary","Elephant","Finale","Swan"]
        self.sounds=[]
        for sound in sounds:
            self.sounds.append(pygame.mixer.Sound(os.path.join(settings.music_folder,"victory.wav")))
        
        self._colors = [(250, 20, 20), (20, 250, 20), (250, 20, 250),
                        (250, 250, 20), (20, 250, 250), ]
        self._color_i = 0
        self._elapsed_time = 0
        self._confettis = [self.Confetti(self._colors[random.randrange(0, len(self._colors))]) for i in range(30)]

        w, h = 150, 50

        self._heading_text_surface = Font.get_render("Congratulations!!", size="big")
        self._heading_text_rect = self._heading_text_surface.get_rect()
        self._heading_text_x = (settings.SCREEN_WIDTH - self._heading_text_rect.width) // 2
        self._heading_text_y = self._heading_text_rect.height // 2

        self._text_surface = Font.get_render("You have completed your journey!", size="normal")
        self._text_rect = self._text_surface.get_rect()
        self._text_x = (settings.SCREEN_WIDTH - self._text_rect.width) // 2
        self._text_y = self._heading_text_y + self._heading_text_rect.height*2

        self._stat_text_surface = Font.get_render("Coins Collected:  %d/%d"%(coins_collected, total_coins*10), size="normal")
        self._stat_text_rect = self._stat_text_surface.get_rect()
        self._stat_text_x = (settings.SCREEN_WIDTH - self._stat_text_rect.width) // 2
        self._stat_text_y = self._text_y + self._text_rect.height * 3 // 2

        

        button_y = self._stat_text_y + self._stat_text_rect.height
       
        self.exit_bttn = Button(((settings.SCREEN_WIDTH - w) // 2, button_y + 125), (w, h), "Quit",
                                lambda: self.quit(goto_scene))
        pygame.mixer.music.set_volume(0)
        self.victory_sound=random.choice(self.sounds)
        self.victory_sound.play(-1)
    def goto_start(self,goto_scene):
        pygame.mixer.music.set_volume(3)
        for sound in self.sounds:
            sound.stop()
        goto_scene("start_menu")
    
    def quit(self, goto_scene):
        for sound in self.sounds:
            sound.stop()
        goto_scene("quit")
        
    def render(self, surface):
        surface.fill((35, 25, 40))
        # surface.blit(self._heading_text_surface, (self._heading_text_x, self._heading_text_y))
        surface.blit(Font.get_render("Congratulations!!", color=self._colors[self._color_i], size="big"), (self._heading_text_x, self._heading_text_y))
        surface.blit(self._text_surface, (self._text_x, self._text_y))
        surface.blit(self._stat_text_surface, (self._stat_text_x, self._stat_text_y))
        self.exit_bttn.render(surface)

        for confetti in self._confettis:
            confetti.render(surface)

    def update(self, delta_time):
        self._elapsed_time += delta_time
        if self._elapsed_time >= 0.25:
            self._elapsed_time = 0
            self._color_i = (self._color_i + 1)%len(self._colors)

        for confetti in self._confettis:
            confetti.update(delta_time)

    def handle_events(self, event):
        self.exit_bttn.handle_events(event)

        if event.type == pygame.KEYDOWN and (event.key == pygame.K_p or event.key == pygame.K_ESCAPE):
            self._goto_scene("start_menu")
