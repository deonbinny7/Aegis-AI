import time
from precog_ui.utils.helpers import Rect, MathHelper
from precog_ui import config

class UIElement:
    def __init__(self, obj_id, x, y, w, h, z_index=0):
        self.id = obj_id
        self.rect = Rect(x, y, w, h)
        self.z_index = z_index
        self.is_hovered = False
        
        # Animation state
        self.anim_t = 0.0
        self.last_anim_time = time.time()
        
    def on_hover(self):
        self.is_hovered = True

    def clear_hover(self):
        self.is_hovered = False

    def update_anim(self):
        now = time.time()
        dt = now - self.last_anim_time
        self.last_anim_time = now
        
        if self.is_hovered:
            self.anim_t = MathHelper.clamp(self.anim_t + dt * 5.0, 0.0, 1.0)
        else:
            self.anim_t = MathHelper.clamp(self.anim_t - dt * 5.0, 0.0, 1.0)

    def on_click(self):
        pass

    def on_drag_start(self, cursor_pos):
        pass

    def on_drag(self, cursor_pos):
        pass

    def on_drop(self):
        pass

class Button(UIElement):
    def __init__(self, obj_id, x, y, w, h, label, action_id=None):
        super().__init__(obj_id, x, y, w, h, z_index=config.UI_Z_INDEX_BUTTONS)
        self.label = label
        self.action_id = action_id
        self.click_t = 0.0

    def on_click(self):
        # Trigger click animation
        self.click_t = 1.0

    def update_anim(self):
        super().update_anim()
        now = time.time()
        dt = now - self.last_anim_time # Note: last_anim_time was updated in super
        if self.click_t > 0:
            self.click_t = MathHelper.clamp(self.click_t - dt * 2.0, 0.0, 1.0)

class Panel(UIElement):
    def __init__(self, obj_id, x, y, w, h, title):
        super().__init__(obj_id, x, y, w, h, z_index=config.UI_Z_INDEX_PANELS)
        self.title = title
        self.items = []
        
        # Dragging state
        self.is_dragging = False
        self.drag_offset = (0, 0)

    def add_element(self, element: UIElement):
        self.items.append(element)

    def on_drag_start(self, cursor_pos):
        self.is_dragging = True
        self.drag_offset = (self.rect.x - cursor_pos[0], self.rect.y - cursor_pos[1])

    def on_drag(self, cursor_pos):
        if self.is_dragging:
            new_x = cursor_pos[0] + self.drag_offset[0]
            new_y = cursor_pos[1] + self.drag_offset[1]
            dx = new_x - self.rect.x
            dy = new_y - self.rect.y
            
            self.rect.x = new_x
            self.rect.y = new_y
            
            # Move children
            for child in self.items:
                child.rect.x += dx
                child.rect.y += dy

    def on_drop(self):
        self.is_dragging = False

class Slider(UIElement):
    def __init__(self, obj_id, x, y, w, h, label, action_id=None, initial_val=0.5):
        super().__init__(obj_id, x, y, w, h, z_index=config.UI_Z_INDEX_BUTTONS)
        self.label = label
        self.action_id = action_id
        self.value = initial_val  # 0.0 to 1.0
        self.target_value = initial_val
        self.is_dragging = False

    def update_anim(self):
        super().update_anim()
        # Smooth interpolation to target value for fluid motion
        self.value += (self.target_value - self.value) * 0.3
    
    def on_drag_start(self, cursor_pos):
        self.is_dragging = True
        self._update_value_from_pos(cursor_pos)

    def on_drag(self, cursor_pos):
        if self.is_dragging:
            self._update_value_from_pos(cursor_pos)

    def on_drop(self):
        self.is_dragging = False

    def _update_value_from_pos(self, cursor_pos):
        cx, cy = cursor_pos
        # x-axis value mapping
        rx = self.rect.x
        rw = self.rect.w
        normalized = (cx - rx) / rw
        self.target_value = MathHelper.clamp(normalized, 0.0, 1.0)

class StatsMonitor(UIElement):
    def __init__(self, obj_id, x, y, w, h, label):
        super().__init__(obj_id, x, y, w, h, z_index=config.UI_Z_INDEX_BUTTONS)
        self.label = label
        self.cpu_usage = 0.0
        self.ram_usage = 0.0

    def set_stats(self, cpu, ram):
        self.cpu_usage = cpu
        self.ram_usage = ram


class UIManager:
    def __init__(self):
        self.elements = []
        self.active_panel_idx = 0
        self.panels = []

    def get_top_item_at(self, pos):
        # Return element with highest z-index at pos
        hits = []
        for el in self.elements:
            if el.rect.contains(pos):
                hits.append(el)
        
        if not hits:
            return None
        
        hits.sort(key=lambda x: x.z_index, reverse=True)
        return hits[0]

    def clear_hovers(self):
        for el in self.elements:
            el.clear_hover()

    def update_animations(self):
        for el in self.elements:
            el.update_anim()

    def add_panel(self, panel: Panel):
        self.panels.append(panel)
        if len(self.panels) - 1 == self.active_panel_idx:
            self._register_panel(panel)

    def _register_panel(self, panel: Panel):
        self.elements.clear()
        self.elements.append(panel)
        for child in panel.items:
            self.elements.append(child)

    def switch_panel(self, direction):
        if not self.panels:
            return
        self.active_panel_idx = (self.active_panel_idx + direction) % len(self.panels)
        self._register_panel(self.panels[self.active_panel_idx])
