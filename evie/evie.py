import cv2
import pyfiglet
from stereocam import StereoCam

ascii_art = pyfiglet.figlet_format('EVIE', font='isometric1')
print(ascii_art)

print('Running calibration wizard!')
cam = StereoCam(1)
cam.calibration_wizard('../data/calibration.npz')

print('Load calibration...')
cam.load_calibration('../data/calibration.npz')

while True:
    left, right = cam.grab()

    key = cv2.waitKey(1)
    if key == 27:
        cam.close()
        cv2.destroyAllWindows()
        break

    cv2.imshow('Stereo Cam', cv2.addWeighted(left, 0.5, right, 0.5, 0))
