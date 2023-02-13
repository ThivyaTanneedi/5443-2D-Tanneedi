#Assignment - 01

#Divya Podila , T.L.N.S Thivya

#2048 Game in python using pygame!!

import pygame
import random
import time
pygame.init()

# Defining variables initially
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont('comicsansms.ttf', 24)
# Load the smiley image
smiley_img = pygame.image.load("C:/Users/18586/OneDrive/Desktop/__pycache__/smiley.png")

# defining colors for 2048 game
colors = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    'light text': (249, 246, 242),
    'dark text': (119, 110, 101),
    'other': (0, 0, 0),
    'bg': (187, 173, 160)
}

# initializing game variables 
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
file = open('high_score', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high
high_score = score
flag = False

# draw game over board and display restart message
def draw_over():
   
    pygame.draw.rect(screen, 'black', [65,50,250,100], 0, 20)
    game_over_text1 = font.render('Game Over!', True, 'White')
    game_over_text2 = font.render('  Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))


# take turn based on direction
def take_turn(direc, board):
    global score
    global smiley_x
    global smiley_y
    global flag
    flag = False
    merged = [[False for _ in range(4)] for _ in range(4)]
    result_pos = [] # emptylist to store the action for every tile merge. 
    #So, make it empty after each action to store multipple resultant merge.
    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2

                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True
                        
                        smiley_x = j * 95 + 57 # center tile coordinate
                        smiley_y = (i-shift - 1) * 95 + 57 # center tile coordinate for y
                        result_pos.append([smiley_x,smiley_y]) # after this action, append  x,y in the list
                        flag = True
                        
    elif direc == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j]                             and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True
                        flag = True
                        smiley_x = j * 95 + 57
                        smiley_y = (3-i+shift) * 95 + 57 
                        result_pos.append([smiley_x,smiley_y])


    elif direc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True
                    flag = True
                    smiley_x = (j-shift-1) * 95 + 57
                    smiley_y = i * 95 + 57
                    result_pos.append([smiley_x,smiley_y])
                    


    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift]                             and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
                        smiley_x = (4-j+shift) * 95 + 57 
                        smiley_y =  i * 95 + 57 
                        result_pos.append([smiley_x,smiley_y])
                        flag = True

    return board ,result_pos ,flag 


# create new pieces randomly when directions start
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


# draw background for the board
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'Black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'Black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))
    pass


# drawing tiles for game
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75],
                             0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.SysFont('Comic Sans.ttf',
                                           48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57,
                                                        i * 95 + 57))
                #screen.blit(smiley, text_rect)

                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black',
                                 [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)


# 2048 Game loop - Runs until run = True
run = True
while run:
    
    timer.tick(fps)
    screen.fill('Gray')
    draw_board()
    draw_pieces(board_values)
    if flag == True:
        for i in pos: # i is a pair of coordiante , for each x,y [[30,30],[45,75]]
            screen.blit(smiley_img, smiley_img.get_rect(center = (i[0] , i[1]) ))
             #i is a list , i[0] and i[1] are the indices of x&y [30,30]
            pygame.display.flip() 
        time.sleep(0.5) #to display smiley and disappear, stop the execution for 0.5sec
        draw_pieces(board_values) # to make the smiley disappear, re-write the board values (re-display tiles as is)
        flag = False #until next merge, smiley should not appear, so make flag = FALSE
    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count =init_count+ 1
    if direction != '': 
        board_values , pos ,flag = take_turn(direction, board_values)
        direction = ''
        spawn_new = True
        
    if game_over:
        draw_over()
        if high_score > init_high:
            file = open('high_score', 'w')
            file.write(f'{high_score}')
            file.close()
            init_high = high_score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'

            if game_over:
                
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ''
                    game_over = False

    if score > high_score:
        high_score = score

    pygame.display.flip()
pygame.quit()




