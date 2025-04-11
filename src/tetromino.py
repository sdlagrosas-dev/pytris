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
        self.rotation_cd = 0  # Cooldown for rotation
        self.hard_drop_cd = 0.2  # Cooldown for hard drop

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

    def can_place(self, block_field):
        """Check if the piece can be placed at its current position"""
        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                if self.shape[y][x]:
                    if not block_field.is_valid_position(self.row + y, self.col + x):
                        return False
                    if block_field.blocks[self.row + y][self.col + x]:
                        return False
        return True

    def find_drop_position(self, block_field):
        """Calculate the lowest possible position for the piece"""
        test_row = self.row
        while True:
            next_row = test_row + 1
            can_move = True

            # Check if next position would be valid
            for y in range(len(self.shape)):
                for x in range(len(self.shape[y])):
                    if self.shape[y][x]:
                        if not block_field.is_valid_position(
                            next_row + y, self.col + x
                        ):
                            can_move = False
                            break
                        if block_field.blocks[next_row + y][self.col + x]:
                            can_move = False
                            break
                if not can_move:
                    break

            if not can_move:
                break
            test_row = next_row

        return test_row

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

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rotation_cd <= 0:
            if self.rotate(block_field):
                self.rotation_cd = 0.1
        else:
            self.rotation_cd -= dt
            if self.rotation_cd < 0:
                self.rotation_cd = 0

        if keys[pygame.K_SPACE] and self.hard_drop_cd <= 0:
            # Hard drop - calculate final position and place piece there
            final_row = self.find_drop_position(block_field)
            self.row = final_row
            block_field.add_piece(self, self.row, self.col)
            return True  # Signal that we need a new piece
        else:
            self.hard_drop_cd -= dt
            if self.hard_drop_cd < 0:
                self.hard_drop_cd = 0

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
                        self.row + y, self.col + x
                    )
                    pygame.draw.rect(
                        screen,
                        self.color,
                        (
                            screen_x + 1,
                            screen_y + 1,
                            block_field.CELL_SIZE - 2,
                            block_field.CELL_SIZE - 2,
                        ),
                    )


# Define the Tetromino shapes using 2D arrays
TETROMINO_SHAPES = {
    "I": [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
    "J": [[1, 0, 0], [1, 1, 1], [0, 0, 0]],
    "L": [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
    "O": [[1, 1], [1, 1]],
    "S": [[0, 1, 1], [1, 1, 0], [0, 0, 0]],
    "T": [[0, 1, 0], [1, 1, 1], [0, 0, 0]],
    "Z": [[1, 1, 0], [0, 1, 1], [0, 0, 0]],
}

# Assign colors to tetrominos (can be RGB tuples, or any color representation)
TETROMINO_COLORS = {
    "I": (153, 102, 204),  # Muted Purple
    "J": (102, 153, 153),  # Soft Teal
    "L": (204, 153, 102),  # Warm Sand
    "O": (153, 153, 102),  # Olive
    "S": (102, 153, 102),  # Sage Green
    "T": (153, 102, 153),  # Dusty Rose
    "Z": (204, 102, 102),  # Muted Red
}
