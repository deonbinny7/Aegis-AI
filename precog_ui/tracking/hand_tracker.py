import cv2
import mediapipe as mp
import numpy as np
from precog_ui import config
from precog_ui.utils.helpers import MathHelper, OneEuroFilter

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=config.MP_MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MP_MIN_TRACKING_CONFIDENCE
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # User Calibration Area (normalized coords)
        self.calibrated = False
        self.interaction_box = {
            'x_min': 0.2,
            'x_max': 0.8,
            'y_min': 0.2,
            'y_max': 0.8
        }
        
        # Stateful adaptive smoothing (One-Euro Filter)
        # freq = FPS_TARGET, min_cutoff=1.0, beta=0.01, d_cutoff=1.0
        self.filter_x = OneEuroFilter(config.FPS_TARGET, min_cutoff=0.5, beta=0.01)
        self.filter_y = OneEuroFilter(config.FPS_TARGET, min_cutoff=0.5, beta=0.01)

    def calculate_distance(self, pt1, pt2):
        return MathHelper.distance((pt1.x, pt1.y), (pt2.x, pt2.y))

    def map_to_screen(self, norm_x, norm_y):
        # Maps purely 1:1 with the camera frame so the cursor is exactly on the finger
        screen_x = int(norm_x * config.FRAME_WIDTH)
        screen_y = int(norm_y * config.FRAME_HEIGHT)
        return screen_x, screen_y

    def process(self, frame):
        # Convert BGR to RGB for mediapipe
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = self.hands.process(img_rgb)
        
        bundle = {
            'detected': False,
            'landmarks': None,
            'cursor_raw': None,   # (x, y) pixels mapped to screen
            'pinch_dist': 0.0,
            'hand_center': None
        }

        if results.multi_hand_landmarks:
            hand_lms = results.multi_hand_landmarks[0] # taking first hand
            bundle['detected'] = True
            bundle['landmarks'] = hand_lms

            # Extract key landmarks
            index_tip = hand_lms.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_lms.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
            wrist = hand_lms.landmark[self.mp_hands.HandLandmark.WRIST]
            middle_mcp = hand_lms.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]

            # Cursor position (index tip) normalized to local space
            raw_x, raw_y = index_tip.x, index_tip.y

            # Apply stateful adaptive smoothing
            smooth_x = self.filter_x.filter(raw_x)
            smooth_y = self.filter_y.filter(raw_y)

            bundle['cursor_raw'] = self.map_to_screen(smooth_x, smooth_y)
            bundle['cursor_actual'] = self.map_to_screen(raw_x, raw_y) # For debug ghost
            
            # Hand center for swipe tracking
            bundle['hand_center'] = self.map_to_screen(middle_mcp.x, middle_mcp.y)

            # Calculate pinch distance (normalized 3D distance between thumb tip and index tip)
            bundle['pinch_dist'] = self.calculate_distance(index_tip, thumb_tip)
            
        return bundle, results

    def draw_landmarks(self, frame, results):
        if results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)
