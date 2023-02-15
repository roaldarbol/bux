def select_camera(self, cam):
    if not self.cams_selected[cam]:
        self.cams_selected[cam] = True
        self.dropdown_camera[cam].config(state="disabled")
        self.button_open_camera[cam].config(text=self.labels["t_cam_deselect"])
        self.log.info("Camera %s selected", cam)
    elif self.cams_selected[cam]:
        self.cams_selected[cam] = False
        self.dropdown_camera[cam].config(state="readonly")
        self.button_open_camera[cam].config(text=self.labels["t_cam_select"])
        self.log.info("Camera %s deselected", cam)
    if any(self.cams_selected.values()):
        self.button_activate.config(state="normal")
    else:
        self.button_activate.config(state="disabled")


def activate_all_cameras(self):
    """Toggles Preview Start/Stop state"""

    if self.active == False:  # otherwise it starts
        for cam in self.cams_selected:
            self.button_open_camera[cam].config(state="disabled")
        self.button_activate.config(text=self.labels["t_cam_deactivate"], bg="red")
        self.button_preview.config(state="normal", bg="green")
        if self.parent == None:
            self.button_record.config(state="normal", bg="green")

        ### MP IMPLEMENTATION
        self.processes = {}
        self.cams_to_open = {
            k: v for k, v in enumerate(self.cams_selected.values()) if v == True
        }

        # Spawn processes
        self.start_dt = dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        for cam in self.cams_to_open:
            self.processes[cam] = mp.Process(
                target=cameraprocess.CameraProcess,
                args=[
                    cam,
                    self.cam_queue,
                    self.path,
                    self.start_dt,
                    self.event_stop,
                    self.event_preview,
                    self.event_record,
                ],
            )

        # Start processes
        print(self.processes)
        for p in self.processes:
            self.processes[p].start()
            self.log.info("Process %s started" % p)

    if self.active == True:
        self.event_stop.set()
        for p in self.processes:
            self.processes[p].join()
        # cv2.destroyAllWindows() # Just needs any input, though it's not using it here...
        for cam in self.cams_selected:
            self.button_open_camera[cam].config(state="normal")
        self.button_activate.config(text=self.labels["t_cam_activate"], bg="green")
        self.button_preview.config(state="disable", bg="green")
        if self.parent == None:
            self.button_record.config(state="disable", bg="green")
        self.event_stop.clear()
        # self.button_start.config(state="normal")

    self.active = not self.active


def toggle_preview(self):
    """Toggles Preview Start/Stop state"""
    if self.preview_running == False:  # otherwise it starts

        # Add settings
        for cam in self.cams_to_open:
            res = self.dropdown_resolution[cam].get()
            res = res.split(",")
            res = [int(n) for n in res]
            self.cam_settings[cam]["res_width"] = res[0]
            self.cam_settings[cam]["res_height"] = res[1]
            self.cam_queue.put(self.cam_settings)

        # Set buttons
        self.button_preview.config(text=self.labels["t_preview_stop"], bg="red")
        self.button_activate.config(state="disable")
        if self.parent is not None:
            self.parent.button_record.config(state="disable")

        # Begin preview
        self.event_preview.set()

    if self.preview_running == True:  # if the experiment is running, it stops
        for cam in self.cams_to_open:
            temp_settings = self.cam_queue.get()
            self.cam_settings[cam] = temp_settings[cam]
        self.event_preview.clear()
        self.button_preview.config(text=self.labels["t_preview"], bg="green")
        self.button_activate.config(state="normal")
        if self.parent is not None:
            self.parent.button_record.config(state="normal")

    self.preview_running = not self.preview_running
    # print(self.cam_queue.get('foo'))


def toggle_record(self):
    """Toggles Preview Start/Stop state"""
    if self.record_running == False:  # otherwise it starts

        # Add settings
        for cam in self.cams_to_open:
            res = self.dropdown_resolution[cam].get()
            res = res.split(",")
            res = [int(n) for n in res]
            self.cam_settings[cam]["res_width"] = res[0]
            self.cam_settings[cam]["res_height"] = res[1]
            self.cam_settings[cam]["vid_interval"] = int(self.spinbox_min[cam].get())
            self.cam_queue.put(self.cam_settings)

        # Set buttons
        self.button_record.config(text=self.labels["t_stop"], bg="red")
        self.button_activate.config(state="disable")
        self.event_record.set()

    if self.record_running == True:  # if the experiment is running, it stops
        for cam in self.cams_to_open:
            temp_settings = self.cam_queue.get()
            self.cam_settings[cam] = temp_settings[cam]
        self.event_record.clear()
        self.button_record.config(text=self.labels["t_start"], bg="green")
        self.button_activate.config(state="normal")

    self.record_running = not self.record_running
