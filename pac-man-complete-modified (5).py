import pygame
import random
import time
import math
import sqlite3


# Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGRAY = (200, 200, 200)
DARKGRAY = (100, 100, 100)
PASTEL_BLUE = (173, 216, 230)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
LIGHT_GREEN = (144, 238, 144)
TAN = (210, 180, 140)
MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0)]
WIDTH, HEIGHT = 480, 480

def main_menu():
    initialize_db()
    running = True
    button_height = 24
    button_y_start = 70
    button_spacing = 10
    button_x_start = 140
    button_width = 200

    # Initialize Pygame
    pygame.init()

    # Game window dimensions
    WIDTH, HEIGHT = 480, 480
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man")
    font = pygame.font.Font(None, 36)

    def draw_button(screen, text, x, y, w, h, color):
        pygame.draw.rect(screen, color, (x, y, w, h))
        text_surf = font.render(text, True, BLACK)
        text_rect = text_surf.get_rect(center=(x + w / 2, y + h / 2))
        screen.blit(text_surf, text_rect)

    

    # Smaller font for scores
    score_font = pygame.font.Font(None, 24)
    title_font = pygame.font.Font(None, 72)

    # Define colors for each letter in "Pac-Man"
    colors = [RED, CYAN, YELLOW, GREEN, PASTEL_BLUE, TAN, LIGHT_GREEN]
    while running:
        screen.fill(BLACK)
        title_text = "Pac-Man"
        x_offset = 140  # Starting position of the title
        for i, letter in enumerate(title_text):
            letter_surf = title_font.render(letter, True, colors[i % len(colors)])
            letter_rect = letter_surf.get_rect(left=x_offset, top=10)
            screen.blit(letter_surf, letter_rect)
            x_offset += letter_rect.width

        # Draw buttons at the top
        draw_button(screen, "Start Playing", 140, button_y_start, 200, button_height, GREEN)
        draw_button(screen, "User Guide", 140, button_y_start + button_height + button_spacing, 200, button_height, YELLOW)  # Added User Guide button
        draw_button(screen, "Exit", 140, button_y_start + 2 * (button_height + button_spacing), 200, button_height, PASTEL_BLUE)

        # Display instructions below the buttons
        instructions = "Use arrow keys to move"
        instructions1 = "Top 10 High Scores"

        text_surf = font.render(instructions, True, WHITE)
        instructions_y = button_y_start + 3 * (button_height + button_spacing)
        screen.blit(text_surf, (100, instructions_y))

        text_surf1 = font.render(instructions1, True, CYAN)
        instructions_y1 = button_y_start + 3 * (button_height + button_spacing)
        screen.blit(text_surf1, (100, instructions_y1 + 30))

        # High Score Section
        scores_y_start = instructions_y + 70
        scores_section_top = scores_y_start - 10  # Slightly above the first score
        scores_section_height = 262  # Adjust as needed
        pygame.draw.rect(screen, DARKGRAY, (100, scores_section_top, 280, scores_section_height), 2)  # Score section border

        # Display top scores within the designated section
        for name, score in get_high_scores():
            score_text = f"{name}: {score}"
            text_surf = score_font.render(score_text, True, CYAN)
            screen.blit(text_surf, (120, scores_y_start))
            scores_y_start += 25  # Adjust spacing for smaller font size
            if scores_y_start > scores_section_top + scores_section_height - 25:
                break  # Stop to avoid overflow

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check if the mouse click is within the "Start Playing" button
                if button_x_start <= mouse_x <= button_x_start + button_width and \
                   button_y_start <= mouse_y <= button_y_start + button_height:
                    run()  
                    running = False
                elif button_x_start <= mouse_x <= button_x_start + button_width and \
                     button_y_start + button_height + button_spacing <= mouse_y <= button_y_start + 2 * (button_height + button_spacing):
                    display_user_guide(screen)
                elif button_x_start <= mouse_x <= button_x_start + button_width and \
                    button_y_start + 2 * (button_height + button_spacing) <= mouse_y <= button_y_start + 3 * (button_height + button_spacing):
                    running = False  # Set running to False to exit the menu loop
                    pygame.quit()  # Quit pygame
                    return  # Exit the main_menu function

                

        pygame.display.flip()

