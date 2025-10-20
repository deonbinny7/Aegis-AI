from precog_ui.ui.components import Panel, Button, Slider, StatsMonitor

def build_dashboard_ui(ui_manager):
    # Panel 1: Stats & Controls
    p1 = Panel("panel_main", 50, 100, 350, 450, "SYSTEM DIAGNOSTICS")
    
    stats = StatsMonitor("sys_stats", 70, 150, 310, 100, "RESOURCE MONITOR")
    p1.add_element(stats)
    
    btn1 = Button("btn_calc", 70, 270, 310, 50, "Launch Calculator", action_id="btn_calc")
    btn2 = Button("btn_notepad", 70, 330, 310, 50, "Launch Notepad", action_id="btn_notepad")
    p1.add_element(btn1)
    p1.add_element(btn2)
    
    ui_manager.add_panel(p1)

    # Panel 2: Media & Hardware
    p2 = Panel("panel_media", 50, 100, 350, 450, "MEDIA & HARDWARE")
    
    slider_vol = Slider("slide_vol", 70, 150, 310, 20, "VOLUME", initial_val=0.5)
    slider_br = Slider("slide_br", 70, 220, 310, 20, "BRIGHTNESS", initial_val=0.8)
    p2.add_element(slider_vol)
    p2.add_element(slider_br)
    
    btn_prev = Button("btn_prev", 70, 280, 90, 50, "<<", action_id="btn_media_prev")
    btn_play = Button("btn_play", 180, 280, 90, 50, "PLAY", action_id="btn_media_play")
    btn_next = Button("btn_next", 290, 280, 90, 50, ">>", action_id="btn_media_next")
    
    p2.add_element(btn_prev)
    p2.add_element(btn_play)
    p2.add_element(btn_next)
    
    ui_manager.add_panel(p2)
    
    return stats, slider_vol, slider_br
