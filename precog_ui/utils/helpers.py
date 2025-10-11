import math

class MathHelper:
    @staticmethod
    def distance(p1, p2):
        return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

    @staticmethod
    def clamp(value, min_val, max_val):
        return max(min_val, min(value, max_val))

    @staticmethod
    def lerp(a, b, t):
        return a + (b - a) * MathHelper.clamp(t, 0.0, 1.0)
    
    @staticmethod
    def ease_out_expo(t):
        return 1.0 if t == 1.0 else 1.0 - math.pow(2.0, -10.0 * t)

class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        px, py = point
        return self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h

    def center(self):
        return (self.x + self.w // 2, self.y + self.h // 2)

    def intersects(self, other):
        return not (self.x + self.w < other.x or
                    self.x > other.x + other.w or
                    self.y + self.h < other.y or
                    self.y > other.y + other.h)
class LowPassFilter:
    def __init__(self, alpha):
        self.alpha = alpha
        self.last_val = None

    def filter(self, value):
        if self.last_val is None:
            res = value
        else:
            res = self.alpha * value + (1.0 - self.alpha) * self.last_val
        self.last_val = res
        return res

class OneEuroFilter:
    def __init__(self, freq, min_cutoff=1.0, beta=0.0, d_cutoff=1.0):
        self.freq = freq
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.d_cutoff = d_cutoff
        self.x_filt = LowPassFilter(self._alpha(min_cutoff))
        self.dx_filt = LowPassFilter(self._alpha(d_cutoff))
        self.last_x = None

    def _alpha(self, cutoff):
        te = 1.0 / self.freq
        tau = 1.0 / (2.0 * math.pi * cutoff)
        return 1.0 / (1.0 + tau / te)

    def filter(self, x):
        dx = 0.0 if self.last_x is None else (x - self.last_x) * self.freq
        self.last_x = x
        edx = self.dx_filt.filter(dx)
        cutoff = self.min_cutoff + self.beta * abs(edx)
        self.x_filt.alpha = self._alpha(cutoff)
        return self.x_filt.filter(x)
