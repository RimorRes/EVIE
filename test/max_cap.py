import time
from picamera2 import Picamera2


def init_cam(camera_index):
    picam = Picamera2(camera_index)
    config = picam.create_video_configuration(main={"size": (1440, 1280)})
    picam.align_configuration(config)
    picam.configure(config)
    picam.set_controls({"FrameRate": 56})

    return picam


def add_buffer_0(job):
    im = cam0.wait(job)
    frames_0.append(im)


def add_buffer_1(job):
    im = cam1.wait(job)
    frames_1.append(im)


if __name__ == "__main__":
    duration = 10

    cam0 = init_cam(0)
    cam1 = init_cam(1)

    frames_0 = []
    frames_1 = []

    cam0.start()
    cam1.start()

    start = time.time()
    while time.time() - start < duration:
        frame0 = cam0.capture_array(wait=False, signal_function=add_buffer_0)
        frame1 = cam1.capture_array(wait=True, signal_function=add_buffer_1)
        # print("time:", time.time() - start)

    print("Capture done...")
    print("Waiting for fuck all to finish >:(")

    time.sleep(1)

    cam0.close()
    cam1.close()

    n = len(frames_0) + len(frames_1)
    print("Numbers of frames camera 0:", len(frames_0))
    print("Numbers of frames camera 1:", len(frames_1))
    print("in {} seconds".format(duration))
    print("FPS:", n/2 / duration)
