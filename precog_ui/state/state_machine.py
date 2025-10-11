from precog_ui.config import InputState, SystemMode

class StateMachine:
    def __init__(self, action_manager):
        self.current_state = InputState.LOST_TRACKING
        self.mode = SystemMode.NAVIGATION
        self.action_manager = action_manager
        
        # Keep track of active entity being dragged
        self.active_drag_item = None

    def update(self, new_raw_state, cursor_pos, ui_manager):
        previous_state = self.current_state
        self.current_state = new_raw_state

        if self.current_state == InputState.LOST_TRACKING:
            # Drop any dragged item safely
            if self.active_drag_item:
                self.active_drag_item.on_drop()
                self.active_drag_item = None
            return

        # UI Priority evaluation
        hovered_item = ui_manager.get_top_item_at(cursor_pos)

        # Broadcast Hover
        ui_manager.clear_hovers()
        if hovered_item and self.current_state != InputState.DRAG:
            hovered_item.on_hover()

        # Handle Mode-specific transitions or Actions
        if self.current_state == InputState.CLICK and previous_state != InputState.CLICK:
            if hovered_item:
                hovered_item.on_click()
                if hasattr(hovered_item, 'action_id') and hovered_item.action_id:
                    self.action_manager.execute(hovered_item.action_id, self.mode)

        elif self.current_state == InputState.DRAG:
            if previous_state != InputState.DRAG and hovered_item:
                self.active_drag_item = hovered_item
                self.active_drag_item.on_drag_start(cursor_pos)
            
            if self.active_drag_item:
                self.active_drag_item.on_drag(cursor_pos)
        
        elif previous_state == InputState.DRAG and self.current_state != InputState.DRAG:
            # Finished dragging
            if self.active_drag_item:
                self.active_drag_item.on_drop()
                self.active_drag_item = None

        # Swipe handling depending on mode
        if self.current_state in [InputState.SWIPE_LEFT, InputState.SWIPE_RIGHT] and previous_state not in [InputState.SWIPE_LEFT, InputState.SWIPE_RIGHT]:
            self._handle_swipe(self.current_state, ui_manager)

    def _handle_swipe(self, swipe_state, ui_manager):
        direction = 1 if swipe_state == InputState.SWIPE_LEFT else -1
        if self.mode == SystemMode.NAVIGATION:
            # Switch panels
            ui_manager.switch_panel(direction)
            print(f"[STATE] Swiped in mode NAV: switching panel direc {direction}")
        elif self.mode == SystemMode.CONTROL:
            # e.g., swipe to change volume
            print(f"[STATE] Swiped in mode CONTROL")
            if direction > 0:
                self.action_manager.execute("btn_vol_up", self.mode)
            else:
                self.action_manager.execute("btn_vol_down", self.mode)
