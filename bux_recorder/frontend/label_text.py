from collections import defaultdict


def create_labels():
    labels = defaultdict(list)

    labels["t_dir_choose"] = ["Select destination", "Directory chosen"]
    labels["t_dir_choose_current"] = labels["t_dir_choose"][0]
    labels["t_update"] = "\u27F3"
    labels["t_cam"] = "Cameras"
    labels["t_cam_choose"] = "Choose camera"
    labels["t_cam_select"] = "Select camera"
    labels["t_cam_deselect"] = "Deselect camera"
    labels["t_cam_activate"] = "Activate"
    labels["t_cam_deactivate"] = "Deactivate"
    labels["t_serial_choose"] = "Choose serial"
    labels["t_serial"] = "Microcontrollers"
    labels["t_serial_open"] = "Open serial"
    labels["t_serial_close"] = "Close serial"
    labels["t_serial_send"] = "Send to serial"
    labels["t_serial_interrupt"] = "Interrupt serial"
    labels["t_script_choose"] = "Choose script"
    labels["t_cam_resolution"] = "Choose resolution"
    labels["t_settings_choose"] = ["Select settings", "Settings selected"]
    labels["t_settings_choose_current"] = [
        labels["t_settings_choose"][0],
        labels["t_settings_choose"][0],
    ]
    labels["t_settings_load"] = "Load settings"
    labels["t_preview"] = "Preview"
    labels["t_preview_stop"] = "Stop preview"
    labels["t_start"] = "Start recording"
    labels["t_stop"] = "Stop recording"
    labels["t_quit"] = "Do you want to quit Bux?"

    return labels
