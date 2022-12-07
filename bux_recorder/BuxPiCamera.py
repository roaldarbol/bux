import multiprocessing as mp
import utils
import time
import logging
import datetime as dt
import bux_recorder.logger as logger
from picamera2 import Picamera2, Preview
from picamera2 import H264Encoder
from picamera2.outputs import FfmpegOutput


class BuxPiCamera:
    def __init__(
        self,
        cam,
        queue,
        path,
        start_dt,
        event_stop,
        event_preview,
        event_record,
        parent=None,
        **kwargs,
    ):
        self.cam = cam
        self.queue = queue
        self.path = path
        self.start_dt = start_dt
        self.event_stop = event_stop
        self.event_preview = event_preview
        self.event_record = event_record
        self.picam2 = picamera2.Picamera2(self.cam)
        self.picam2.start(show_preview=False)

        # VideoWriter
        # self.fourcc = cv2.VideoWriter_fourcc(*'mp4v') # .avi with 'XVID'
        self.encoder = H264Encoder(10000000)
        self.fps = 30
        self.filetype = "mp4"  # "avi"
        self.vid_num = 0
        self.filename = "{}/{}-cam{}-vid{}.{}".format(
            self.path, self.start_dt, self.cam, self.vid_num, self.filetype
        )

        # Begin event loop
        self.run()

    def run(self):
        while True:
            if self.event_preview.is_set():
                self.preview()
            elif self.event_record.is_set():
                self.record()
            elif self.event_stop.is_set():
                self.cap.release()
                break

    def preview(self, **kwargs):

        # Set video settings
        self.cam_settings = self.queue.get()
        self.vid_width = self.cam_settings[self.cam]["res_width"]
        self.vid_height = self.cam_settings[self.cam]["res_height"]
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cam_settings[self.cam]['res_width'])
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cam_settings[self.cam]['res_height'])
        # self.vid_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        # self.vid_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.queue.put(self.cam_settings)

        # Preview loop
        self.picam2.start_preview(Preview.QTGL)
        while True:

            # Check event
            if not self.event_preview.is_set():
                self.picam2.stop_preview()
                break

    def record(self, **kwargs):
        """Recording loop"""
        # Set logger
        self.set_logger()

        # Set video settings
        self.cam_settings = self.queue.get()
        self.vid_width = self.cam_settings[self.cam]["res_width"]
        self.vid_height = self.cam_settings[self.cam]["res_height"]
        self.vid_interval = self.cam_settings[self.cam]["vid_interval"]
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cam_settings[self.cam]["res_width"])
        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT, self.cam_settings[self.cam]["res_height"]
        )
        self.vid_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.vid_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.queue.put(self.cam_settings)
        self.log.info("Settings:", self.cam_settings)

        # Create output file
        self.out = FfmpegOutput(self.filename)
        # self.out = cv2.VideoWriter(
        #     self.filename,
        #     self.fourcc,
        #     self.fps,
        #     (self.vid_width, self.vid_height)
        #     )

        i = 0
        t0 = time.time()
        print("Beginning recording")

        self.cap.start_recording(self.encoder, self.out)
        while True:
            ret, frame = self.cap.read()  # Capture frame-by-frame
            if ret == True:
                i += 1
                grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.out.write(frame)
                # cv2.imshow('Cam %d' % self.cam, frame)
                cv2.waitKey(1)
                self.log.info("Frame %s", i)

            # Check time (in minutes) - start new video
            t1 = time.time()
            t_diff = (t1 - t0) / 60
            if t_diff >= self.vid_interval:
                self.out.release()
                cv2.waitKey(1)
                self.vid_num += 1
                self.filename = "{}/{}-cam{}-vid{}.{}".format(
                    self.path, self.start_dt, self.cam, self.vid_num, self.filetype
                )
                print("Starting new recording")
                self.out = cv2.VideoWriter(
                    self.filename,
                    self.fourcc,
                    self.fps,
                    (self.vid_width, self.vid_height),
                )
                i = 0
                t0 = time.time()

            # Check queue
            if not self.event_record.is_set():
                self.out.release()
                cv2.waitKey(1)
                cv2.destroyAllWindows()
                cv2.waitKey(1)
                break

    def set_logger(self):

        # Set logger
        log_object = logger.Create_logger(f"Cam-{self.cam}")
        log_object.add_file_handler(self.path, self.start_dt)
        self.log = logging.getLogger(f"Cam-{self.cam}")


if __name__ == "__main__":
    cam = 0
    queue = mp.Queue()
    path = "/Users/roaldarbol/Desktop"
    start_dt = dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    vid_interval_time = 5
    cam_settings = {}
    cam_settings["res_width"] = 800
    cam_settings["res_height"] = 600
    event_stop = mp.Event()
    event_preview = mp.Event()
    event_record = mp.Event()

    queue.put(cam_settings)

    # Spawn processes
    process = mp.Process(
        target=BuxPiCamera,
        args=[cam, queue, path, start_dt, event_stop, event_preview, event_record],
    )

    # Start processes
    process.start()
    event_record.set()
    time.sleep(3)
    event_stop.set()
    process.join()
