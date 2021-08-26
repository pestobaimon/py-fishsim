import pygame

from Fish import Fish, Food
from game_params import *
from vector_math import *

pygame.init()  # Start Pygame
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))  # Start the screen
pygame.display.set_caption('Fish Schooling Simulator')
surf_objects = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), flags=0)
surf_helpers = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)

gen = 0


def run_game():
    pygame.init()  # Start Pygame
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))  # Start the screen
    pygame.display.set_caption('Fish Schooling Simulator')

    surf = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), flags=0)

    fish_array = []

    clock = pygame.time.Clock()
    dt = 0
    game_time = 0

    running = True
    while running:
        dt = clock.tick(FPS)
        df = dt / 1000
        game_time += dt
        surf.fill([0, 0, 0])
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    fish_array.append(Fish(pos[0], pos[1], spectate=True))
            if event.type == pygame.MOUSEBUTTONUP:
                fish_array.append(Fish(pos[0], pos[1]))
            if event.type == pygame.QUIT:  # The user closed the window!
                running = False  # Stop running

        for fish in fish_array:
            visible_fish_array, visible_fish_avg_pos = fish.update_fish(fish_array, df)
            pos = fish.position
            if fish.spectate:
                pygame.draw.line(surf, (0, 255, 0), fish.position, (fish.position[0] + fish.visible_left_vect.dir[0],
                                                                    fish.position[1] + fish.visible_left_vect.dir[1]),
                                 width=1)
                pygame.draw.line(surf, (0, 255, 0), fish.position, (fish.position[0] + fish.visible_right_vect.dir[0],
                                                                    fish.position[1] + fish.visible_right_vect.dir[1]),
                                 width=1)
                vel_line = fish.velocity.clamp(50)
                pygame.draw.line(surf, (0, 255, 0), fish.position, (fish.position[0] + vel_line.dir[0],
                                                                    fish.position[1] + vel_line.dir[1]),
                                 width=1)
                pygame.draw.arc(surf, (0, 255, 0),
                                [fish.position[0] - fish.visible_radius, fish.position[1] - fish.visible_radius,
                                 fish.visible_radius*2, fish.visible_radius*2], fish.velocity.angle(),
                                fish.velocity.angle() + fish.visible_angle/2, width=1)
                pygame.draw.arc(surf, (0, 255, 0),
                                [fish.position[0] - fish.visible_radius, fish.position[1] - fish.visible_radius,
                                 fish.visible_radius*2, fish.visible_radius*2], fish.velocity.angle() - fish.visible_angle / 2,
                                fish.velocity.angle(), width=1)
                pygame.draw.circle(surf, (255, 255, 255), visible_fish_avg_pos.dir, 3)
                # pygame.draw.arc(surf, (0, 255, 0),
                #                 [fish.position[0] - fish.visible_radius / 2, fish.position[1] - fish.visible_radius / 2,
                #                  fish.visible_radius, fish.visible_radius], fish.velocity.angle(),
                #                 fish.velocity.angle() - fish.visible_angle / 2, width=1)
            # pygame.draw.circle(surf, (255, 255, 255), pos, 3)

            head_vect = fish.velocity.normalize().multiply(10)
            tail_vect = fish.velocity.normalize().multiply(3)
            head = [pos[0] + head_vect.dir[0], pos[1] + head_vect.dir[1]]
            left_tail = [pos[0] - tail_vect.dir[1], pos[1] + tail_vect.dir[0]]
            right_tail = [pos[0] + tail_vect.dir[1], pos[1] - tail_vect.dir[0]]
            pygame.draw.polygon(surf, (255, 255, 255), (head, left_tail, right_tail))
            for visible_fish in visible_fish_array:
                max_dist = fish.visible_radius
                dist = get_distance_from_a_to_b(fish.position, visible_fish.position)
                if dist > 150:
                    dist = 150
                opacity = (max_dist - dist) / max_dist
                if fish.spectate:
                    line_color = int(255 * opacity)
                    pygame.draw.line(surf, (line_color, 0, 0), fish.position, visible_fish.position, width=1)

        screen.blit(surf, (0, 0))
        pygame.display.update()

    pygame.quit()  # Close the window


# def draw_to_screen(fish_arr, predator, food_arr, surf_obj, surf_help):
#     surf_obj.fill([0, 0, 0])
#     surf_helpers.fill(pygame.Color(0,0,0,0))
#     for fish in fish_arr:
#         pygame.draw.circle(surf_help, (200, 200, 200), fish.position, fish.visible_radius, width=1)
#         pygame.draw.circle(surf_obj, (255, 255, 255), fish.position, 3)
#     for food in food_arr:
#         pygame.draw.circle(surf_obj, (0, 255, 0), food.position, food.size / 2)
#     # pygame.draw.circle(surf, (0, 0, 255), predator.position, 10)
#     # pygame.draw.circle(surf, (255, 0, 255), predator.position, predator.visible_radius, width=1)
#     screen.blit(surf_obj, (0, 0))
#     screen.blit(surf_help, (0, 0))


def check_food_collision(fish: Fish, food: Food, food_array: list):
    between_x = (food.position[0] - (food.size / 2)) <= fish.position[0] <= (food.position[0] + (food.size / 2))
    between_y = (food.position[1] - (food.size / 2)) <= fish.position[1] <= (food.position[1] + (food.size / 2))
    if between_x and between_y:
        fish.eat(food)
        food_array.remove(food)


def check_wall_collide(fish: Fish):
    pos = fish.position
    if pos[0] <= 1 or pos[0] >= 999 or pos[1] <= 1 or pos[1] >= 999:
        return True
    else:
        return False


if __name__ == "__main__":
    run_game()
