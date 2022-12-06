import multiprocessing as mp
import cv2
import utils
import time
import logging
import datetime as dt
import bux_recorder.logger as logger

# import bux_recorder.gui
# import bux_recorder.gui_video

# https://stackoverflow.com/questions/10862532/opencv-and-multiprocessing
# https://www.reddit.com/r/learnpython/comments/62ppgp/opencv_grab_images_from_several_cameras_in/

# class CamProcess(mp.Process):
#     def __init__(self):

#     def terminate(self):


def cam_preview(cam, queue, **kwargs):

    cam_settings = queue.get()
    cap = cv2.VideoCapture(cam)

    # for name, value in kwargs.items():
    #     print('{0} = {1}'.format(name, value))
    vid_width = cam_settings["res_width"]
    vid_height = cam_settings["res_height"]
    # new_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # new_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_settings["res_height"])
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_settings["res_width"])
    # cap.set(cv2.CAP_PROP_FPS, 9)
    queue.put(cam_settings)

    # Here we can maybe try to change settings in the loop
    set_res_attempt = 0
    # i = 0
    while True:
        ret, frame = cap.read()  # Capture frame-by-frame
        if ret == True:
            # If something new happens in settings, change accordingly
            # i += 1
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # sky = grayFrame[
            #     new_vid_height[0]:new_vid_height[1],
            #     new_vid_width[0]:new_vid_width[1]
            #     ]
            cv2.imshow("Cam %d" % cam, grayFrame)
            cv2.waitKey(1)
            # log.info(f'Frame {cam}, {time}')
            # if set_res_attempt == 0 and cap.get(cv2.CAP_PROP_FRAME_HEIGHT) != vid_height:
            #     # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, vid_height)
            #     # cap.set(cv2.CAP_PROP_FRAME_WIDTH, vid_width)
            #     set_res_attempt = 1 # If it isn't possible to set the new resolution, prevent trying again
            # elif cap.get(cv2.CAP_PROP_FRAME_HEIGHT) == vid_height:
            #     set_res_attempt = 0

        # THIS NEEDS TO GO INTO A GRACEFUL SHUTDOWN METHOD
        # if queue.empty() is not True:
        #     print("finishing")
        #     cap.release()
        #     cv2.destroyAllWindows()
        #     break


def cam_record(cam, queue, path, start_dt, event, **kwargs):

    # Set logger
    log_object = logger.Create_logger(f"Cam-{cam}")
    # log_object.add_stream_handler()
    log_object.add_file_handler(path, start_dt)
    log = logging.getLogger(f"Cam-{cam}")

    cam_settings = queue.get()
    queue.put(cam_settings)
    # queue.put(cam_settings)
    # queue.put(False)
    vid_width = cam_settings["res_width"]
    vid_height = cam_settings["res_height"]
    cap = cv2.VideoCapture(cam)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_settings["res_height"])
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_settings["res_width"])

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    fps = 30
    filetype = "mp4"  # "avi"
    filename = "{}/{}-Cam-{}.{}".format(path, start_dt, cam, filetype)
    # vid_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    # vid_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    out = cv2.VideoWriter(filename, fourcc, fps, (vid_width, vid_height))
    i = 0
    while True:
        # i += 1
        ret, frame = cap.read()  # Capture frame-by-frame
        if ret == True:
            i += 1
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            out.write(frame)
            cv2.imshow("Cam %d" % cam, frame)
            cv2.waitKey(1)
            log.info("Frame %s", i)

        # Check queue
        if event.is_set():
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