def display_user_guide(screen):
    def draw_button(screen, text, x, y, w, h, color):
        pygame.draw.rect(screen, color, (x, y, w, h))
        font = pygame.font.Font(None, 24)
        text_surf = font.render(text, True, BLACK)
        text_rect = text_surf.get_rect(center=(x + w / 2, y + h / 2))
        screen.blit(text_surf, text_rect)
    # Function to display the user guide
    user_guide_text = [
        "User Guide:",
        "1. Use arrow keys to move Pac-Man.",
        "2. Collect all the dots without getting caught by the enemies.",
        "3. Score points by collecting dots.",
        "4. Avoid collisions with enemies.",
        "5. Press 'Spacebar' to start the game.",
        "6. Have fun playing Pac-Man!",
        '',
        '',
        "Made with love by Smith"
    ]
    screen.fill(BLACK)
    font = pygame.font.Font(None, 24)
    y_offset = 50
    for line in user_guide_text:
        text_surf = font.render(line, True, WHITE)
        screen.blit(text_surf, (14, y_offset))
        y_offset += 30
    # Add a back button
    draw_button(screen, "Back", 200, 400, 100, 30, PASTEL_BLUE)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 200 <= mouse_x <= 300 and 400 <= mouse_y <= 430:
                    return


def initialize_db():
    conn = sqlite3.connect('pacman_scores.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def save_score(name, score):
    conn = sqlite3.connect('pacman_scores.db')
    c = conn.cursor()
    c.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
    conn.commit()
    conn.close()

def input_box(screen, message):
    font = pygame.font.Font(None, 36)
    instruction_font = pygame.font.Font(None, 20)
    input_box = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    selected_level = None
    levels = ["Easy", "Medium", "Hard"]
    level_states = [False] * len(levels)  # To keep track of selected levels
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                if event.key in [pygame.K_SPACE, pygame.K_LEFT, pygame.K_RIGHT]:
                    # Deselect all levels
                    level_states = [False] * len(levels)
                    # Toggle selection for the corresponding level
                    if event.key == pygame.K_SPACE:
                        level_states[0] = True
                    elif event.key == pygame.K_LEFT:
                        level_states[1] = True
                    elif event.key == pygame.K_RIGHT:
                        level_states[2] = True

        screen.fill((30, 30, 30))
        # Display instructions for selecting the level
        instruction_text = "Press spacebar for Easy, > for Hard, and < for Medium"
        instruction_surf = instruction_font.render(instruction_text, True, WHITE)
        screen.blit(instruction_surf, (WIDTH // 4, HEIGHT // 3 - 30))
        
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        # Draw checkboxes for levels
        checkbox_y = input_box.bottom + 10
        for i, level in enumerate(levels):
            checkbox_x = input_box.x + 5 + i * 120
            checkbox_rect = pygame.Rect(checkbox_x, checkbox_y, 20, 20)
            pygame.draw.rect(screen, color_inactive, checkbox_rect, 2)
            if level_states[i]:
                pygame.draw.rect(screen, (0, 255, 0), (checkbox_x + 3, checkbox_y + 3, 14, 14))  # Filled rectangle for selection

            level_text = font.render(level, True, (255, 255, 255))
            screen.blit(level_text, (checkbox_x + 30, checkbox_y))

        pygame.display.flip()

    return text, [levels[i] for i, state in enumerate(level_states) if state]




def display_scores(screen, high_scores):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)
    y = 100
    for name, score in high_scores:
        score_text = f"{name}: {score}"
        text_surface = font.render(score_text, True, (255, 255, 255))
        screen.blit(text_surface, (WIDTH // 4, y))
        y += 40
    pygame.display.flip()
    pygame.time.wait(5000)


def get_high_scores():
    conn = sqlite3.connect('pacman_scores.db')
    c = conn.cursor()
    c.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT 10")
    high_scores = c.fetchall()
    conn.close()
    return high_scores


def generate_maze(width, height):
    # Create a grid with all walls
    maze = [[1 for x in range(width)] for y in range(height)]
    # Create a set to hold the cells with paths
    path_cells = set()
    # Start with a random cell and carve a path
    start_cell = (random.randint(1, width-2), random.randint(1, height-2))
    path_cells.add(start_cell)
    stack = [start_cell]

    # Directions to move
    directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]

    while stack:
        current_cell = stack[-1]
        x, y = current_cell
        # Determine new potential cells to visit
        potential_cells = [(x+dx, y+dy) for dx, dy in directions if 0 < x+dx < width-1 and 0 < y+dy < height-1]
        neighbors = [cell for cell in potential_cells if cell not in path_cells]
        if neighbors:
            next_cell = random.choice(neighbors)
            path_cells.add(next_cell)
            stack.append(next_cell)
            # Carve a path between the current cell and the next cell
            mid_x, mid_y = (x + next_cell[0]) // 2, (y + next_cell[1]) // 2
            maze[mid_y][mid_x] = 2
            maze[next_cell[1]][next_cell[0]] = 2
        else:
            stack.pop()

    # Ensure the outer walls and add dots inside the paths
    for x in range(width):
        maze[0][x] = maze[height-1][x] = 1
    for y in range(height):
        maze[y][0] = maze[y][width-1] = 1
    for y in range(1, height-1):
        for x in range(1, width-1):
            if maze[y][x] == 2 and ((x+1) % 2 or (y+1) % 2):
                maze[y][x] = 0  # Make cells with value '2' into dots

    return maze


def find_pacman_start_position(maze):
    for y in range(1, len(maze)-1):
        for x in range(1, len(maze[y])-1):
            if maze[y][x] == 0:  # Find the first empty path
                return x, y
    return 1, 1  # Fallback position


def A_star(board, start, goal):
    def heuristic(node):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    if start == goal:
        return []

    open_list = [(*start, 0, None)]  # (x, y, g_cost, parent)
    closed_list = set()

    MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    while open_list:
        open_list.sort(key=lambda x: x[2] + heuristic(x[:2]))
        current = open_list.pop(0)

        # Check if the current node is the goal
        if current[:2] == goal:
            path = []
            while current:
                path.append(current[:2])
                current = current[3]
            return path[::-1][1:]  # Reverse and remove the start node

        closed_list.add(current[:2])

        for move in MOVES:
            neighbor = (current[0] + move[0], current[1] + move[1])
            if 0 <= neighbor[0] < len(board[0]) and 0 <= neighbor[1] < len(board) and board[neighbor[1]][neighbor[0]] != 1:
                if neighbor not in closed_list:
                    g_cost = current[2] + 1
                    if not any(item[:2] == neighbor for item in open_list) or g_cost < [item for item in open_list if item[:2] == neighbor][0][2]:
                        open_list.append((*neighbor, g_cost, current))
    return None


def run():
    # Initialize the display
    WIDTH, HEIGHT = 480, 480
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man")

    # Game window dimensions
    BOARD_WIDTH, BOARD_HEIGHT = 20, 20
    TILE_SIZE = WIDTH // BOARD_WIDTH

    # Game state variables
    global pacman_x, pacman_y, score, enemies, board, direction, game_over
    score = 0
    game_over = False

    score = 0
    
    board = generate_maze(BOARD_WIDTH, BOARD_HEIGHT)
    pacman_x, pacman_y = find_pacman_start_position(board)

    # Pac-Man's initial position and size
    pacman_size = TILE_SIZE

    # Directions
    UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
    direction = RIGHT

    # Speed of Pac-Man (pixels per game loop iteration)
    pacman_speed = 2

    # Enemy setup
    num_enemies = 3  # Number of enemies
    enemies = [{"x": random.randint(1, BOARD_WIDTH-2), "y": random.randint(1, BOARD_HEIGHT-2), "dir": random.choice([UP, DOWN, LEFT, RIGHT])} for _ in range(num_enemies)]

    # Score
    score = 0

    # Main game loop
    running = True
    clock = pygame.time.Clock()    
    
    running = True
    clock = pygame.time.Clock()
    player_name, selected_level = input_box(screen, "Enter your name and select level:")
    selected_level = selected_level[0]

    # Adjust the game difficulty based on the selected level
    if selected_level.lower() == 'easy':
        pacman_speed = 1  
    elif selected_level.lower() == 'medium':
        pacman_speed = 2  
    elif selected_level.lower() == 'hard':
        pacman_speed = 3  

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = UP
                elif event.key == pygame.K_DOWN:
                    direction = DOWN
                elif event.key == pygame.K_LEFT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    direction = RIGHT

        if not game_over:
            # Update Pac-Man's position with speed adjustment
            new_x = pacman_x + direction[0] * pacman_speed
            new_y = pacman_y + direction[1] * pacman_speed
            if 0 <= new_x < BOARD_WIDTH and 0 <= new_y < BOARD_HEIGHT and board[new_y][new_x] != 1:
                pacman_x, pacman_y = new_x, new_y
                if board[pacman_y][pacman_x] == 2:
                    board[pacman_y][pacman_x] = 0
                    score += 1

            # Check if all dots have been collected
            remaining_dots = sum(row.count(2) for row in board)
            if remaining_dots == 0:
                board = generate_maze(BOARD_WIDTH, BOARD_HEIGHT)
                pacman_x, pacman_y = find_pacman_start_position(board)
                enemies = [{"x": random.randint(1, BOARD_WIDTH-2), "y": random.randint(1, BOARD_HEIGHT-2)} for _ in range(num_enemies)]

            # Update enemies' positions
            for enemy in enemies:
                path = A_star(board, (enemy["x"], enemy["y"]), (pacman_x, pacman_y))
                if path:
                    next_x, next_y = path[1]
                    enemy["x"], enemy["y"] = next_x, next_y

            # Check for collision with enemies
            for enemy in enemies:
                if enemy["x"] == pacman_x and enemy["y"] == pacman_y:
                    time.sleep(0.5)
                    game_over = True
                if (abs(enemy["x"] - pacman_x) <= 1 and enemy["y"] == pacman_y) or \
                   (abs(enemy["y"] - pacman_y) <= 1 and enemy["x"] == pacman_x):
                    time.sleep(0.5)
                    game_over = True

        screen.fill((0, 0, 0))

        if game_over:
            font = pygame.font.Font(None, 72)
            text = font.render('Game Over', True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            save_score(player_name, score)
            display_scores(screen, get_high_scores())
            break

        else:
            # Render the maze with walls and dots
            for y in range(BOARD_HEIGHT):
                for x in range(BOARD_WIDTH):
                    cell_value = board[y][x]
                    if cell_value == 1:  # Wall
                        pygame.draw.rect(screen, (0, 0, 255), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    elif cell_value == 2:  # Dot
                        pygame.draw.circle(screen, (255, 255, 255), (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), 5)

            # Draw Pac-Man
            pacman_rect = pygame.Rect(pacman_x * TILE_SIZE, pacman_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.arc(screen, (255, 255, 0), pacman_rect, 0.2 * math.pi, 1.8 * math.pi)

            # Draw enemies
            for enemy in enemies:
                enemy_rect = pygame.Rect(enemy["x"] * TILE_SIZE, enemy["y"] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, (255, 0, 0), enemy_rect)

            # Draw score
            font = pygame.font.Font(None, 36)
            text = font.render(f'Score: {score}', True, (255, 255, 255))
            screen.blit(text, (5, 5))

        # Update the display
        pygame.display.flip()
        clock.tick(10)
    main_menu()

# Initialize the database
# initialize_db()
main_menu()
