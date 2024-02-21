import random

class Color:
    def __init__(self):
        self.WHITE = (255, 255, 255)
        self.RED = (228, 129, 129)
        self.GREEN = (69, 164, 69)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (116, 0, 194)
        self.CYAN = (0, 255, 255)

    def random_color_background(self):
        color_available = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return random.choice(color_available)