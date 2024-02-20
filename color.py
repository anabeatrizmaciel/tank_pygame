import random

class Color:
    def __init__(self):
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (228, 129, 129)
        self.GREEN = (69, 164, 69)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (116, 0, 194)
        self.CYAN = (0, 255, 255)

    def random_color_wall(self):
        return random.choice([self.RED, self.GREEN, self.BLUE, self.YELLOW, self.PURPLE, self.CYAN])

    def random_color_background(self, cor):
        color_available = [c for c in [self.RED, self.GREEN, self.BLUE, self.YELLOW, self.PURPLE, self.CYAN] if
                             c != cor]
        return random.choice(color_available)