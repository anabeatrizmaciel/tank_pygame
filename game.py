
import random
from wall import Wall
from bullet import Bullet

class Game:
    def __init__(self):
        self.battlefield = Wall(20, 10)
        self.tank1_x = random.randint(0, self.battlefield.width // 2)
        self.tank1_y = random.randint(0, self.battlefield.height)
        self.tank2_x = random.randint(self.battlefield.width // 2, self.battlefield.width - 1)
        self.tank2_y = random.randint(0, self.battlefield.height)
        self.bullets = []
        self.score_tank1 = 0
        self.score_tank2 = 0

    def check_collision(self, bullet):
        # implement collision detection logic and update the score
        if self.is_hit(self.tank1_x, self.tank1_y, bullet.x, bullet.y):
            self.score_tank2 += 1
            print("Player 1 hit! Player 2 scores!")
            return True
        elif self.is_hit(self.tank2_x, self.tank2_y, bullet.x, bullet.y):
            self.score_tank1 += 1
            print("Player 2 hit! Player 1 scores!")
            return True
        return False

    def is_hit(self, target_x, target_y, bullet_x, bullet_y):
        # Check if the bullet is close enough to the target
        return abs(target_x - bullet_x) <= 1 and abs(target_y - bullet_y) <= 1

    def move_bullets(self):
        self.bullets = [bullet for bullet in self.bullets
                        if 0 <= bullet.x < self.battlefield.width and 0 <= bullet.y < self.battlefield.height]
        for bullet in self.bullets:
            bullet.move()
            if self.check_collision(bullet):
                self.bullets.remove(bullet)

    def shoot(self, tank_x, tank_y, direction):
        new_bullet = Bullet(tank_x, tank_y, direction)
        self.bullets.append(new_bullet)
