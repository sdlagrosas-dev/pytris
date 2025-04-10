import pygame


class BlockField(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.GRID_WIDTH = 10
        self.GRID_HEIGHT = 20
        self.CELL_SIZE = 30
        self.blocks = [[0] * self.GRID_WIDTH for _ in range(self.GRID_HEIGHT)]
        
        # Position the grid in the center of the screen
        self.x_offset = 400  # Adjust this value to center the grid
        self.y_offset = 50   # Add some padding from the top
        
    def get_cell_position(self, row, col):
        """Convert grid coordinates to screen coordinates"""
        return (self.x_offset + col * self.CELL_SIZE, 
                self.y_offset + row * self.CELL_SIZE)
    
    def is_valid_position(self, row, col):
        """Check if the given position is within the grid bounds"""
        return (0 <= row < self.GRID_HEIGHT and 
                0 <= col < self.GRID_WIDTH)
    
    def add_piece(self, tetromino, row, col):
        """Try to add a tetromino to the grid at the specified position"""
        for y in range(len(tetromino.shape)):
            for x in range(len(tetromino.shape[y])):
                if tetromino.shape[y][x]:
                    if not self.is_valid_position(row + y, col + x):
                        return False
                    if self.blocks[row + y][col + x]:
                        return False
        
        # If we get here, the position is valid, so add the piece
        for y in range(len(tetromino.shape)):
            for x in range(len(tetromino.shape[y])):
                if tetromino.shape[y][x]:
                    self.blocks[row + y][col + x] = tetromino.color
        return True
    
    def clear_lines(self):
        """Clear any completed lines and return the number of lines cleared"""
        lines_cleared = 0
        y = self.GRID_HEIGHT - 1
        while y >= 0:
            if all(self.blocks[y]):
                # Move all lines above this one down
                for move_y in range(y, 0, -1):
                    self.blocks[move_y] = self.blocks[move_y - 1][:]
                self.blocks[0] = [0] * self.GRID_WIDTH
                lines_cleared += 1
            else:
                y -= 1
        return lines_cleared

    def draw(self, screen):
        # Draw the background grid
        for row in range(self.GRID_HEIGHT):
            for col in range(self.GRID_WIDTH):
                x, y = self.get_cell_position(row, col)
                pygame.draw.rect(screen, (50, 50, 50), 
                               (x, y, self.CELL_SIZE, self.CELL_SIZE), 1)

        # Draw the filled blocks
        for row in range(self.GRID_HEIGHT):
            for col in range(self.GRID_WIDTH):
                if self.blocks[row][col]:
                    x, y = self.get_cell_position(row, col)
                    color = self.blocks[row][col]
                    pygame.draw.rect(screen, color,
                                   (x + 1, y + 1, 
                                    self.CELL_SIZE - 2, self.CELL_SIZE - 2))
                    
    def is_game_over(self):
        """Check if the game is over (i.e., a block has reached the top)"""
        return any(block for row in self.blocks[:1] for block in row)

