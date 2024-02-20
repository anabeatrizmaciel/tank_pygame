import pygame
from wall import Wall

class Maze:

    def __init__(self, width, height, colors, maze_structure):
        self.width = width
        self.height = height
        self.colors = colors
        self.maze_structure = maze_structure  # Representation of the maze's structure
        self.background_color = self.colors.random_color_background() # Select a random color to the background, different form the wall's color
        self.walls = pygame.sprite.Group() # Create a group of sprites to store tha maze's walls
        self.create_walls_group()  # Create the walls according to the maze's structure

    def create_walls_group(self):
        cell_height = 40
        brick_height = 50
        brick_image = pygame.image.load("assets/bricks1.png").convert_alpha()
        brick_image = pygame.transform.scale(brick_image, (brick_height, brick_height))

        for y, row in enumerate(self.maze_structure):
            for x, cell in enumerate(row):
                if cell == "#":
                    wall = Wall(x * cell_height, y * cell_height * 0.4, brick_image)
                    self.walls.add(wall)
    def draw(self, screen):
        screen.fill(self.background_color)  # Fill the background with the random color selected

        for wall in self.walls: 
            screen.blit(wall.image, wall.rect) # Draw each wall in the screen