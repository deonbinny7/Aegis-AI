from enum import Enum

# Screen / Camera Configuration
CAMERA_INDEX = 0
WINDOW_NAME = "PreCog UI Prototype"
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FPS_TARGET = 30

# MediaPipe Configuration
MP_MIN_DETECTION_CONFIDENCE = 0.7
MP_MIN_TRACKING_CONFIDENCE = 0.7

# Physics & Smooting
CURSOR_MASS = 1.0
CURSOR_DAMPING = 0.95  # Slightly higher for more stability
CURSOR_MAX_VELOCITY = 150.0
SMOOTHING_EMA_ALPHA = 0.4 # Higher = more responsive, lower = more stable (0.1 - 0.5)


# Gestures & Interaction Constants
PINCH_THRESHOLD = 0.05 # Normalized distance between thumb and index
SWIPE_VELOCITY_THRESHOLD = 200 # pixels per second roughly
CLICK_CONFIRMATION_TIME = 0.150 # seconds (150ms)
COOLDOWN_ACTION = 1.0 # seconds before same action can trigger again
LOST_TRACKING_MSEC_TIMEOUT = 500

# UI Priorities and Geometry
UI_Z_INDEX_PANELS = 10
UI_Z_INDEX_BUTTONS = 20

# Colors (BGR for OpenCV)
THEME_DARK_BG = (15, 15, 20)
THEME_PANEL_BG = (30, 30, 40)
THEME_PANEL_BORDER = (50, 50, 70)
THEME_NEON_BLUE = (255, 100, 0)
THEME_NEON_GREEN = (50, 255, 50)
THEME_NEON_RED = (50, 50, 255)
THEME_NEON_ORANGE = (0, 140, 255)
THEME_HOLO_CYAN = (255, 230, 0)
THEME_HOLO_MAGENTA = (255, 0, 255)
THEME_HOLO_DARK = (20, 25, 25)
THEME_TEXT_PRIMARY = (240, 240, 240)
THEME_TEXT_SECONDARY = (150, 150, 150)

class SystemMode(Enum):
    NAVIGATION = "NAVIGATION"
    CONTROL = "CONTROL"
    EDIT = "EDIT"

class InputState(Enum):
    IDLE = "IDLE"
    HOVER = "HOVER"
    CLICK = "CLICK"
    DRAG = "DRAG"
    SWIPE_LEFT = "SWIPE_LEFT"
    SWIPE_RIGHT = "SWIPE_RIGHT"
    LOST_TRACKING = "LOST_TRACKING"
