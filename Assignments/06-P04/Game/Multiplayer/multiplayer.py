import pygame as py
import random
import os


class Multiplayer:

    def __init__(self):

        self.players = {}

        self.player_imgs = self.load_player_imgs()
        # self.bullet_imgs = self.load_bullet_imgs()
        # self.bullet_sound = self.load_bullet_sound()


    def update(self, messages, ship):
        
        # goes through the messages from different enemy players
        for player, message in messages.items():

            # if the message is from a player not already in the player list add them
            if player not in self.players:
                self.players[player] = Friend_Player(
                    player,
                    self.player_imgs[message['img']-1],
                    
                    
                    message['space coord']
                )

            # for all players, update there stuff (coords, health, bullets)
            self.update_player(self.players[player], message)

            # check if current ship killed an enemy players
            
    
    def update_player(self, player, message):

        player.space_coord = message['space coord']
        player.health = message['health']
        
        player.rect.x, player.rect.y = player.space_coord[0], player.space_coord[1]

        

        




    def display_friends(self, messages, ship,surface,camera):
        
        for sender in messages.values():

            # get ship's screen locations and display the ship
            ship_screen_coords = self.screen_location_update(sender['space coord'], ship)

            # only draw if the ship is on the screen
            #py.draw.rect(surface,"red",(camera.get_relative_pos(sender['space coord'][0],sender['space coord'][1]),(50,100)))
            print(ship_screen_coords)
            surface.blit(self.player_imgs[sender['img']-1],camera.get_relative_pos(sender['space coord'][0],sender['space coord'][1]))
                #self.draw_ship(ship_screen_coords, sender['img'], sender['angle'], sender['health'], ship)

                # an enemy ship has just shot so play the sound
              




    #   Description:
    #       Updates the location of the GameObject based on the space_location
    def screen_location_update(self, space_coordinates, ship):
        x = space_coordinates[0] - ship.rect.x
        y = space_coordinates[1] - ship.rect.y
        return (x, y)
        

    #----------------------------------------------------------------------------
    #   Description:
    #       Draws the ship rotated
    #
    def draw_ship(self, screen_coordinates, img, angle, health, ship):

        rot_img = py.transform.rotate(self.ship_imgs[img], angle)
        x, y = screen_coordinates
        ship.screen.blit(rot_img, (x - rot_img.get_width()//2, y - rot_img.get_width()//2))

        bar_width = health/2
        if health > 60:                 # display green
            color = (0, 255, 0)
        elif health > 30:               # display yellow
            color = (255, 255, 0)
        else:                           # display red
            color = (255, 0, 0)

        py.draw.rect(ship.screen, color, py.Rect(x -(bar_width/2), y+32, bar_width, 10))


    #----------------------------------------------------------------------------
    #   Description:
    #       Draws the bullet rotated
    #
    def draw_bullet(self, screen_coordinates, img, angle, bullet):

        rot_img = py.transform.rotate(self.bullet_imgs[img], angle)
        x, y = screen_coordinates
        bullet.screen.blit(rot_img, (x - rot_img.get_width()//2, y - rot_img.get_width()//2))


    def add_ships(self, messages):

        for sender in messages:
            if sender not in self.players:
                pass
                


    #############################################################
    #   Description:
    #
    #       loads the ship images 
    #
    def load_player_imgs(self):

       
        player_images = [] 

        #   load all the ship files, scale them and put into a list
        for i in range(1,5):
            player = py.image.load(f'Resources/images/Player/Player{i}/idle.png')
            player=player.subsurface(py.Rect(0, 0, 60, 60))
            player_images.append(player)

        return player_images
    

    #############################################################
    #   Description:
    #
    #       loads the bullet images 
    #
    



class Friend_Player(py.sprite.Sprite):

    def __init__(self, player, s_img, space_coordinates):
        py.sprite.Sprite.__init__(self)

        self.player = player
        self.ship_img = s_img
        self.rect = s_img.get_rect()       
        self.health = 100

        self.space_coordinates = space_coordinates
        



        
