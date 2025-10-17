import cv2
import numpy as np
import time
import math
from precog_ui import config
from precog_ui.config import InputState
from precog_ui.utils.helpers import MathHelper
from precog_ui.ui.components import Button, Panel, Slider, StatsMonitor

class Renderer:
    def __init__(self):
        # Trail history
        self.cursor_trail = []
        self.start_time = time.time()

    def draw_rounded_rect(self, img, pt1, pt2, color, thickness, r, d):
        cv2.rectangle(img, pt1, pt2, color, thickness)

    def _render_background_grid(self, frame, alpha=0.1):
        # Scanlines and Hex/Grid overlay for Minority report feel
        overlay = frame.copy()
        
        # Grid
        step = 40
        for x in range(0, config.FRAME_WIDTH, step):
            cv2.line(overlay, (x, 0), (x, config.FRAME_HEIGHT), config.THEME_HOLO_CYAN, 1)
        for y in range(0, config.FRAME_HEIGHT, step):
            cv2.line(overlay, (0, y), (config.FRAME_WIDTH, y), config.THEME_HOLO_CYAN, 1)
            
        t = time.time() - self.start_time
        scanline_y = int((t * 200) % config.FRAME_HEIGHT)
        cv2.line(overlay, (0, scanline_y), (config.FRAME_WIDTH, scanline_y), config.THEME_HOLO_MAGENTA, 2)
        
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    def render(self, frame, ui_manager, state_machine, cursor_pos, confidence, raw_cursor_pos=None):
        # 1. Apply a subtle Dark Holographic Tint (clearly visible camera)
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (config.FRAME_WIDTH, config.FRAME_HEIGHT), config.THEME_DARK_BG, -1)
        # Keeps camera highly visible while maintaining the dark aesthetic (40% dark, 60% camera)
        cv2.addWeighted(overlay, 0.40, frame, 0.60, 0, frame)
        
        self._render_background_grid(frame, alpha=0.15)
        
        # 2. Render UI Elements (bottom to top based on Z-index)
        elements_sorted = sorted(ui_manager.elements, key=lambda x: x.z_index)
        for el in elements_sorted:
            if isinstance(el, Panel):
                self._render_panel(frame, el)
            elif isinstance(el, Button):
                self._render_button(frame, el)
            elif isinstance(el, Slider):
                self._render_slider(frame, el)
            elif isinstance(el, StatsMonitor):
                self._render_stats_monitor(frame, el)

        # 3. Render Cursor & Trail
        self._render_cursor(frame, state_machine.current_state, cursor_pos)

        # 3.5 Render Raw Landmark (Debug Ghost)
        if raw_cursor_pos is not None:
            cv2.circle(frame, raw_cursor_pos, 4, (100, 100, 100), 1)

        # 4. Render Debug / HUD layer
        self._render_hud(frame, state_machine, confidence)

        return frame

    def _draw_corners(self, frame, x, y, w, h, color, length=15, thickness=2):
        # Top-Left
        cv2.line(frame, (x, y), (x + length, y), color, thickness)
        cv2.line(frame, (x, y), (x, y + length), color, thickness)
        # Top-Right
        cv2.line(frame, (x + w, y), (x + w - length, y), color, thickness)
        cv2.line(frame, (x + w, y), (x + w, y + length), color, thickness)
        # Bottom-Left
        cv2.line(frame, (x, y + h), (x + length, y + h), color, thickness)
        cv2.line(frame, (x, y + h), (x, y + h - length), color, thickness)
        # Bottom-Right
        cv2.line(frame, (x + w, y + h), (x + w - length, y + h), color, thickness)
        cv2.line(frame, (x + w, y + h), (x + w, y + h - length), color, thickness)

    def _render_panel(self, frame, panel: Panel):
        color = config.THEME_HOLO_DARK
        if panel.is_hovered:
            color = (color[0]+15, color[1]+15, color[2]+15)
        
        overlay = frame.copy()
        cv2.rectangle(overlay, (panel.rect.x, panel.rect.y), 
                      (panel.rect.x + panel.rect.w, panel.rect.y + panel.rect.h), 
                      color, -1)
        cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

        # Sci-Fi Corner Borders
        self._draw_corners(frame, panel.rect.x, panel.rect.y, panel.rect.w, panel.rect.h, config.THEME_HOLO_CYAN, 20, 2)
        
        # Faint full border
        cv2.rectangle(frame, (panel.rect.x, panel.rect.y), 
                      (panel.rect.x + panel.rect.w, panel.rect.y + panel.rect.h), 
                      config.THEME_PANEL_BORDER, 1)
        
        # Title Background tab
        cv2.rectangle(frame, (panel.rect.x, panel.rect.y), 
                      (panel.rect.x + panel.rect.w, panel.rect.y + 40), 
                      (40, 40, 50), -1)
        
        cv2.putText(frame, f"// {panel.title}", (panel.rect.x + 10, panel.rect.y + 25), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, config.THEME_HOLO_CYAN, 2)

    def _render_button(self, frame, btn: Button):
        base_color = config.THEME_PANEL_BORDER
        active_color = config.THEME_HOLO_CYAN
        
        r = int(MathHelper.lerp(base_color[0], active_color[0], btn.anim_t))
        g = int(MathHelper.lerp(base_color[1], active_color[1], btn.anim_t))
        b = int(MathHelper.lerp(base_color[2], active_color[2], btn.anim_t))
        color = (b, g, r)
        
        scale = 1.0 - (btn.click_t * 0.05)
        cx, cy = btn.rect.center()
        w = int(btn.rect.w * scale)
        h = int(btn.rect.h * scale)
        x = cx - w // 2
        y = cy - h // 2

        overlay = frame.copy()
        cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)

        border_color = config.THEME_HOLO_CYAN if btn.anim_t > 0.5 else config.THEME_PANEL_BORDER
        cv2.rectangle(frame, (x, y), (x + w, y + h), border_color, 1)
        self._draw_corners(frame, x, y, w, h, border_color, 8, 2)
        
        text_size = cv2.getTextSize(btn.label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
        tx = cx - text_size[0] // 2
        ty = cy + text_size[1] // 2
        
        t_color = config.THEME_HOLO_CYAN if btn.anim_t > 0.5 else config.THEME_TEXT_PRIMARY
        cv2.putText(frame, btn.label, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, 0.5, t_color, 2)

    def _render_slider(self, frame, slider: Slider):
        cx, cy = slider.rect.center()
        track_y = cy
        track_start = slider.rect.x
        track_end = slider.rect.x + slider.rect.w
        
        # Draw dotted track
        for tx in range(track_start, track_end, 10):
            cv2.line(frame, (tx, track_y), (tx + 5, track_y), config.THEME_PANEL_BORDER, 2)
        
        # Draw glowing fill
        fill_end = track_start + int(slider.value * slider.rect.w)
        overlay = frame.copy()
        cv2.line(overlay, (track_start, track_y), (fill_end, track_y), config.THEME_HOLO_MAGENTA, 6)
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)

        # Handle Diamond Shape
        handle_x = fill_end
        handle_color = config.THEME_HOLO_MAGENTA if (slider.is_hovered or slider.is_dragging) else config.THEME_HOLO_CYAN
        
        if slider.is_dragging:
            h_size = 10
            pts = np.array([[handle_x, track_y - h_size], [handle_x + h_size, track_y], 
                            [handle_x, track_y + h_size], [handle_x - h_size, track_y]], np.int32)
            cv2.fillPoly(frame, [pts], config.THEME_HOLO_MAGENTA)
            cv2.polylines(frame, [pts], True, (255,255,255), 2)
        else:
            h_size = 8
            pts = np.array([[handle_x, track_y - h_size], [handle_x + h_size, track_y], 
                            [handle_x, track_y + h_size], [handle_x - h_size, track_y]], np.int32)
            cv2.fillPoly(frame, [pts], config.THEME_DARK_BG)
            cv2.polylines(frame, [pts], True, handle_color, 2)

        # Value Readout Box
        val_str = f"{int(slider.value*100)}%"
        cv2.putText(frame, f"{slider.label}", (track_start, track_y - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, config.THEME_HOLO_CYAN, 1)
        cv2.putText(frame, val_str, (track_end - 40, track_y - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, config.THEME_HOLO_MAGENTA, 1)

    def _render_stats_monitor(self, frame, stats: StatsMonitor):
        cv2.putText(frame, f">> {stats.label}", (stats.rect.x, stats.rect.y + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, config.THEME_HOLO_CYAN, 1)

        bar_w = stats.rect.w - 50
        
        def draw_segmented_bar(name, y_off, color, usage):
            cv2.putText(frame, name, (stats.rect.x, stats.rect.y + y_off + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, config.THEME_TEXT_SECONDARY, 1)
            seg_count = 20
            seg_w = bar_w // seg_count
            active_segs = int((usage / 100.0) * seg_count)
            
            for i in range(seg_count):
                sx = stats.rect.x + 40 + i * seg_w
                sy = stats.rect.y + y_off
                
                c = color if i < active_segs else config.THEME_PANEL_BORDER
                cv2.rectangle(frame, (sx + 1, sy), (sx + seg_w - 2, sy + 12), c, -1)
                
            cv2.putText(frame, f"{usage:04.1f}%", (stats.rect.x + 40 + bar_w + 10, stats.rect.y + y_off + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

        draw_segmented_bar("CPU", 40, config.THEME_HOLO_CYAN, stats.cpu_usage)
        draw_segmented_bar("RAM", 70, config.THEME_HOLO_MAGENTA, stats.ram_usage)

    def _render_cursor(self, frame, state, pos):
        if state == InputState.LOST_TRACKING:
            return

        self.cursor_trail.append(pos)
        if len(self.cursor_trail) > 15:
            self.cursor_trail.pop(0)

        # Cyberpunk Trail
        for i in range(1, len(self.cursor_trail)):
            pt1 = self.cursor_trail[i-1]
            pt2 = self.cursor_trail[i]
            thickness = int(np.interp(i, [0, 15], [1, 4]))
            alpha_line = i / 15.0
            
            overlay = frame.copy()
            cv2.line(overlay, pt1, pt2, config.THEME_NEON_ORANGE, thickness)
            cv2.addWeighted(overlay, alpha_line, frame, 1 - alpha_line, 0, frame)

        # Radar Reticle
        t = time.time() - self.start_time
        angle = t * 3.0 # rotation speed
        
        glow_size = 20
        color = config.THEME_NEON_ORANGE
        if state == InputState.CLICK:
            color = config.THEME_NEON_RED
            glow_size = 12
        elif state == InputState.DRAG:
            color = config.THEME_NEON_GREEN
            glow_size = 18
        elif state == InputState.HOVER:
            color = config.THEME_NEON_BLUE
            glow_size = 25

        cx, cy = pos
        # Inner dot
        cv2.circle(frame, pos, 3, (255, 255, 255), -1)
        
        # Rotating dashed outer circle
        radius = glow_size
        dash_len = math.pi / 4
        for i in range(4):
            start_angle = angle + i * (math.pi / 2)
            end_angle = start_angle + dash_len
            cv2.ellipse(frame, pos, (radius, radius), 0, math.degrees(start_angle), math.degrees(end_angle), color, 2)
            
        # Target bracket crosshairs when hovered or dragging
        if state in [InputState.HOVER, InputState.DRAG]:
            b_size = radius + 8
            cv2.line(frame, (cx - b_size, cy), (cx - b_size + 5, cy), color, 2)
            cv2.line(frame, (cx + b_size, cy), (cx + b_size - 5, cy), color, 2)
            cv2.line(frame, (cx, cy - b_size), (cx, cy - b_size + 5), color, 2)
            cv2.line(frame, (cx, cy + b_size), (cx, cy + b_size - 5), color, 2)

    def _render_hud(self, frame, state_machine, confidence):
        # Top left HUD - Data Readouts
        hud_x, hud_y = 20, 30
        self._draw_corners(frame, hud_x - 5, hud_y - 20, 200, 110, config.THEME_HOLO_CYAN, 10, 1)
        
        cv2.putText(frame, f"SYS.MODE: {state_machine.mode.value}", (hud_x, hud_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, config.THEME_HOLO_CYAN, 1)
        
        state_color = config.THEME_TEXT_PRIMARY
        if state_machine.current_state == InputState.LOST_TRACKING:
            state_color = config.THEME_NEON_RED
            cv2.putText(frame, "WARNING: SENSOR OFFLINE", (hud_x, hud_y + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, state_color, 2)

        cv2.putText(frame, f"OP.STATE: {state_machine.current_state.value}", (hud_x, hud_y + 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, state_color, 1)
        
        conf_str = f"SYNC.LVL: {int(confidence*100)}%"
        cv2.putText(frame, conf_str, (hud_x, hud_y + 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, config.THEME_HOLO_MAGENTA, 1)
