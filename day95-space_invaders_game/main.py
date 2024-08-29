import setup
from ship import Ship
from bullet import Bullet
from invaders import InvadersWall
import math
import time

MAX_BULLETS = 3
COLLISION_DISTANCE = 15
bullets = []


def fire_bullet(position):
    if len(bullets) < MAX_BULLETS:
        new_bullet = Bullet(position)
        bullets.append(new_bullet)


def is_collision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    return distance < COLLISION_DISTANCE


def main():
    window = setup.setup_screen()
    ship = Ship()
    wall = InvadersWall()

    window.listen()
    window.onkeypress(ship.move_right, "Right")
    window.onkeypress(ship.move_left, "Left")
    window.onkeypress(lambda: fire_bullet(ship.get_position()), "space")

    game_in_progress = True

    while game_in_progress:
        window.update()
        time.sleep(0.02)

        for bullet in bullets:
            bullet.move()
            if bullet.ycor() > 500:
                bullet.ht()
                bullet.goto(1000, 1000)
                bullets.remove(bullet)

            # Check for a collision between the bullet and invaders
            for invader in wall.invaders:
                if is_collision(bullet, invader):
                    bullet.remove_from_screen()
                    bullets.remove(bullet)
                    wall.remove_invader(invader)

        wall.move_invaders()

        for invader in wall.invaders:
            # Check for a collision between the ship and invaders
            if is_collision(ship, invader):
                ship.remove_from_screen()
                invader.remove_from_screen()
                print("Game Over")
                game_in_progress = False

        if len(wall.invaders) == 0:
            game_in_progress = False

    print("YOU WON!")


if __name__ == "__main__":
    main()
