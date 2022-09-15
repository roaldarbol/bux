import multiprocessing as mp
import cv2
import utils
import time

# https://stackoverflow.com/questions/10862532/opencv-and-multiprocessing
# https://www.reddit.com/r/learnpython/comments/62ppgp/opencv_grab_images_from_several_cameras_in/

# class CamProcess(mp.Process):
#     def __init__(self):

#     def terminate(self):


def cam_preview(cam, queue):
    cap = cv2.VideoCapture(cam)
    while True:
        ret, frame = cap.read() # Capture frame-by-frame
        if ret == True:
            # i += 1
            cv2.imshow('Cam %d' % cam, frame)
            cv2.waitKey(1)
            
        # THIS NEEDS TO GO INTO A GRACEFUL SHUTDOWN METHOD
        # if queue.empty() is not True:
        #     print("finishing")
        #     cap.release()
        #     cv2.destroyAllWindows()
        #     break

def cam_record(cam, queue, filename):
    cap = cv2.VideoCapture(cam)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 20.0
    filetype = "avi"
    filename = "{}-cam{}.{}".format(filename, cam, filetype)
    vid_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    vid_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    out = cv2.VideoWriter(filename, fourcc, fps, (vid_width, vid_height))
    # i = 0
    while True:
        ret, frame = cap.read() # Capture frame-by-frame
        if ret == True:
            # i += 1
            out.write(frame)
            cv2.imshow('Cam %d' % cam, frame)
            cv2.waitKey(1)
