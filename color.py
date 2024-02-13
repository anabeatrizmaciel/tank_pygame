import pygame
import random

class Color:
    def __init__(self):
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (255, 0, 255)
        self.CYAN = (0, 255, 255)

    def random_color_wall(self):
        return random.choice([self.RED, self.GREEN, self.BLUE, self.YELLOW, self.PURPLE, self.CYAN])

    def random_color_background(self, cor):
        cores_disponiveis = [c for c in [self.RED, self.GREEN, self.BLUE, self.YELLOW, self.PURPLE, self.CYAN] if
                             c != cor]
        return random.choice(cores_disponiveis)