class Wall:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw_field(self, tank1_x, tank1_y, tank2_x, tank2_y, bullets):
        for y in range(self.height):
            for x in range(self.width):
                if x == tank1_x and y == tank1_y:
                    print("T1", end='')
                elif x == tank2_x and y == tank2_y:
                    print("T2", end='')
                elif any(b.x == x and b.y == y for b in bullets):
                    print("B", end='')  # Bullet indicator
                else:
                    print(".", end='')
            print()
