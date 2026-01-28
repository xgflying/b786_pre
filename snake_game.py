# snake_game.py
import pygame
import random
import sys
from typing import List, Tuple

from game_constants import *

# Initialize pygame
pygame.init()

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        self.reset_game()
    
    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT  # Add direction queue
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.apples_eaten = 0
    
    def generate_food(self) -> Tuple[int, int]:
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), 
                   random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    return True
                
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    return True
                
                if not self.paused:
                    # Use current direction for collision check, not next_direction
                    if event.key == pygame.K_w and self.direction != Direction.DOWN:
                        self.next_direction = Direction.UP
                    elif event.key == pygame.K_s and self.direction != Direction.UP:
                        self.next_direction = Direction.DOWN
                    elif event.key == pygame.K_a and self.direction != Direction.RIGHT:
                        self.next_direction = Direction.LEFT
                    elif event.key == pygame.K_d and self.direction != Direction.LEFT:
                        self.next_direction = Direction.RIGHT
        
        return True
    
    def update(self):
        if self.game_over or self.paused:
            return
        
        # Update direction from queue at the start of each frame
        self.direction = self.next_direction
        
        # Move snake
        head = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head[0] + dx, head[1] + dy)
        
        # Check collision with walls
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.game_over = True
            return
        
        # Check collision with self
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check if food is eaten
        if new_head == self.food:
            self.score += 10
            self.apples_eaten += 1
            self.food = self.generate_food()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def get_background_color(self):
        """Return background color based on apples eaten"""
        if self.apples_eaten >= 10:
            return DARK_BLUE
        else:
            return BLACK
    
    def draw_apple(self, x, y):
        """Draw an apple-like food item"""
        center_x = x * GRID_SIZE + GRID_SIZE // 2
        center_y = y * GRID_SIZE + GRID_SIZE // 2
        radius = GRID_SIZE // 2 - 2
        
        # Draw apple body (red circle)
        pygame.draw.circle(self.screen, RED, (center_x, center_y), radius)
        pygame.draw.circle(self.screen, DARK_RED, (center_x, center_y), radius, 2)
        
        # Draw apple stem (small brown rectangle)
        stem_width = 3
        stem_height = 6
        stem_x = center_x - stem_width // 2
        stem_y = center_y - radius - stem_height + 2
        pygame.draw.rect(self.screen, BROWN, (stem_x, stem_y, stem_width, stem_height))
        
        # Draw apple leaf (small green oval)
        leaf_width = 6
        leaf_height = 4
        leaf_x = center_x + 2
        leaf_y = center_y - radius - 2
        pygame.draw.ellipse(self.screen, APPLE_GREEN, (leaf_x, leaf_y, leaf_width, leaf_height))
    
    def get_border_radius_head(self, direction):
        """Get border radius tuple based on direction for head segment"""
        if direction == Direction.UP:
            return (10, 10, 0, 0)
        elif direction == Direction.DOWN:
            return (0, 0, 10, 10)
        elif direction == Direction.LEFT:
            return (10, 0, 10, 0)
        elif direction == Direction.RIGHT:
            return (0, 10, 0, 10)
        return (0, 0, 0, 0)  # Default case
    
    def get_border_radius_tail(self, tailSegment, previousSegment):
        """Get border radius tuple based on position of the previous segment for tail segment"""
        # Calculate the direction from previous segment to tail
        dx = tailSegment[0] - previousSegment[0]
        dy = tailSegment[1] - previousSegment[1]
        
        # The tail should round the corners opposite to the direction of the previous segment
        # border_radius format: (top_left, top_right, bottom_left, bottom_right)
        if dx > 0:  # Tail is to the right of previous segment
            return (0, 10, 0, 10)
        elif dx < 0:  # Tail is to the left of previous segment
            return (10, 0, 10, 0)
        elif dy > 0:  # Tail is below previous segment
            return (0, 0, 10, 10)
        elif dy < 0:  # Tail is above previous segment
            return (10, 10, 0, 0)
        else:
            return (0, 0, 0, 0)
    
    def draw(self):
        # Fill background with dynamic color
        self.screen.fill(self.get_background_color())
        
        # Draw snake segments
        for i, segment in enumerate(self.snake):
            rect_x = segment[0] * GRID_SIZE
            rect_y = segment[1] * GRID_SIZE
            rect_width = GRID_SIZE
            rect_height = GRID_SIZE
            
            if i == 0: #head
                color = BRIGHT_GREEN
                border_radius = self.get_border_radius_head(self.direction)
                # Draw rectangle
                pygame.draw.rect(self.screen, color, (rect_x, rect_y, rect_width, rect_height), 
                    border_top_left_radius=border_radius[0], border_top_right_radius=border_radius[1], 
                    border_bottom_left_radius=border_radius[2], border_bottom_right_radius=border_radius[3])
                # Draw border
                pygame.draw.rect(self.screen, DARK_GREEN, (rect_x, rect_y, rect_width, rect_height), width=2, 
                    border_top_left_radius=border_radius[0], border_top_right_radius=border_radius[1], 
                    border_bottom_left_radius=border_radius[2], border_bottom_right_radius=border_radius[3])
            elif i == len(self.snake) - 1: #tail
                color = GREEN
                border_radius = self.get_border_radius_tail(segment, self.snake[i - 1])
                # Draw rectangle
                pygame.draw.rect(self.screen, color, (rect_x, rect_y, rect_width, rect_height), 
                    border_top_left_radius=border_radius[0], border_top_right_radius=border_radius[1], 
                    border_bottom_left_radius=border_radius[2], border_bottom_right_radius=border_radius[3])
                # Draw border
                pygame.draw.rect(self.screen, DARK_GREEN, (rect_x, rect_y, rect_width, rect_height), width=2, 
                    border_top_left_radius=border_radius[0], border_top_right_radius=border_radius[1], 
                    border_bottom_left_radius=border_radius[2], border_bottom_right_radius=border_radius[3])
            else:
                # Body segments: use rectangles
                color = GREEN
                rect_x = segment[0] * GRID_SIZE
                rect_y = segment[1] * GRID_SIZE
                rect_width = GRID_SIZE
                rect_height = GRID_SIZE
                
                # Draw rectangle
                pygame.draw.rect(self.screen, color, (rect_x, rect_y, rect_width, rect_height))
                # Draw border
                pygame.draw.rect(self.screen, DARK_GREEN, (rect_x, rect_y, rect_width, rect_height), width=2)
        
        # Draw apple food
        self.draw_apple(self.food[0], self.food[1])
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over screen
        if self.game_over:
            self.draw_game_over()
        elif self.paused:
            self.draw_pause_screen()
        
        pygame.display.flip()
        
    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.big_font.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        # Final score
        final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        self.screen.blit(final_score_text, score_rect)
        
        # Restart instruction
        restart_text = self.font.render("Press SPACE to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_pause_screen(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.big_font.render("PAUSED", True, BLUE)
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, text_rect)
        
        # Instruction
        instruction_text = self.font.render("Press P to resume", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(instruction_text, instruction_rect)
    
    def run(self):
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)  # 10 FPS for smooth gameplay
        
        pygame.quit()
        sys.exit()

def main():
    print("Starting Snake Game...")
    
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    main()
