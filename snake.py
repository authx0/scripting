#!/usr/bin/env python3
import curses
import random
import time

def main(stdscr):
    # Initialize curses
    curses.curs_set(0)  # Hide cursor
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food color
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Text color
    
    # Get screen dimensions
    max_y, max_x = stdscr.getmaxyx()
    
    # Check if the terminal is large enough
    if max_y < 15 or max_x < 40:
        stdscr.clear()
        stdscr.addstr(0, 0, "Terminal too small! Need at least 40x15")
        stdscr.refresh()
        time.sleep(2)
        return

    # Game area (leaving space for borders and info)
    game_height = max_y - 4  # Space for instructions and borders
    game_width = max_x - 2   # Space for borders
    
    # Create a window for the game
    game_win = curses.newwin(game_height, game_width, 3, 1)
    game_win.keypad(True)  # Enable keypad mode to capture arrow keys
    game_win.timeout(100)  # Refresh rate in milliseconds (snake speed)
    game_win.border(0)
    
    # Initial snake position and body
    snake_y = game_height // 2
    snake_x = game_width // 2
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2]
    ]
    
    # Initial food position (random)
    food = [random.randint(1, game_height - 2), random.randint(1, game_width - 2)]
    game_win.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(2))
    
    # Initial direction: right
    key = curses.KEY_RIGHT
    
    # Initial score
    score = 0
    
    # Game instructions
    stdscr.addstr(0, 1, "SNAKE GAME - Use arrow keys to move, 'q' to quit", curses.color_pair(3))
    stdscr.addstr(1, 1, f"Score: {score}", curses.color_pair(3))
    stdscr.refresh()
    
    # Main game loop
    while True:
        # Get next key pressed
        next_key = game_win.getch()
        
        # If a key was pressed, set it as the new direction
        if next_key != -1:
            key = next_key
        
        # Check for quit
        if key == ord('q'):
            break
        
        # Calculate new snake head position
        new_head = [snake[0][0], snake[0][1]]
        
        # Handle direction
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        elif key == curses.KEY_UP:
            new_head[0] -= 1
        elif key == curses.KEY_LEFT:
            new_head[1] -= 1
        elif key == curses.KEY_RIGHT:
            new_head[1] += 1
        
        # Insert new head
        snake.insert(0, new_head)
        
        # Check if snake hit the border
        if (new_head[0] == 0 or new_head[0] == game_height - 1 or
            new_head[1] == 0 or new_head[1] == game_width - 1 or
            new_head in snake[1:]):
            game_over(stdscr, game_win, score)
            break
        
        # Check if snake ate food
        if snake[0] == food:
            # Generate new food
            while True:
                food = [random.randint(1, game_height - 2), random.randint(1, game_width - 2)]
                if food not in snake:
                    break
            
            game_win.addch(food[0], food[1], curses.ACS_DIAMOND, curses.color_pair(2))
            
            # Increase score
            score += 10
            stdscr.addstr(1, 1, f"Score: {score}    ", curses.color_pair(3))
            stdscr.refresh()
        else:
            # Remove tail
            tail = snake.pop()
            game_win.addch(tail[0], tail[1], ' ')
        
        # Draw snake head
        game_win.addch(snake[0][0], snake[0][1], curses.ACS_BLOCK, curses.color_pair(1))
        
        # Redraw the border in case it was overwritten
        game_win.border(0)
        game_win.refresh()

def game_over(stdscr, game_win, score):
    game_win.clear()
    h, w = game_win.getmaxyx()
    
    # Display Game Over message
    game_over_msg = "GAME OVER!"
    score_msg = f"Final Score: {score}"
    restart_msg = "Press any key to exit"
    
    game_win.addstr(h//2 - 1, (w - len(game_over_msg))//2, game_over_msg, curses.color_pair(2) | curses.A_BOLD)
    game_win.addstr(h//2, (w - len(score_msg))//2, score_msg, curses.color_pair(3))
    game_win.addstr(h//2 + 1, (w - len(restart_msg))//2, restart_msg, curses.color_pair(3))
    
    game_win.border(0)
    game_win.refresh()
    
    # Wait for a key press
    game_win.timeout(-1)  # Disable timeout
    game_win.getch()

if __name__ == "__main__":
    try:
        # Initialize curses
        curses.wrapper(main)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up curses
        curses.endwin()
        print("Thanks for playing Snake!")

