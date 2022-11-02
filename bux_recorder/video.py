import multiprocessing as mp
import cv2
import utils
import time

# https://stackoverflow.com/questions/10862532/opencv-and-multiprocessing
# https://www.reddit.com/r/learnpython/comments/62ppgp/opencv_grab_images_from_several_cameras_in/

# class CamProcess(mp.Process):
#     def __init__(self):

#     def terminate(self):



def cam_preview(cam, queue, **kwargs):
    cap = cv2.VideoCapture(cam)

    for name, value in kwargs.items():
        print('{0} = {1}'.format(name, value))

    vid_height = 600
    vid_width = 800

    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, vid_height)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, vid_width)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 10)
    # vid_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # vid_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    print("hi")
    print(vid_width, vid_height)
    print(
        cap.get(cv2.CAP_PROP_FRAME_WIDTH), 
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )
    # print(vid_width/2, vid_height/2)
    # new_vid_height = [
    #     int(vid_height/2 - vid_height/4),
    #     int(vid_height/2 + vid_height/4)
    # ]
    # new_vid_width = [
    #     int(vid_width/2 - vid_width/4),
    #     int(vid_width/2 + vid_width/4)
    # ]
    # print(new_vid_height, new_vid_width)
    # cap.set(cv2.CAP_PROP_EXPOSURE, -8.0)
    # Here we can maybe try to change settings in the loop
    set_res_attempt = 0
    while True:
        ret, frame = cap.read() # Capture frame-by-frame
        if ret == True:
            # If something new happens in settings, change accordingly
            # i += 1
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # sky = grayFrame[
            #     new_vid_height[0]:new_vid_height[1],
            #     new_vid_width[0]:new_vid_width[1]
            #     ]
            cv2.imshow('Cam %d' % cam, grayFrame)
            cv2.waitKey(1)
            if set_res_attempt == 0 and cap.get(cv2.CAP_PROP_FRAME_HEIGHT) != vid_height:
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, vid_height)
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, vid_width)
                set_res_attempt = 1 # If it isn't possible to set the new resolution, prevent trying again
            elif cap.get(cv2.CAP_PROP_FRAME_HEIGHT) == vid_height:
                set_res_attempt = 0
            
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
