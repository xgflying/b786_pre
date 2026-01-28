# Snake Game

A classic Snake game implemented in Python using Pygame.

## Features

- Classic snake gameplay mechanics
- Smooth controls with arrow keys
- Score tracking
- Pause functionality
- Game over screen with restart option
- Clean, modern UI with grid lines
- Collision detection (walls and self)

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

1. Run the game:
   ```bash
   python snake_game.py
   ```

2. Controls:
   - **Arrow Keys**: Move the snake
   - **P**: Pause/Resume the game
   - **SPACE**: Restart the game (when game over)
   - **ESC**: Quit the game

## Game Rules

- Control the snake to eat the red food
- Each food eaten increases your score by 10 points
- The snake grows longer with each food eaten
- Game ends if you hit the walls or yourself
- Try to get the highest score possible!

## Requirements

- Python 3.6+
- Pygame 2.0.0+

## File Structure

- `snake_game.py` - Main game file
- `requirements.txt` - Python dependencies
- `README.md` - This file 