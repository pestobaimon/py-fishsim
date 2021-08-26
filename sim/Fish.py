from __future__ import annotations

import random

from game_params import *
from vector_math import *


class Fish:
    stable_speed = 1
    excited_speed = 10
    wander_strength = 0.2

    # steer_strength = 0.5

    def __init__(self, x, y, spectate=False, visible_angle=1.5 * math.pi, visible_radius=150):
        self.spectate = spectate
        self.max_speed = 120

        # self.desired_direction: Vector = make_rand_unit_vector()
        # self.velocity: Vector = self.desired_direction.multiply(self.max_speed)

        # force model
        self.position: [float, float] = [x, y]
        self.velocity: Vector = make_rand_unit_vector().multiply(self.max_speed)

        # visible cone
        self.visible_radius = visible_radius
        self.visible_angle = visible_angle
        self.behind_vect = self.velocity.normalize().multiply(visible_radius).flip()
        self.visible_left_vect = self.behind_vect.rotate((2 * math.pi - self.visible_angle), clockwise=True)
        self.visible_right_vect = self.behind_vect.rotate((2 * math.pi - self.visible_angle), clockwise=False)

    def move(self, delta_time: float):
        old_pos = self.position
        self.position[0] += self.velocity.dir[0] * delta_time
        self.position[1] += self.velocity.dir[1] * delta_time
        self.avoid_collision()
        # print('pos', int(self.position[1])-1, int(self.position[0])-1)

    # def wander(self, vector: Vector):
    #     self.desired_direction = vector.add(make_rand_unit_vector().multiply(self.wander_strength)).normalize()

    def steer_left(self, strength=0.1):
        left_vect = Vector(self.velocity.dir[1], -self.velocity.dir[0]).normalize()
        force = left_vect.multiply(strength)
        return force

    def steer_right(self, strength=0.1):
        right_vect = Vector(-self.velocity.dir[1], self.velocity.dir[0]).normalize()
        force = right_vect.multiply(strength)
        return force

    # def turn_to_point(self, target_x: float, target_y: float):
    #     vector_to_point = Vector(self.position[0], self.position[1], target_x, target_y).normalize()
    #     self.desired_direction = vector_to_point

    # def align_velocity(self, target_vector: Vector):
    #     strength = 0.01
    #     is_right = a_is_right_of_b(self.velocity, target_vector)
    #     if is_right > 0:
    #         self.steer_right(strength=strength)
    #     elif is_right == 0:
    #         pass
    #     else:
    #         self.steer_left(strength=strength)

    def steer_away_from_point_force(self, point: [float, float], strength):
        vector_to_point = Vector(self.position[0] - point[0], self.position[1] - point[1])
        dist = vector_to_point.magnitude()
        max_dist = self.visible_radius
        strength_squared = strength * (max_dist - dist) ** 2

        on_right = self.velocity.cross(vector_to_point) < 0
        on_left = self.velocity.cross(vector_to_point) > 0

        # if self.spectate:
        #     print("target", point)
        #     print("self", self.position)
        #     print("vector_to_point", vector_to_point.dir)
        #     print("velocity", self.velocity.dir)
        #     print("cross", self.velocity.cross(vector_to_point))
        #     print("left", on_left)
        #     print("right", on_right)

        if on_right:
            return self.steer_left(strength=strength_squared)
        else:
            return self.steer_right(strength=strength_squared)

    def steer_to_point_force(self, point: [float, float], strength):
        vector_to_point = Vector(self.position[0] - point[0], self.position[1] - point[1])

        on_left = self.velocity.cross(vector_to_point) > 0
        on_right = self.velocity.cross(vector_to_point) < 0

        # if self.spectate:
        #     print("target", point)
        #     print("self", self.position)
        #     print("vector_to_point", vector_to_point.dir)
        #     print("cross", self.velocity.cross(vector_to_point))
        #     print(on_left)

        if on_left:
            return self.steer_left(strength=strength)
        elif on_right:
            return self.steer_right(strength=strength)
        else:
            return 0

    def is_visible(self, target_fish):
        vect = Vector(target_fish.position[0] - self.position[0], target_fish.position[1] - self.position[1])
        outside_left_boundary = self.visible_left_vect.cross(vect) <= 0
        outside_right_boundary = self.visible_right_vect.cross(vect) >= 0
        if outside_left_boundary or outside_right_boundary:
            return True

    def avoid_collision(self):
        if self.position[0] < 0:
            # self.position[0] = 0
            # self.desired_direction.dir[0] = -self.desired_direction.dir[0]
            self.position[0] = DISPLAY_WIDTH
            self.position[1] = DISPLAY_HEIGHT - self.position[1]

        if self.position[1] < 0:
            # self.position[1] = 0
            # self.desired_direction.dir[1] = -self.desired_direction.dir[1]
            self.position[1] = DISPLAY_HEIGHT
            self.position[0] = DISPLAY_WIDTH - self.position[0]

        if self.position[0] > DISPLAY_WIDTH:
            # self.position[0] = DISPLAY_WIDTH
            # self.desired_direction.dir[0] = -self.desired_direction.dir[0]
            self.position[0] = 0
            self.position[1] = DISPLAY_HEIGHT - self.position[1]

        if self.position[1] > DISPLAY_HEIGHT:
            # self.position[1] = DISPLAY_HEIGHT
            # self.desired_direction.dir[1] = -self.desired_direction.dir[1]
            self.position[1] = 0
            self.position[0] = DISPLAY_WIDTH - self.position[0]

    def update_fish(self, fish_array: list, dt):
        acceleration = Vector(0, 0)

        closest_fish: Fish = None
        distance_to_closest_fish = 1000000

        visible_fish = []
        visible_fish_avg_pos = Vector(0, 0)
        visible_fish_vel_sum = Vector(0, 0)
        visible_fish_pos_sum = Vector(0, 0)
        for fish in fish_array:
            if fish != self:
                distance_from_current_fish = get_distance_from_a_to_b(self.position, fish.position)
                if distance_from_current_fish <= self.visible_radius and self.is_visible(fish):

                    visible_fish_vel_sum = visible_fish_vel_sum.add(fish.velocity)
                    visible_fish_pos_sum = visible_fish_pos_sum.add(Vector(fish.position[0], fish.position[1]))

                    visible_fish.append(fish)
                    if distance_to_closest_fish > distance_from_current_fish:
                        distance_to_closest_fish = distance_from_current_fish
                        closest_fish = fish

        visible_fish_count = len(visible_fish)
        if visible_fish_count > 0:
            visible_fish_avg_pos = visible_fish_pos_sum.multiply(1 / visible_fish_count)

            steer_away_from_fish_force = self.steer_away_from_point_force(closest_fish.position, strength=0.02)
            align_force = self.steer_to_point_force(visible_fish_vel_sum.dir, strength=100)
            cohesion_force = self.steer_to_point_force(visible_fish_avg_pos.dir, strength=200)

            acceleration = acceleration.add(steer_away_from_fish_force)
            acceleration = acceleration.add(align_force)
            acceleration = acceleration.add(cohesion_force)

        self.velocity = self.velocity.add(acceleration.multiply(dt))
        self.velocity = self.velocity.clamp(self.max_speed)

        self.behind_vect = self.velocity.normalize().multiply(self.visible_radius).flip()
        self.visible_left_vect = self.behind_vect.rotate((2 * math.pi - self.visible_angle) / 2, clockwise=True)
        self.visible_right_vect = self.behind_vect.rotate((2 * math.pi - self.visible_angle) / 2, clockwise=False)

        self.avoid_collision()
        self.move(dt)
        return visible_fish, visible_fish_avg_pos


class Food:
    def __init__(self, x, y):
        self.position = (x, y)
        self.life_time = 500
        self.nutrition = random.randint(300, 500)
        self.size = random.randint(5, 20)
