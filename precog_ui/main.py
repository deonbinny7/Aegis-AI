import cv2
import time
import argparse
import psutil

from precog_ui import config
from precog_ui.tracking.hand_tracker import HandTracker
from precog_ui.gestures.gesture_engine import GestureEngine
from precog_ui.actions.action_manager import ActionManager
from precog_ui.state.state_machine import StateMachine
from precog_ui.ui.components import UIManager, Panel, Button, Slider, StatsMonitor
from precog_ui.ui.renderer import Renderer
from precog_ui.utils.physics import PhysicsState

from precog_ui.ui.dashboard import build_dashboard_ui

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--calibrate", action="store_true", help="Start with calibration mode")
    parser.add_argument("--debug", action="store_true", help="Show landmarks and raw overlay")
    args = parser.parse_args()

    # Initialize Modules
    tracker = HandTracker()
    if args.calibrate:
        print("[INIT] Calibration not fully implemented, falling back defaults.")
        
    gesture_engine = GestureEngine()
    action_manager = ActionManager()
    state_machine = StateMachine(action_manager)
    ui_manager = UIManager()
    renderer = Renderer()
    cursor_physics = PhysicsState(config.FRAME_WIDTH // 2, config.FRAME_HEIGHT // 2)

    stats_mon, vol_slide, br_slide = build_dashboard_ui(ui_manager)

    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, config.FPS_TARGET)

    print("[SYSTEM] PreCog Control Center Initialized. Press 'q' to quit.")

    prev_time = time.time()
    last_psutil_fetch = 0.0

    while cap.isOpened():
        success, raw_frame = cap.read()
        if not success:
            continue

        # Flip horizontally for mirror effect
        frame = cv2.flip(raw_frame, 1)
        curr_time = time.time()

        # Update Psutil safely without stalling frame rate (fetch every 1 second)
        if curr_time - last_psutil_fetch > 1.0:
            stats_mon.set_stats(psutil.cpu_percent(), psutil.virtual_memory().percent)
            last_psutil_fetch = curr_time

        # If sliders are dragged, output values
        if vol_slide.is_dragging:
            pass # In a real system you'd call a volume hook here

        # 1. Perception
        tracking_bundle, raw_results = tracker.process(frame)

        # 2. Update Physics Cursor
        if tracking_bundle['detected'] and tracking_bundle['cursor_raw']:
            tx, ty = tracking_bundle['cursor_raw']
            cursor_pos = cursor_physics.update_target(tx, ty)
        else:
            # maintain last position or decay velocity
            cursor_pos = cursor_physics.update_target(cursor_physics.x, cursor_physics.y)

        # 3. Gesture Engine (get state and confidence)
        raw_state, confidence = gesture_engine.analyze(tracking_bundle)

        # 4. State Machine (update interactions)
        state_machine.update(raw_state, cursor_pos, ui_manager)

        # 5. UI Animations Update
        ui_manager.update_animations()

        # 6. Render Dashboard
        raw_cursor = tracking_bundle.get('cursor_actual')
        output_frame = renderer.render(frame, ui_manager, state_machine, cursor_pos, confidence, raw_cursor_pos=raw_cursor)
        
        # Overlay landmarks if debug
        if args.debug:
            tracker.draw_landmarks(output_frame, raw_results)

        # FPS calculation
        fps = 1 / (max(curr_time - prev_time, 0.001))
        prev_time = curr_time
        cv2.putText(output_frame, f"FPS: {int(fps)}", (config.FRAME_WIDTH - 150, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, config.THEME_HOLO_CYAN, 2)

        # Display
        cv2.imshow(config.WINDOW_NAME, output_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
