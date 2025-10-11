import time
from precog_ui.utils.helpers import MathHelper
from precog_ui import config

class PhysicsState:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.last_update = time.time()

    def update_target(self, target_x, target_y):
        now = time.time()
        dt = now - self.last_update
        if dt <= 0:
            return int(self.x), int(self.y)
        self.last_update = now

        # Switch to a more stable Exponential Smoothing (Lerp) follow
        # This is MUCH more stable than a spring-mass-damper for 2D pointers
        # and prevents the "scribble" zigzag oscillation.
        follow_speed = 15.0 # pixels per second roughly, adjusted by dt
        alpha = MathHelper.clamp(dt * follow_speed, 0.0, 1.0)
        
        self.x = MathHelper.lerp(self.x, target_x, alpha)
        self.y = MathHelper.lerp(self.y, target_y, alpha)

        return int(self.x), int(self.y)

    def force_position(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.last_update = time.time()
