import pygame
from config import *

class Tetromino(pygame.sprite.Sprite):
    def __init__(self, shape, color):
        super().__init__()
        self.shape = shape
        self.color = color
        self.row = 0  # Grid position
        self.col = self.calculate_start_column()
        self.fall_time = 0
        self.fall_speed = 1.0  # Seconds per grid cell
        
    def calculate_start_column(self):
        """Calculate starting column to center the piece"""
        width = len(self.shape[0])
        return (10 - width) // 2  # 10 is grid width
        
    def move(self, d_row, d_col, block_field):
        """Try to move the piece by the given delta. Returns True if successful."""
        new_row = self.row + d_row
        new_col = self.col + d_col
        
        # Check if new position would be valid
        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                if self.shape[y][x]:
                    if not block_field.is_valid_position(new_row + y, new_col + x):
                        return False
                    if block_field.blocks[new_row + y][new_col + x]:
                        return False
        
        self.row = new_row
        self.col = new_col
        return True
        
    def rotate(self, block_field):
        """Rotates the piece clockwise if possible"""
        # Store old shape in case rotation is invalid
        old_shape = self.shape
        
        # Transpose the matrix and then reverse each row
        rows = len(self.shape)
        cols = len(self.shape[0])
        new_shape = [[0 for _ in range(rows)] for _ in range(cols)]
        
        for i in range(rows):
            for j in range(cols):
                new_shape[j][rows - 1 - i] = self.shape[i][j]
        
        # Test if rotation is valid
        self.shape = new_shape
        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                if self.shape[y][x]:
                    if not block_field.is_valid_position(self.row + y, self.col + x):
                        self.shape = old_shape
                        return False
                    if block_field.blocks[self.row + y][self.col + x]:
                        self.shape = old_shape
                        return False
        return True
        
    def update(self, dt, block_field):
        """Update piece position based on time and input"""
        self.fall_time += dt
        
        # Handle keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move(0, -1, block_field)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move(0, 1, block_field)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.fall_speed = 0.1  # Fall faster while pressing down
        else:
            self.fall_speed = 1.0

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rotate(block_field)
            
        if keys[pygame.K_SPACE]:
            # Hard drop
            while self.move(1, 0, block_field):
                pass
            # Lock the piece in place
            block_field.add_piece(self, self.row, self.col)
            
        # Handle falling
        if self.fall_time >= self.fall_speed:
            if not self.move(1, 0, block_field):
                # If we can't move down, lock the piece in place
                block_field.add_piece(self, self.row, self.col)
                return True  # Signal that we need a new piece
            self.fall_time = 0
            
        return False
        
    def draw(self, screen, block_field):
        """Draw the piece at its current position"""
        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                if self.shape[y][x]:
                    screen_x, screen_y = block_field.get_cell_position(
                        self.row + y, self.col + x)
                    pygame.draw.rect(screen, self.color,
                                   (screen_x + 1, screen_y + 1, 
                                    block_field.CELL_SIZE - 2, 
                                    block_field.CELL_SIZE - 2))

# Define the Tetromino shapes using 2D arrays
TETROMINO_SHAPES = {
    'I': [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    'J': [
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
    ],
    'L': [
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0]
    ],
    'O': [
        [1, 1],
        [1, 1]
    ],
    'S': [
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0]
    ],
    'T': [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0]
    ],
    'Z': [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0]
    ]
}

# Assign colors to tetrominos (can be RGB tuples, or any color representation)
TETROMINO_COLORS = {
    'I': (0, 255, 255),  # Cyan
    'J': (0, 0, 255),  # Blue
    'L': (255, 0, 0),  # Red
    'O': (255, 255, 0),  # Yellow
    'S': (0, 255, 0),  # Green
    'T': (128, 0, 128), # Purple
    'Z': (255, 0, 255) # Magenta
}