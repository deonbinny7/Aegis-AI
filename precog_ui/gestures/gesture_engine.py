import time
import numpy as np
from collections import deque
from precog_ui import config
from precog_ui.config import InputState

class GestureEngine:
    def __init__(self):
        # Buffer for stabilizing state
        self.state_buffer = deque(maxlen=7)
        self.center_history = deque(maxlen=5)
        self.last_click_start = 0
        self.click_confirmed = False
        
        # Swipe tracking
        self.last_swipe_time = 0
        self.swipe_cooldown = config.COOLDOWN_ACTION

    def analyze(self, tracking_bundle):
        if not tracking_bundle['detected']:
            self.state_buffer.clear()
            self.center_history.clear()
            return InputState.LOST_TRACKING, 0.0

        pinch_dist = tracking_bundle['pinch_dist']
        current_center = tracking_bundle['hand_center']
        self.center_history.append(current_center)

        confidence = self._calculate_confidence()
        
        # Determine raw instantaneous state
        raw_state = InputState.IDLE

        # 1. Check for Swipe
        if self._check_swipe():
            # swipe takes precedence but we need to know direction
            dx = current_center[0] - self.center_history[0][0]
            if dx > 0:
                raw_state = InputState.SWIPE_RIGHT
            else:
                raw_state = InputState.SWIPE_LEFT
            self.last_swipe_time = time.time()
        
        # 2. Check for Pinch / Click / Drag
        elif pinch_dist < config.PINCH_THRESHOLD:
            # We are pinching. Are we moving?
            if self._is_moving():
                raw_state = InputState.DRAG
            else:
                raw_state = InputState.CLICK
        else:
            raw_state = InputState.HOVER # Default actively tracked state is hover ready to interact

        self.state_buffer.append(raw_state)

        # Stabilize state
        stable_state = self._stabilize_state()

        # Handle Click Confirmation Window
        if stable_state == InputState.CLICK:
            if not self.click_confirmed:
                if self.last_click_start == 0:
                    self.last_click_start = time.time()
                    stable_state = InputState.HOVER # Mask as hover until confirmed
                elif time.time() - self.last_click_start > config.CLICK_CONFIRMATION_TIME:
                    self.click_confirmed = True
                else:
                    stable_state = InputState.HOVER # Still confirming
        else:
            self.last_click_start = 0
            self.click_confirmed = False

        # Apply confidence threshold
        if confidence < 0.3 and stable_state not in [InputState.IDLE, InputState.HOVER]:
            stable_state = InputState.HOVER # Downgrade if low confidence

        return stable_state, confidence

    def _is_moving(self):
        if len(self.center_history) < 2:
            return False
        dx = self.center_history[-1][0] - self.center_history[0][0]
        dy = self.center_history[-1][1] - self.center_history[0][1]
        dist = np.sqrt(dx**2 + dy**2)
        return dist > 15 # small threshold for dragging

    def _check_swipe(self):
        if time.time() - self.last_swipe_time < self.swipe_cooldown:
            return False
        if len(self.center_history) < 5:
            return False
        
        # Calculate velocity over the buffer
        dx = self.center_history[-1][0] - self.center_history[0][0]
        dy = self.center_history[-1][1] - self.center_history[0][1]
        
        # Assuming 30fps, 5 frames is ~0.16s
        # Velocity = pixels / second
        vx = abs(dx) / 0.16
        
        return vx > config.SWIPE_VELOCITY_THRESHOLD and abs(dx) > abs(dy) * 2

    def _stabilize_state(self):
        if not self.state_buffer:
            return InputState.IDLE
        
        # Return most common state in buffer (mode)
        states = list(self.state_buffer)
        return max(set(states), key=states.count)

    def _calculate_confidence(self):
        # Confidence based on state stability
        if not self.state_buffer:
            return 0.0
        
        recent_states = list(self.state_buffer)
        most_common = max(set(recent_states), key=recent_states.count)
        stability_score = recent_states.count(most_common) / len(recent_states)

        # Motion consistency could also be factored in (e.g. smooth velocity vs jitter)
        return stability_score
