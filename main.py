from game import Game

def main():
    game_instance = Game()

    while True:
        game_instance.battlefield.draw_field(game_instance.tank1_x, game_instance.tank1_y,
                                             game_instance.tank2_x, game_instance.tank2_y,
                                             game_instance.bullets)

        action1 = input("Player 1 - Choose an action (w, a, s, d to move, t to shoot): ")
        action2 = input("Player 2 - Choose an action (w, a, s, d to move, t to shoot): ")

        # Process tank movements and shooting
        if action1 == "w" and game_instance.tank1_y > 0:
            game_instance.tank1_y -= 1
        elif action1 == "s" and game_instance.tank1_y < game_instance.battlefield.height - 1:
            game_instance.tank1_y += 1
        elif action1 == "a" and game_instance.tank1_x > 0:
            game_instance.tank1_x -= 1
        elif action1 == "d" and game_instance.tank1_x < game_instance.battlefield.width // 2 - 1:
            game_instance.tank1_x += 1
        elif action1 == "t":
            game_instance.shoot(game_instance.tank1_x, game_instance.tank1_y, "d")

        if action2 == "w" and game_instance.tank2_y > 0:
            game_instance.tank2_y -= 1
        elif action2 == "s" and game_instance.tank2_y < game_instance.battlefield.height - 1:
            game_instance.tank2_y += 1
        elif action2 == "a" and game_instance.tank2_x > game_instance.battlefield.width // 2:
            game_instance.tank2_x -= 1
        elif action2 == "d" and game_instance.tank2_x < game_instance.battlefield.width - 1:
            game_instance.tank2_x += 1
        elif action2 == "t":
            game_instance.shoot(game_instance.tank2_x, game_instance.tank2_y, "a")

        # Bullet movement and removal logic
        game_instance.move_bullets()

        # Check for winner
        if game_instance.score_tank1 >= 3 or game_instance.score_tank2 >= 3:
            print("Game Over!")
            if game_instance.score_tank1 >= 3:
                print("Player 1 wins!")
            else:
                print("Player 2 wins!")
            break

if __name__ == "__main__":
    main()

