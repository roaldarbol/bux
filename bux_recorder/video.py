import multiprocessing as mp
import cv2
import utils
import time

# https://stackoverflow.com/questions/10862532/opencv-and-multiprocessing
# https://www.reddit.com/r/learnpython/comments/62ppgp/opencv_grab_images_from_several_cameras_in/


def cam_loop(cam, queue, mode):
    cap = cv2.VideoCapture(cam)
    # i = 0
    while True:
        ret, frame = cap.read() # Capture frame-by-frame
        if ret == True:
            # i += 1
            cv2.imshow('Cam %d' % cam, frame)
            cv2.waitKey(1)
        # if queue.empty() is not True:
        #     print("finishing")
        #     cap.release()
        #     cv2.destroyAllWindows()
        #     break
