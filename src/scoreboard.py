import pygame
from config import *


class ScoreBoard:
    def __init__(self):
        self.score = 0
        self.lines_cleared = 0
        self.font = get_font(30)

    def update_score(self, lines_cleared):
        if lines_cleared > 0:
            # Score calculation: more lines = exponentially more points
            # 1 line = 100, 2 lines = 300, 3 lines = 600, 4 lines = 1000
            points = {1: 100, 2: 300, 3: 600, 4: 1000}
            self.score += points.get(lines_cleared, 0)
            self.lines_cleared += lines_cleared

    def draw(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, "#FFFFFF")
        lines_text = self.font.render(f"Lines: {self.lines_cleared}", True, "#FFFFFF")

        # Position the text in the top right corner
        score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 20, 50))
        lines_rect = lines_text.get_rect(topright=(SCREEN_WIDTH - 20, 90))

        screen.blit(score_text, score_rect)
        screen.blit(lines_text, lines_rect)
