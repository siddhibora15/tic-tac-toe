import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 150
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (150, 206, 180)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Font
FONT = pygame.font.Font(None, 40)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Board
board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Game history
game_history = []

def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (50, SQUARE_SIZE + 50), (SQUARE_SIZE * 3 + 50, SQUARE_SIZE + 50), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (50, 2 * SQUARE_SIZE + 50), (SQUARE_SIZE * 3 + 50, 2 * SQUARE_SIZE + 50), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE + 50, 50), (SQUARE_SIZE + 50, SQUARE_SIZE * 3 + 50), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE + 50, 50), (2 * SQUARE_SIZE + 50, SQUARE_SIZE * 3 + 50), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2) + 50, int(row * SQUARE_SIZE + SQUARE_SIZE // 2) + 50), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE + 50, row * SQUARE_SIZE + SQUARE_SIZE - SPACE + 50), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE + 50, row * SQUARE_SIZE + SPACE + 50), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE + 50, row * SQUARE_SIZE + SPACE + 50), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE + 50, row * SQUARE_SIZE + SQUARE_SIZE - SPACE + 50), CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == ''

def is_board_full():
    return all(all(cell != '' for cell in row) for row in board)

def check_win(player):
    # Check horizontal
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    # Check vertical
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    # Check diagonals
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        return True
    return False

def minimax(depth, is_maximizing):
    if check_win('O'):
        return 1
    if check_win('X'):
        return -1
    if is_board_full():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == '':
                    board[row][col] = 'O'
                    score = minimax(depth + 1, False)
                    board[row][col] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == '':
                    board[row][col] = 'X'
                    score = minimax(depth + 1, True)
                    board[row][col] = ''
                    best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -float('inf')
    best_move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == '':
                board[row][col] = 'O'
                score = minimax(0, False)
                board[row][col] = ''
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    return best_move

def reset_game():
    global board
    screen.fill(BG_COLOR)
    draw_lines()
    board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    draw_ui()
    pygame.display.update()

def draw_ui():
    # Draw "New Game" button
    pygame.draw.rect(screen, WHITE, (550, 50, 200, 50))
    new_game_text = FONT.render("New Game", True, BLACK)
    screen.blit(new_game_text, (590, 60))

    # Draw "Play Again" button
    pygame.draw.rect(screen, WHITE, (550, 120, 200, 50))
    play_again_text = FONT.render("Play Again", True, BLACK)
    screen.blit(play_again_text, (590, 130))

    # Draw game history
    history_text = FONT.render("Game History", True, WHITE)
    screen.blit(history_text, (550, 200))
    
    for i, result in enumerate(game_history[-3:]):
        result_text = FONT.render(result, True, WHITE)
        screen.blit(result_text, (550, 250 + i * 40))

def update_history(result):
    game_history.append(result)
    if len(game_history) > 3:
        game_history.pop(0)

# Main game loop
player = 'X'
game_over = False

draw_lines()
draw_ui()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            
            # Check if "New Game" button is clicked
            if 550 <= mouseX <= 750 and 50 <= mouseY <= 100:
                reset_game()
                game_over = False
                player = 'X'
                continue

            # Check if "Play Again" button is clicked
            if 550 <= mouseX <= 750 and 120 <= mouseY <= 170:
                if game_over:
                    reset_game()
                    game_over = False
                    player = 'X'
                continue
            
            if not game_over:
                clicked_row = int((mouseY - 50) // SQUARE_SIZE)
                clicked_col = int((mouseX - 50) // SQUARE_SIZE)
                
                if 0 <= clicked_row < 3 and 0 <= clicked_col < 3 and available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    if check_win(player):
                        game_over = True
                        update_history(f"Player {player} wins!")
                    elif is_board_full():
                        game_over = True
                        update_history("It's a draw!")
                    player = 'O'
    
    if player == 'O' and not game_over:
        row, col = ai_move()
        if row is not None and col is not None:
            mark_square(row, col, player)
            if check_win(player):
                game_over = True
                update_history("AI wins!")
            elif is_board_full():
                game_over = True
                update_history("It's a draw!")
            player = 'X'
    
    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    draw_ui()
    pygame.display.update()