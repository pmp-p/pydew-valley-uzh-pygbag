import time

import pygame


class SceneAnimation:
    def __init__(self, target_points, speeds=None, pauses=None):
        self.target_points = target_points
        self.speeds = speeds if speeds else [200] * (len(target_points) - 1)
        self.pauses = pauses if pauses else [0] * len(target_points)
        self.current_index = 0
        self.current_pos = pygame.Vector2(target_points[0])
        self.is_finished = False
        self.pause_start_time = None

    def get_current_position(self):
        return self.current_pos

    def reset(self):
        self.current_index = 0
        self.current_pos = pygame.Vector2(self.target_points[0])
        self.is_finished = False
        self.pause_start_time = None

    def pause_active(self):
        return self.pause_start_time is not None

    def is_remaining_pause_time(self):
        elapsed_pause_time = time.time() - self.pause_start_time
        pause_duration = self.pauses[self.current_index]
        return elapsed_pause_time < pause_duration

    def reset_pause(self):
        self.pause_start_time = None
        self.current_index += 1

    def move_towards_target(self, dt):
        target = pygame.Vector2(self.target_points[self.current_index])
        direction = target - self.current_pos
        distance_to_target = direction.length()

        if distance_to_target <= self.speeds[self.current_index - 1] * dt:
            self.current_pos = target
            self.pause_start_time = time.time()
        else:
            direction = direction.normalize()
            self.current_pos += direction * self.speeds[self.current_index - 1] * dt

    def has_more_targets(self):
        return self.current_index < len(self.target_points)

    def animate(self, dt):
        if self.is_finished:
            return

        if self.pause_active():
            if self.is_remaining_pause_time():
                return
            self.reset_pause()

        if self.has_more_targets():
            self.move_towards_target(dt)
        else:
            self.is_finished = True

    def update(self, dt):
        self.animate(dt)
