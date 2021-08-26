from __future__ import annotations

from game_params import *
from vector_math import *


class Predator:
    stable_speed = 1
    excited_speed = 10
    wander_strength = 0.1
    steer_strength = 0.9

    def __init__(self, x, y):
        self.max_speed = 80
        self.velocity: Vector = make_rand_unit_vector().multiply(self.max_speed)
        self.desired_direction: Vector = make_rand_unit_vector()
        self.visible_range = 200
        self.position: [float, float] = [x, y]

    def move(self, delta_time: float):
        self.position[0] += self.velocity.x * delta_time
        self.position[1] += self.velocity.y * delta_time

    def steer(self, vector: Vector):
        self.desired_direction = add_vector(vector, make_rand_unit_vector().multiply(self.wander_strength)).normalize()

    def get_distance_to_closest_fish(self):
        cf: Fish = self.closest_fish
        return get_distance_from_a_to_b(self.position[0], self.position[1], cf.position[0], cf.position[1])

    def scan_environment(self, fish_arr):
        closest_fish = None
        for fish in fish_arr:
            distance_from_current_fish = get_distance_from_a_to_b(self.position[0], self.position[1], fish.position[0],
                                                                  fish.position[1])
            if distance_from_current_fish <= self.visible_range:
                if closest_fish is None:
                    closest_fish = fish
                elif distance_from_current_fish < get_distance_from_a_to_b(self.position[0], self.position[1],
                                                                           closest_fish.position[0],
                                                                           closest_fish.position[1]):
                    closest_fish = fish
        if closest_fish is not None:
            self.turn_to_point(closest_fish.position[0], closest_fish.position[1])

    def avoid_collision(self):
        if self.position[0] < 0:
            self.position[0] = 0
            self.desired_direction.x = -self.desired_direction.x

        if self.position[1] < 0:
            self.position[1] = 0
            self.desired_direction.y = -self.desired_direction.y

        if self.position[0] > DISPLAY_WIDTH:
            self.position[0] = DISPLAY_WIDTH
            self.desired_direction.x = -self.desired_direction.x

        if self.position[1] > DISPLAY_HEIGHT:
            self.position[1] = DISPLAY_HEIGHT
            self.desired_direction.y = -self.desired_direction.y

    def turn_to_point(self, target_x: float, target_y: float):
        vector_to_point = Vector(self.position[0], self.position[1], target_x, target_y).normalize()
        self.desired_direction = vector_to_point

    def turn_away_from_point(self, target_x: int, target_y: int):
        vector_to_point = Vector(target_x, target_y, self.position[0], self.position[1]).normalize()
        self.desired_direction = vector_to_point
