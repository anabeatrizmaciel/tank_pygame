class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def move(self):
        if self.direction == "w":
            self.y -= 1
        elif self.direction == "s":
            self.y += 1
        elif self.direction == "a":
            self.x -= 1
        elif self.direction == "d":
            self.x += 1
