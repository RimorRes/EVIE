import time
from picamera2 import Picamera2

# TODO: Asynchronous capture. Make sure we can capture at 50fps MINIMUM.
# TODO: try having seperate threads for seperate cameras

picam2 = Picamera2()

config = picam2.create_video_configuration(main={"size": (2304, 1296)})
# config = picam2.create_video_configuration(main={"size": (1440, 1280)})
picam2.align_configuration(config)
print(config["main"])

picam2.configure(config)
picam2.set_controls({"FrameRate": 56})
picam2.start()

frames = []
start = time.time()
duration = 10

while time.time() - start < duration:
    im = picam2.capture_array()
    frames.append(im)
    # cv2.imshow("Camera", im)
    # cv2.waitKey(1)

picam2.stop()
print("Numbers of frames captured:", len(frames))
print("in {} seconds".format(duration))
print("FPS:", len(frames) / duration)
