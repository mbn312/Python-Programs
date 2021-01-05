import pygame
import pygame.freetype
import random
import copy
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from pygame.sprite import RenderUpdates

#RGB Codes for colors used
WHITE = (255,255,255)
BLACK = (0,0,0)
MAPLE = (241, 195, 142)
RED = (255,102,102)
LIGHT_RED = (255,153,153)
GREEN = (102,255,102)
YELLOW = (255,255,204)
GRAY = (192,192,192)
DARK_GRAY = (64,64,64)

COUNTER = 0

#Class for Sudoku Game
class Game:

    def __init__(self,screen,bg_color=WHITE,selected=None,rows=9,cols=9,width=500,height=500,solutions=0,left=81,ended=False):
        self.ended = ended
        self.left = left
        self.selected = selected
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.screen = screen
        self.solutions = solutions
        self.bg_color = bg_color
        self.original_board = [[0 for i in range(9)] for x in range(9)]
        self.solution_board = [[0 for i in range(9)] for x in range(9)]
        self.board = [[0 for i in range(9)] for x in range(9)]
        self.squares = [[Square(screen,(width/cols),(height/rows),row,col) for row in range(rows)] for col in range(cols)]

    #sets whether or not the game has ended
    def end(self,val):
        self.ended = val

    #sets all of its squares equal to the its boards values
    def set_all_squares(self):
        self.left = 0 
        for row in range(self.rows):
            for col in range(self.cols):
                val = self.board[row][col]
                if val == 0:
                    val = None
                    self.left += 1
                self.squares[row][col].set_value(val)
                self.squares[row][col].set_valid(None)
                self.squares[row][col].set_selected(False)

    #sets a single square and board value
    def set_square(self,val):
        pos = self.selected
        if val is None:
            self.board[pos[0]][pos[1]] = 0
        else:
            self.board[pos[0]][pos[1]] = val
        self.squares[pos[0]][pos[1]].set_value(val)

    def clear_temp_values(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.squares[r][c].set_temp_value(0)

    #checks to see if any squares are invalid
    def check_invalid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.squares[r][c].valid is not None and not self.squares[r][c].valid:
                    return True
        return False

    #sets which square is selected
    def select_square(self,pos):
        if self.selected is not None:
            cur = self.selected
            self.squares[cur[0]][cur[1]].set_selected(False)
        self.selected = pos
        if pos is not None:
            self.squares[pos[0]][pos[1]].set_selected(True)
    
    #returns the position of where the users mouseclick was on the board
    def click(self, mouse_pos):
        pos = (int((mouse_pos[1] - 50)/(self.height/9)),int((mouse_pos[0] - 150)/(self.width/9)))
        return pos

    #creates a random new board
    def new_board(self):
        self.original_board,self.solution_board = create_board()
        self.board = copy.deepcopy(self.original_board)
        self.set_all_squares()
        self.selected = None
        self.clear_temp_values()

    #clears all the values from the board
    def clear_board(self):
        self.original_board = [[0 for i in range(9)] for x in range(9)]
        self.solution_board = [[0 for i in range(9)] for x in range(9)]
        self.board = [[0 for i in range(9)] for x in range(9)]
        self.squares = [[Square(self.screen,(self.width/self.cols),(self.height/self.rows),row,col) for row in range(self.rows)] for col in range(self.cols)]
        self.selected = None
        self.clear_temp_values()

    #resets the board to the original version
    def reset_board(self):
        self.board = copy.deepcopy(self.original_board)
        self.set_all_squares()
        self.selected = None
        self.clear_temp_values()

    #checks to see if all the spots are filled to determine if the winner has won
    def check_win(self):
        self.left -= 1
        if self.left == 0:
            self.win()
            self.ended = True
            return True
        else:
            return False
    
    #solves the board and shows the changes
    def solve(self,delay=10):
        idx = (0,0)
        while self.board[idx[0]][idx[1]] != 0:
            if idx[1] + 1 > 8:
                idx = (idx[0] + 1, 0)
            else:
                idx = (idx[0], idx[1] + 1)

            if idx == (9, 0):
                return True

        num_list = [i for i in range(1, 10)]
        for check in num_list:
            if is_valid(self.board, idx[0], idx[1], check):
                self.board[idx[0]][idx[1]] = check                
                self.squares[idx[0]][idx[1]].set_value(check)
                self.squares[idx[0]][idx[1]].set_valid(True)
                self.draw()
                pygame.display.update()
                pygame.time.delay(delay)

                if self.solve():
                    self.squares[idx[0]][idx[1]].set_valid(True)
                    return True

                self.squares[idx[0]][idx[1]].set_valid(False)
                self.board[idx[0]][idx[1]] = 0
                self.squares[idx[0]][idx[1]].set_value(0)
                self.draw()
                pygame.display.update()
                pygame.time.delay(delay)

        return False

    #sets all the squares as valid
    def win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.squares[r][c].set_valid(True)

    #sets all the squares that are wrong to invalid
    def lose(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.squares[r][c].value != self.solution_board[r][c]:
                    self.squares[r][c].set_valid(False)

    #draws the board
    def draw(self):
        pygame.draw.rect(self.screen, WHITE, [150,50,self.width,self.height])
        space = self.width/9

        for row in range(self.rows):
            for col in range(self.cols):
                self.squares[row][col].draw()

        for i in range(self.rows + 1):
            if i % 3 == 0:
                pygame.draw.line(self.screen, BLACK, (150, i*space+50), (self.width +150, i*space+50), 4)
                pygame.draw.line(self.screen, BLACK, (i * space+150, 50), (i * space+150, self.height+50), 4)
            else:
                pygame.draw.line(self.screen, BLACK, (150, i*space+50), (self.width+150, i*space+50), 1)
                pygame.draw.line(self.screen, BLACK, (i * space+150, 50), (i * space+150, self.height+50), 1)

#class for each of the games squares
class Square:

    def __init__(self,screen,width,height,row,col,temp=0,value=None,selected=False,valid=None):
        self.screen = screen
        self.width = width
        self.height = height
        self.row = row
        self.col = col
        self.value = value
        self.temp = temp
        self.selected = selected
        self.valid = valid

    #sets the value of the square
    def set_value(self,val):
        self.value = val

    #sets whether or not the square is selected
    def set_selected(self,val):
        self.selected = val

    #sets the temporary value of the square
    def set_temp_value(self,val):
        self.temp = val
    
    #sets whether or not the square is valid
    def set_valid(self,val):
        self.valid = val

    #draws the square
    def draw(self):
        font = pygame.freetype.SysFont("Times New Roman", 30)
        pos = (self.width * self.row, self.width * self.col)

        if self.valid is not None:
            if self.valid:
                pygame.draw.rect(self.screen,GREEN,(pos[0]+150,pos[1]+50,self.width+1,self.width+1))
                bg_rgb = GREEN
            else:
                pygame.draw.rect(self.screen,RED,(pos[0]+150,pos[1]+50,self.width+1,self.width+1))
                bg_rgb = RED
        elif self.selected:
            pygame.draw.rect(self.screen,YELLOW,(pos[0]+150,pos[1]+50,self.width+1,self.width+1))
            bg_rgb = YELLOW
        else:
            bg_rgb = WHITE

        if self.value is not None:
            text,_ = font.render(text=str(self.value),fgcolor=BLACK,bgcolor=bg_rgb)
            self.screen.blit(text, (150 + pos[0] + (self.width/2 - text.get_width()/2), 50 + pos[1] + (self.width/2 - text.get_height()/2)))         
        elif self.temp != 0 and bg_rgb != RED:
            text,_ = font.render(text=str(self.temp),fgcolor=GRAY,bgcolor=bg_rgb)
            self.screen.blit(text, (150 + pos[0] + (self.width/2 - text.get_width()/2), 50 + pos[1] + (self.width/2 - text.get_height()/2))) 
        elif self.temp != 0:
            text,_ = font.render(text=str(self.temp),fgcolor=DARK_GRAY,bgcolor=bg_rgb)
            self.screen.blit(text, (150 + pos[0] + (self.width/2 - text.get_width()/2), 50 + pos[1] + (self.width/2 - text.get_height()/2))) 


#generates a random sudoku board
def create_board():

    global COUNTER

    #blank is the desired amount of blank spots for the puzzle
    blank = 60
    #fail is the maximum amount of failures allowed
    fail = 5
    valid = False

    #creates a random valid sudoku solution
    while not valid:
        board = [[0 for i in range(9)] for x in range(9)]
        #calls on the solve function to fill in the grid and make sure that it is valid
        valid = solve_board(board, False)

    solution = copy.deepcopy(board)
    #removes spaces until wanted number of blank spots or maximum amount of failures is reached
    while (fail > 0 and blank > 0):
        COUNTER = 0
        test_board = copy.deepcopy(board)
        #randomly chooses a filled in spot to remove
        while True:
            rand = random.randint(0, 80)
            rem = (rand//9, rand%9)
            if test_board[rem[0]][rem[1]] != 0:
                test_board[rem[0]][rem[1]] = 0
                break
        #tests to see if board with the random spot removed has only one solution
        solve_board(test_board, True)

        #if it only has one solution it will keep the change or else it will count as a failure
        if COUNTER == 1:
            board[rem[0]][rem[1]] = 0
            blank -= 1
        else:
            fail -= 1

    #returns the created board
    return board,solution

#returns whether the board is solvable, solves the board, or gets the number of solutions
def solve_board(board, count):
    idx = (0, 0)
    while board[idx[0]][idx[1]] != 0: #loops through the board looking for an empty spot
        if idx[1] + 1 > 8:
            idx = (idx[0] + 1, 0)
        else:
            idx = (idx[0], idx[1] + 1)

        if idx == (9, 0): #if the board is filled, returns that the board is solvable
            return True

    num_list = [i for i in range(1, 10)]
    random.shuffle(num_list) #shuffles the domain to generate a random puzzle
    for check in num_list:
        if is_valid(board, idx[0], idx[1], check): #checks to see if a number is valid for that spot
            board[idx[0]][idx[1]] = check
            #recursively calls the function to see if the number leads to a solution
            if solve_board(board, count):
                if count:
                    #if looking for number of solutions, it will increment counter by 1
                    global COUNTER
                    COUNTER += 1
                else:
                    return True #returns that the board is solvable

            board[idx[0]][idx[1]] = 0

    return False #returns that the board is not solvable if it isn't

#function checks to see if a number is valid for a certain position
def is_valid(board, row, col, check):

    #checks to see if any spots in the same row have the same value
    for c in range(9):
        if board[row][c] == check and c != col:
            return False

    #checks to see if any spots in the same column have the same value
    for r in range(9):
        if (board[r][col] == check and r != row):
            return False

    #checks to see if any spots in the same box have the same value
    x = 3 * (col // 3)
    y = 3 * (row // 3)
    for r in range(3):
        for c in range(3):
            if board[y+r][x+c] == check and (y+r, x+c) != (row, col):
                return False

    return True


#creates a surface with text on it to add to GUI
def create_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Times New Roman", font_size, bold=True)
    surface,_ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

#function prints out an text version of inputted board
def printboard(board):

    print("-------------------------------------")
    for r in range(9):
        if r % 3 == 0 and r != 0:
            print("|-----------|-----------|-----------|")
        row = "|  "
        for c in range(9):
            if c == 0:
                sep = ""
            elif c % 3 == 0:
                sep = "  |  "
            else:
                sep = "  "
            if board[r][c] == 0:
                val = " "
            else:
                val = str(board[r][c])
            row = row + sep + val
        print(row + "  |")
    print("-------------------------------------")

#class for the player
class Player:
    def __init__(self, streak=0):
        self.streak = streak

    def update_streak(self,win):
        if win:
            self.streak += 1
        else:
            self.streak = 0

#class for the all of the buttons in the program
class UIElement(Sprite):

    def __init__(self, center_pos, text, font_size, text_rgb, bg_rgb, hl_action = True, hl_rgb=None, action=None):

        super().__init__()

        self.mouse_over = False
        default_img = create_text(text, font_size, text_rgb, bg_rgb)

        if hl_action:
            if hl_rgb is not None:
                highlighted_img = create_text('* ' + text + ' *', font_size, hl_rgb, bg_rgb)
            else:
                highlighted_img = create_text('* ' + text + ' *', font_size, text_rgb, bg_rgb)
        else:
            highlighted_img = default_img

        self.images = [default_img, highlighted_img]
        self.rects = [default_img.get_rect(center = center_pos),
                     highlighted_img.get_rect(center = center_pos)]

        self.action = action
    
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    #sets whether or not the mouse is over the button and returns action if it is clicked
    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False
    
    #draws the button
    def draw(self, surface):
        surface.blit(self.image, self.rect)

#class for which screen to be on
class GameState(Enum):
    QUIT = -1
    TITLE = 0
    GAME_BOARD = 1
    SOLVER = 2

#class for which board action to perform
class BoardAction(Enum):
    NOTHING = 0
    SOLVE = 1
    RESET = 2
    NEWGAME = 3
    HOME = 4

#displays the title screen of the program
def title_screen(screen):

    title = UIElement(
        center_pos = (400,150),
        font_size = 100,
        bg_rgb = MAPLE,
        text_rgb = WHITE,
        hl_action = False,
        text = "Sudoku"
    )

    play_btn = UIElement(
        center_pos = (400,350),
        font_size = 30,
        bg_rgb = MAPLE,
        text_rgb = WHITE,
        text = "New Game",
        action = GameState.GAME_BOARD
    )

    solver_btn = UIElement(
        center_pos = (400,400),
        font_size = 30,
        bg_rgb = MAPLE,
        text_rgb = WHITE,
        text = "Solver",
        action = GameState.SOLVER
    )

    quit_btn = UIElement(
        center_pos = (400,450),
        font_size = 30,
        bg_rgb = MAPLE,
        text_rgb = WHITE,
        text = "QUIT",
        action = GameState.QUIT
    )

    buttons = [title, play_btn, quit_btn, solver_btn]

    while True:
        mouse_up = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill(MAPLE)
        
        for btn in buttons:
            btn_action = btn.update(pygame.mouse.get_pos(),mouse_up)
            if btn_action is not None:
                return btn_action
            btn.draw(screen)

        pygame.display.flip()

#displays the solver screen for the program
def solver_screen(screen):
    game = Game(screen)
    board_action = BoardAction.NOTHING

    solve_btn = UIElement(
        center_pos = (650,575),
        font_size = 20,
        bg_rgb = MAPLE,
        text_rgb = WHITE,
        text = "Solve",
        action = BoardAction.SOLVE
    )
    clear_btn = UIElement(
        center_pos = (400,575),
        font_size = 20,
        bg_rgb = MAPLE,
        text_rgb = WHITE,
        text = "Clear",
        action = BoardAction.RESET
    )
    home_btn = UIElement(
        center_pos = (150,575),
        font_size = 20,
        bg_rgb = MAPLE,
        text_rgb = WHITE,
        text = "Home",
        action = BoardAction.HOME
    )

    buttons = [home_btn, clear_btn, solve_btn]

    while True:

        if board_action == BoardAction.SOLVE:
            if not game.check_invalid():
                game.select_square(None)
                game.solve(0)
            board_action = BoardAction.NOTHING
        elif board_action == BoardAction.RESET:
            game.clear_board()
            board_action = BoardAction.NOTHING
        elif board_action == BoardAction.HOME:
            return GameState.TITLE

        mouse_up = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                if pos[0] >= 150 and pos[0] <= 150 + game.height and pos[1] >=50 and pos[1] <= 50 + game.width:
                    game.select_square(game.click(pos))
                else:
                    mouse_up = True
            elif event.type == pygame.KEYDOWN and game.selected is not None:        
                row = game.selected[0]
                col = game.selected[1]
                value = -1

                if event.key == pygame.K_1:
                    value = 1
                elif event.key == pygame.K_2:
                    value = 2
                elif event.key == pygame.K_3:
                    value = 3
                elif event.key == pygame.K_4:
                    value = 4
                elif event.key == pygame.K_5:
                    value = 5
                elif event.key == pygame.K_6:
                    value = 6
                elif event.key == pygame.K_7:
                    value = 7
                elif event.key == pygame.K_8:
                    value = 8
                elif event.key == pygame.K_9:
                    value = 9
                elif event.key == pygame.K_DELETE or event.key == pygame.K_SPACE or event.key == pygame.K_0:
                    value = None

                if value is None or value > 0:
                    if value is None or is_valid(game.board, row, col, value):
                        game.squares[row][col].set_valid(None)
                    else:
                        game.squares[row][col].set_valid(False)

                    game.set_square(value)

        screen.fill(MAPLE)
        
        for btn in buttons:
            btn_action = btn.update(pygame.mouse.get_pos(),mouse_up)
            if btn_action is not None:
                    board_action = btn_action
            btn.draw(screen)
            
        game.draw()
        pygame.display.flip()

#displays the game board screen for the program
def game_board_screen(screen):

    player = Player()
    game = Game(screen)
    game.new_board()
    board_action = BoardAction.NOTHING
    
    solve_btn = UIElement(
        center_pos = (650,575),
        font_size = 20,
        bg_rgb = MAPLE,
        text_rgb = WHITE,
        text = "Solve",
        action = BoardAction.SOLVE
    )
    reset_btn = UIElement(
        center_pos = (400,575),
        font_size = 20,
        bg_rgb = MAPLE,
        text_rgb = WHITE,
        text = "Reset",
        action = BoardAction.RESET
    )
    home_btn = UIElement(
        center_pos = (150,575),
        font_size = 20,
        bg_rgb = MAPLE,
        text_rgb = WHITE,
        text = "Home",
        action = BoardAction.HOME
    )
    newgame_btn = UIElement(
        center_pos = (650,575),
        font_size = 20,
        bg_rgb = MAPLE,
        text_rgb = WHITE,
        text = "New Game",
        action = BoardAction.NEWGAME
    )    

    buttons = [home_btn,solve_btn,reset_btn]
  
    while True:

        if board_action == BoardAction.SOLVE:
            game.select_square(None)
            game.solve()
            game.end(True)
            buttons = [newgame_btn,home_btn,reset_btn]
            board_action = BoardAction.NOTHING
        elif board_action == BoardAction.RESET:
            game.end(False)
            game.reset_board()
            buttons = [home_btn,solve_btn,reset_btn]
            board_action = BoardAction.NOTHING
        elif board_action == BoardAction.NEWGAME:
            game.new_board()
            buttons = [home_btn,solve_btn,reset_btn]
            game.end(False)
            board_action = BoardAction.NOTHING
        elif board_action == BoardAction.HOME:
            if player.streak > 0:
                print("Streak Ended at " + str(player.streak) + " wins")
            return GameState.TITLE

        mouse_up = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if player.streak > 0:
                    print("Streak Ended at " + str(player.streak) + " wins")
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                if not game.ended and pos[0] >= 150 and pos[0] <= 150 + game.height and pos[1] >=50 and pos[1] <= 50 + game.width:
                    game.select_square(game.click(pos))
                else:
                    mouse_up = True
            elif not game.ended and event.type == pygame.KEYDOWN and game.selected is not None:        
                row = game.selected[0]
                col = game.selected[1]
                if game.squares[row][col].value is None:
                    value = -1
                    cur = game.squares[row][col].temp

                    if event.key == pygame.K_1:
                        value = 1
                    elif event.key == pygame.K_2:
                        value = 2
                    elif event.key == pygame.K_3:
                        value = 3
                    elif event.key == pygame.K_4:
                        value = 4
                    elif event.key == pygame.K_5:
                        value = 5
                    elif event.key == pygame.K_6:
                        value = 6
                    elif event.key == pygame.K_7:
                        value = 7
                    elif event.key == pygame.K_8:
                        value = 8
                    elif event.key == pygame.K_9:
                        value = 9
                    elif event.key == pygame.K_DELETE or event.key == pygame.K_SPACE or event.key == pygame.K_0:
                        value = 0
                    elif event.key == pygame.K_RETURN and cur != 0:
                        value = 0
                        game.set_square(cur)
                        if game.solution_board[row][col] == cur:
                            game.squares[row][col].set_valid(True)
                            if game.check_win():
                                buttons = [newgame_btn,home_btn,reset_btn]
                                player.update_streak(True)
                                print("Current Streak = " + str(player.streak))
                        else:
                            game.lose()
                            game.end(True)
                            if player.streak > 0:
                                print("Streak Ended at " + str(player.streak) + " wins")
                            player.update_streak(False)
                            buttons = [newgame_btn,home_btn,reset_btn]
                    
                    if value >= 0 and value != cur:
                        game.squares[row][col].set_temp_value(value)

        screen.fill(MAPLE)
        
        for btn in buttons:
            btn_action = btn.update(pygame.mouse.get_pos(),mouse_up)
            if btn_action is not None:
                    board_action = btn_action
            btn.draw(screen)
            
        game.draw()
        pygame.display.flip()


#runs the program
def main():

    #initializes pygame
    pygame.init()

    #creates screen with width of 800 and height of 600
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Sudoku")

    #comment out two line below if you did not download the icon into the program directory
    icon = pygame.image.load('sudoku_icon.png')
    pygame.display.set_icon(icon)

    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)
        elif game_state == GameState.GAME_BOARD:
            game_state = game_board_screen(screen)
        elif game_state == GameState.SOLVER:
            game_state = solver_screen(screen)
        elif game_state == GameState.QUIT:
            pygame.quit()
            return

main()
