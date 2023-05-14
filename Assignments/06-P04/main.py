from Game import Game
import sys
import os
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)
Game().run()