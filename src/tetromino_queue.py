import pygame
from tetromino import Tetromino, TETROMINO_SHAPES, TETROMINO_COLORS
import random


class TetrominoQueue:
    def __init__(self, queue_size=3):
        self.queue_size = queue_size
        self.queue = [self._create_new_tetromino() for _ in range(queue_size)]
        self.hold_piece = None
        self.hold_cooldown = False
        self.can_hold = True
        self.font = pygame.font.Font("assets/font.ttf", 20)

    def _create_new_tetromino(self):
        shape_name = random.choice(list(TETROMINO_SHAPES.keys()))
        shape = TETROMINO_SHAPES[shape_name]
        color = TETROMINO_COLORS[shape_name]
        return Tetromino(shape, color)

    def get_next_piece(self):
        next_piece = self.queue.pop(0)
        self.queue.append(self._create_new_tetromino())
        next_piece.row = 0
        next_piece.col = next_piece.calculate_start_column()
        self.can_hold = True
        return next_piece

    def hold_current_piece(self, current_piece):
        if not self.can_hold:
            return current_piece

        self.can_hold = False
        if self.hold_piece is None:
            # First hold
            self.hold_piece = Tetromino(current_piece.shape, current_piece.color)
            return self.get_next_piece()
        else:
            # Swap current and held piece
            temp = Tetromino(current_piece.shape, current_piece.color)
            current_piece = Tetromino(self.hold_piece.shape, self.hold_piece.color)
            self.hold_piece = temp
            return current_piece

    def _draw_preview(self, screen, piece, x, y, cell_size=20):
        # Center the piece in its preview box
        shape = piece.shape
        width = len(shape[0]) * cell_size
        height = len(shape) * cell_size

        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col]:
                    pygame.draw.rect(
                        screen,
                        piece.color,
                        (
                            x + col * cell_size,
                            y + row * cell_size,
                            cell_size - 1,
                            cell_size - 1,
                        ),
                    )

    def draw(self, screen):
        # Draw hold piece
        hold_text = self.font.render("HOLD", True, "#FFFFFF")
        screen.blit(hold_text, (50, 50))

        if self.hold_piece:
            self._draw_preview(screen, self.hold_piece, 50, 80)

        # Draw next pieces
        next_text = self.font.render("NEXT", True, "#FFFFFF")
        screen.blit(next_text, (50, 200))

        for i, piece in enumerate(self.queue):
            self._draw_preview(screen, piece, 50, 230 + i * 80)
