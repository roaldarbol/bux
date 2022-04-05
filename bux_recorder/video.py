import cv2

def read_frame(cam, out):
    ret, frame = cam.read() # Capture frame-by-frame
    if ret == True:
        cv2.imshow(str(cam), frame) # Display the resulting frame
    if out:
        out.write(frame)

def check_cv_break(cam_opened):
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return True
    elif not any(cam_opened):
        return True

